"""Ingest katmanı ortak tipleri."""

from __future__ import annotations

import hashlib
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from doqqy.config import SUPPORTED_EXTENSIONS, get_logger, sanitize_tag
from doqqy.workspace import Workspace

_LOG = get_logger("doqqy.ingest.base")

# Sanitize edilen/düşürülen klasör adları dosya başına değil, klasör başına
# loglanır — aksi halde 500 dosyalık bir "smart farming" klasörü ingest
# progress bar'ının ortasına 500 aynı satır basar.
_LOGGED_TAG_SOURCES: set[str] = set()

# processed_path_for() aynı gövde adını paylaşan kardeşleri görmek için kaynağın
# klasörünü taramak zorunda. Tarama dosya başına yapılsaydı n dosyalık bir klasör
# n kez taranırdı (500 dosya = 250 bin dizin girişi); bu yüzden sonuç klasör
# başına önbelleğe alınıyor. Önbellek bir çalışmanın ömründen uzun yaşamamalı —
# `doqqy watch` arka arkaya sync çalıştırır ve arada raw/ değişir.
_STEM_GROUP_CACHE: dict[Path, dict[str, list[str]]] = {}

# ws.raw_dir.resolve() dosya başına bir syscall; Manifest.diff her belge için
# processed_path_for çağırdığı için büyük korpuslarda kayda değer bir yük oluyor.
# Aynı çalışma boyunca değişmediğinden önbelleğe alınıyor.
_RESOLVED_RAW_DIRS: dict[Path, Path] = {}


def reset_tag_log_state() -> None:
    """Klasör başına tek log garantisini yeni bir ingest çalışması için sıfırla."""
    _LOGGED_TAG_SOURCES.clear()


def reset_stem_group_cache() -> None:
    """Kardeş taraması önbelleğini boşalt — her ingest/sync çalışması taze başlamalı."""
    _STEM_GROUP_CACHE.clear()
    _RESOLVED_RAW_DIRS.clear()


def _output_name_forms(source: Path) -> tuple[str, str]:
    """Bir kaynağın alabileceği iki çıktı adı: (tekil biçim, ayrıştırılmış biçim).

    Başka biçim yok — bu yüzden bir belgenin *diğer* adı her zaman tek ve
    hesaplanabilir. Grup değiştiğinde geride kalan bayat dosyayı bulmak buna
    dayanıyor.
    """
    return f"{source.stem}.md", f"{source.stem}-{source.suffix.lower().lstrip('.')}.md"


def _stem_groups(parent: Path) -> dict[str, list[str]]:
    """*parent* içindeki desteklenen dosyaları gövde adına göre grupla: stem -> [uzantılar].

    Yalnızca tek bir dizin seviyesi taranır; çakışma ancak aynı klasördeki
    dosyalar arasında olabilir, çünkü processed/ altındaki klasör yapısı raw/
    yapısını birebir korur.

    Gruplama anahtarı ``str.lower()`` ile normalize edilir. ``Rapor.md`` ile
    ``rapor.txt`` harf duyarsız bir dosya sisteminde (Windows, varsayılan macOS)
    tek bir ``rapor.md``ye yazardı; gövde adının yazımını aynen alsaydık bunları
    iki ayrı tekil grup sanıp ayrıştırmaz ve tam da bu issue'nun kapatmaya
    çalıştığı sessiz ezmeyi bırakırdık.

    Kasıtlı olarak ``casefold()`` değil: casefold harf büyüklüğünün ötesine geçen
    katlamalar da yapar (``maße`` -> ``masse``) ve hiçbir dosya sisteminin aynı
    saymadığı çiftleri gereksiz yere ayrıştırırdı. ``lower()`` harf büyüklüğüyle
    sınırlı kalıp platformdan bağımsız aynı sonucu üretiyor.
    """
    cached = _STEM_GROUP_CACHE.get(parent)
    if cached is not None:
        return cached

    try:
        entries = list(parent.iterdir())
    except OSError as exc:
        # Klasör okunamıyorsa çakışma tespiti YAPILAMAZ ve bunu söylemek zorundayız.
        # Boş sözlük dönmek "bu gövde adı tekildir" pozitif iddiasıdır; yanlış
        # olduğunda dosya yanlış adla yazılır, diff onu yeniden adlandırılmış sanar
        # ve doğru olan eski çıktıyı sildirir. Bilmiyorsak hata veriyoruz — çağıran
        # katman bunu dosya bazında izole eder (§1.4). Sonuç önbelleğe de alınmıyor:
        # geçici bir hata tüm çalışmayı zehirlememeli.
        raise IngestError(f"{parent} taranamadı, ad çakışması tespit edilemiyor: {exc}") from exc

    groups: dict[str, list[str]] = {}
    for entry in entries:
        suffix = entry.suffix.lower()
        if suffix in SUPPORTED_EXTENSIONS and entry.is_file():
            groups.setdefault(entry.stem.lower(), []).append(suffix)

    _STEM_GROUP_CACHE[parent] = groups
    return groups


@dataclass
class Document:
    """Kanonik markdown haline gelmiş bir doküman."""

    source_path: Path                       # raw/auth/jwt.pdf
    processed_path: Path                    # processed/auth/jwt.md
    content: str                            # kanonik markdown
    metadata: dict[str, Any] = field(default_factory=dict)

    def write(self) -> None:
        """processed_path'e frontmatter + content yaz."""
        self.processed_path.parent.mkdir(parents=True, exist_ok=True)
        body = _serialize(self)
        self.processed_path.write_text(body, encoding="utf-8")


def _serialize(doc: Document) -> str:
    """Frontmatter blok + body."""
    import yaml  # type: ignore

    fm = yaml.safe_dump(doc.metadata, allow_unicode=True, sort_keys=True).strip()
    return f"---\n{fm}\n---\n\n{doc.content.strip()}\n"


@dataclass
class IngestResult:
    """Bir ingest çalışmasının özet sonucu."""

    succeeded: list[Path] = field(default_factory=list)
    failed: list[tuple[Path, str]] = field(default_factory=list)
    skipped: list[Path] = field(default_factory=list)
    # Gövde adı bir kardeşiyle çakıştığı için çıktısı <stem>-<ext>.md olarak
    # yazılan kaynaklar (issue #76). Yeniden adlandırma sessiz kalmasın diye
    # çalışma özetinde raporlanır.
    disambiguated: list[Path] = field(default_factory=list)

    @property
    def total(self) -> int:
        return len(self.succeeded) + len(self.failed) + len(self.skipped)


class IngestError(Exception):
    """Parser-spesifik hatalar bu tipte sarılır."""


def content_hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]


def processed_path_for(source: Path, ws: Workspace) -> Path:
    """Kaynağın processed/ altındaki kanonik .md hedef yolu.

    raw/ altındaki klasör yapısı korunur; raw/ dışındaki kaynaklar
    doğrudan processed/ köküne düşer.

    Aynı gövde adını paylaşan birden fazla kaynak varsa (``rapor.pdf`` ile
    ``rapor.docx`` yan yana) hepsi tek bir ``rapor.md``ye yazıp birbirini ezerdi.
    Böyle bir grubun **her** üyesi uzantısıyla ayrıştırılır: ``rapor-pdf.md``,
    ``rapor-docx.md``. Grup tek üyeliyse ad değişmez, dolayısıyla mevcut
    workspace'lerdeki çıktılar yeniden adlandırılmaz.

    Karar bilerek bu yardımcının içinde veriliyor: ``doqqy ingest`` ile
    ``doqqy sync``in kullandığı dosya başına yol aynı fonksiyondan geçtiği için
    ikisi aynı sonucu üretmek zorunda kalıyor.

    DİKKAT: sonuç kaynağın klasöründeki o anki kardeşlere bağlı. Silinmiş bir
    kaynağın çıktısını bulmak için bu fonksiyon kullanılamaz — kaynak diskten
    kalkınca grup küçülür ve farklı bir ad döner. Onun için manifest'teki
    ``ManifestEntry.processed_path`` alanı var.
    """
    resolved = source.resolve()
    raw_dir = _RESOLVED_RAW_DIRS.get(ws.raw_dir)
    if raw_dir is None:
        raw_dir = ws.raw_dir.resolve()
        _RESOLVED_RAW_DIRS[ws.raw_dir] = raw_dir

    try:
        rel = resolved.relative_to(raw_dir)
    except ValueError:
        rel = Path(source.name)

    plain, disambiguated = _output_name_forms(resolved)
    suffixes = _stem_groups(resolved.parent).get(resolved.stem.lower(), ())
    name = disambiguated if len(suffixes) > 1 else plain

    return ws.processed_dir / rel.parent / name


def processed_id(processed_path: Path, ws: Workspace) -> str:
    """processed/ yolunun manifest'te saklanan taşınabilir biçimi (ws.root'a göre, / ile)."""
    try:
        return str(processed_path.relative_to(ws.root)).replace("\\", "/")
    except ValueError:
        return processed_path.name


def claims_source(processed_path: Path, source_id: str) -> bool:
    """*processed_path* var ve frontmatter'ı kaynak olarak *source_id*'yi mi gösteriyor?

    Bir processed dosyasının kime ait olduğunun manifest'ten bağımsız tek kanıtı
    bu. Bayat bir çıktıyı silmeden önce sorulur: adı uyan ama başkasına ait bir
    dosyaya asla dokunulmaz.
    """
    import frontmatter  # type: ignore

    # Geniş yakalama kasıtlı: bu fonksiyon bir dosyayı SİLİP silmemeye karar
    # veriyor ve okunamayan bir dosya hakkında verilecek tek güvenli cevap
    # "bana ait değil". Bozuk YAML (yarım yazılmış frontmatter) yaml.YAMLError
    # fırlatır — ValueError'dan türemez, dolayısıyla dar bir except onu kaçırır
    # ve `doqqy sync` ile `doqqy status` tek bozuk dosyada komple düşerdi.
    try:
        with processed_path.open("r", encoding="utf-8") as fh:
            post = frontmatter.load(fh)
    except Exception:  # noqa: BLE001
        return False
    return str(post.metadata.get("source", "")).replace("\\", "/") == source_id


def drop_superseded_output(ws: Workspace, source: Path, current: Path, source_id: str) -> Path | None:
    """Bu belgenin *diğer* ad biçimindeki bayat çıktısını sil; silineni döndür.

    Bir kaynağın kardeş kümesi değiştiğinde adı iki biçim arasında gidip gelir.
    Eski dosya kaldırılmazsa chunk/map/inject onu ayrı bir belge sanar: kaynak
    duruyorsa içerik indekste ikilenir, silinmişse geri gelir.

    Silme yalnızca frontmatter dosyanın gerçekten bu kaynağa ait olduğunu
    söylüyorsa yapılır; ad benzerliği tek başına yeterli değil.
    """
    plain, disambiguated = _output_name_forms(source)
    other_name = disambiguated if current.name == plain else plain
    other = current.parent / other_name

    if other == current or not other.exists() or not claims_source(other, source_id):
        return None

    # processed/ dışına asla çıkma — yol manifest'ten gelmiş olabilir.
    try:
        other.resolve().relative_to(ws.processed_dir.resolve())
    except ValueError:
        _LOG.warning("processed/ dışındaki %s silinmedi.", other)
        return None

    try:
        other.unlink()
    except OSError as exc:
        _LOG.warning("Bayat çıktı %s silinemedi: %s", other, exc)
        return None
    return other


def base_metadata(source: Path, project_root: Path, kind: str) -> dict[str, Any]:
    rel = source.relative_to(project_root) if source.is_absolute() else source

    # "raw/" veya proje_root altındaki klasör kırılımlarını filtrele
    # Örneğin: raw/bulut-saha/ornek-b2b-sistemi/veri.md
    # -> tags: ["bulut-saha", "ornek-b2b-sistemi"]
    parts = list(rel.parts)
    if parts and parts[0] == "raw":
        parts = parts[1:]

    # Son parça dosya adı, onu atıyoruz. Kalanlar klasör isimleri (tag'ler)
    raw_tags = parts[:-1] if len(parts) > 1 else []

    tags: list[str] = []
    for raw_tag in raw_tags:
        sanitized = sanitize_tag(raw_tag)
        first_time = raw_tag not in _LOGGED_TAG_SOURCES
        if sanitized is None:
            if first_time:
                _LOGGED_TAG_SOURCES.add(raw_tag)
                _LOG.warning("klasör adı %r geçerli bir tag üretmedi, atlandı (ilk görülen: %s).", raw_tag, rel)
            continue
        if sanitized != raw_tag and first_time:
            _LOGGED_TAG_SOURCES.add(raw_tag)
            _LOG.info("tag %r -> %r olarak temizlendi (ilk görülen: %s).", raw_tag, sanitized, rel)
        tags.append(sanitized)

    return {
        "source": str(rel).replace("\\", "/"),
        "type": kind,
        "tags": tags,
        "ingested_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    }
