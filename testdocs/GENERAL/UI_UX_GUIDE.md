# UI/UX Design Guide

## 1. Overview
This document defines the design principles, component standards, and user experience guidelines for a B2B ERP Integrated E-Commerce Portal. All interface development will be done in accordance with this guide.

## 2. Design Philosophy

### 2.1. Basic Principles
- **Simplicity:** Avoid unnecessary decoration, focus on functionality.
- **Consistency:** The same components, colors, and typography are used across all pages.
- **Accessibility:** Contrast and dimensions conforming to WCAG 2.1 AA standards.
- **Performance:** Lightweight components, fast loading times. Lazyloading can be used.
- **Mobile-First:** Design is first considered for mobile, then extended to desktop.

### 2.2. User Experience Goals
- A new user should be able to place their first order within 5 minutes.
- The admin should be able to approve an order in less than 3 clicks.
- The user should know exactly what to do in case of errors.
- Loading status should be clear to the user (Skeleton screens).

## 3. Design System

### 3.1. UI Library
- **Main Library:** Shadcn/UI (Radix UI primitives + Tailwind CSS)
- **Why:** Customizable, accessible, modern, and lightweight.
- **Alternative Components:** TanStack Table (data tables), React Hook Form (forms)

### 3.2. Color Palette

| Color Type | Value | Usage |
| :--- | :--- | :--- |
| **Primary** | #2563EB (Blue-600) | Main buttons, links, active states |
| **Primary Hover** | #1D4ED8 (Blue-700) | Button hover status |
| **Secondary** | #64748B (Slate-500) | Secondary buttons, texts |
| **Success** | #16A34A (Green-600) | Confirmation, successful transaction, stock available |
| **Warning** | #CA8A04 (Yellow-600) | Warning, critical stock, pending |
| **Danger** | #DC2626 (Red-600) | Error, cancellation, out of stock, limit exceeded |
| **Background** | #F8FAFC (Slate-50) | Page background |
| **Surface** | #FFFFFF (White) | Card, panel, modal background |
| **Border** | #E2E8F0 (Slate-200) | Borders, separators |
| **Text Primary** | #0F172A (Slate-900) | Main headings, text |
| **Text Secondary** | #64748B (Slate-500) | Auxiliary text, placeholder |

### 3.3. Typography

| Element | Font | Size | Weight | Line Height |
| :--- | :--- | :--- | :--- | :--- |
| **H1** | Inter | 32px | 700 | 1.2 |
| **H2** | Inter | 24px | 600 | 1.3 |
| **H3** | Inter | 20px | 600 | 1.4 |
| **Body** | Inter | 16px | 400 | 1.5 |
| **Small** | Inter | 14px | 400 | 1.5 |
| **Caption** | Inter | 12px | 400 | 1.4 |

- **Font Family:** Inter (Google Fonts)
- **Why:** High readability, modern, suitable for B2B interfaces.

### 3.4. Spacing System (8px Grid)

| Token | Value | Usage |
| :--- | :--- | :--- |
| **xs** | 4px | Icon-margin, tight spacing |
| **sm** | 8px | Form elements, nearby elements |
| **md** | 16px | Card inner padding, standard spacing |
| **lg** | 24px | Section spacing, card margin |
| **xl** | 32px | Page padding, large sections |
| **2xl** | 48px | Main section spacing |

### 3.5. Border Radius

| Token | Value | Usage |
| :--- | :--- | :--- |
| **sm** | 4px | Buttons, inputs |
| **md** | 8px | Cards, modals |
| **lg** | 12px | Large containers |
| **full** | 9999px | Avatar, badge, pill buttons |

### 3.6. Shadow System

| Token | Value | Usage |
| :--- | :--- | :--- |
| **sm** | 0 1px 2px rgba(0,0,0,0.05) | Slight scaling, input focus |
| **md** | 0 4px 6px rgba(0,0,0,0.1) | Cards, dropdowns |
| **lg** | 0 10px 15px rgba(0,0,0,0.1) | Modals, floating panels |

| **xl** | 0 20px 25px rgba(0,0,0,0.15) | Large overlays |

## 4. Page Structures and Layout
### 4.1. Ana Layout Yapısı
```
┌─────────────────────────────────────────────┐
│  Header (Logo, User Menu, Notifications)    │
├──────────────┬──────────────────────────────┤
│   Sidebar    │                              │
│   (Nav)      │      Main Content Area       │
│              │                              │
│              │                              │
│              │                              │
└──────────────┴──────────────────────────────┘
```

### 4.2. Header Components
- **Logo:** Top left corner, clickable redirects to dashboard.
- **Search Bar:** Product/barcode quick search (Global search).
- **Notification Icon:** New order notification (for Admin).
- **User Menu:** Profile, Logout, Change Theme.
- **Height:** 64px (fixed).

### 4.3. Sidebar Navigation
- **Width:** 256px (desktop), opens as a drawer on mobile.
- **Menu Items:** Icon + Text combination.
- **Active Status:** Primary color background + white text.
- **Hover Status:** Light gray background.
- **Collapse:** Automatic on mobile.