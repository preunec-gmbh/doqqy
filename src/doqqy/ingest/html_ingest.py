"""HTML parser/ingester for the doqqy pipeline."""

from __future__ import annotations

from pathlib import Path

from doqqy.ingest.base import Document, IngestError, base_metadata, content_hash, processed_path_for
from doqqy.workspace import Workspace

# Her zaman atılan şablon/boilerplate etiketleri. header/footer bu listede değil:
# onlar yalnızca site şablonuysa atılır (aşağıya bak), makale içindekiler korunur.
_BOILERPLATE_TAGS = ("script", "style", "nav", "aside", "form", "iframe", "noscript", "svg")

# header/footer bu etiketlerin altındaysa gerçek içerik parçası sayılır ve korunur.
_CONTENT_SCOPES = ("article", "section", "main")


def ingest_html(source: Path, ws: Workspace) -> Document:
    """Ingest an HTML file, pre-clean elements/comments with BeautifulSoup,
    and convert to canonical Markdown using markdownify.
    """
    try:
        from bs4 import BeautifulSoup, Comment  # noqa: PLC0415
        from markdownify import markdownify  # noqa: PLC0415
    except ImportError as exc:
        raise IngestError(
            "beautifulsoup4 ve markdownify gerekli: pip install beautifulsoup4 markdownify"
        ) from exc

    # Bytes olarak okuyup çözümlemeyi BeautifulSoup'a (UnicodeDammit) bırakıyoruz:
    # BOM ve <meta charset> bildirimini okuyarak kodlamayı kendisi tespit eder
    # (Türkçe cp1254/windows-1254 sayfalar dahil).
    raw_bytes = source.read_bytes()

    try:
        soup = BeautifulSoup(raw_bytes, "html.parser")
        detected_encoding = soup.original_encoding

        # Sayfa başlığını <head> atılmadan önce yakala.
        title = soup.title.get_text(strip=True) if soup.title else ""
        if soup.head is not None:
            soup.head.decompose()

        # Boilerplate etiketlerini at.
        for element in soup(list(_BOILERPLATE_TAGS)):
            element.decompose()

        # header/footer yalnızca site şablonu (chrome) ise atılır; article/section/main
        # içindekiler dokümanın gerçek başlığını taşıyabilir, korunur.
        for element in soup(["header", "footer"]):
            if element.find_parent(list(_CONTENT_SCOPES)) is None:
                element.decompose()

        # HTML yorumlarını at.
        for comment in soup.find_all(string=lambda text: isinstance(text, Comment)):
            comment.extract()

        has_h1 = soup.find("h1") is not None
        cleaned_html = str(soup)
    except Exception as exc:  # noqa: BLE001
        raise IngestError(f"HTML ayrıştırma hatası: {exc}") from exc

    # Convert to markdown with ATX heading style
    try:
        md = markdownify(cleaned_html, heading_style="ATX").strip()
    except Exception as exc:  # noqa: BLE001
        raise IngestError(f"Markdown dönüştürme hatası: {exc}") from exc

    if not md:
        raise IngestError("boş içerik")

    # Gövdede hiç H1 kalmadıysa <title> doküman başlığı olur — header-aware
    # chunking'in başlıksız tek blok üretmesini engeller.
    if title and not has_h1:
        md = f"# {title}\n\n{md}"

    meta = base_metadata(source, ws.root, kind="html")
    meta["parser"] = "markdownify"
    if title:
        meta["title"] = title
    if detected_encoding:
        meta["encoding"] = detected_encoding
    meta["content_hash"] = content_hash(md)

    return Document(
        source_path=source,
        processed_path=processed_path_for(source, ws),
        content=md,
        metadata=meta,
    )
