# PEMCO Website

Static website for **PEMCO Company Limited** (Progressive Engineer Myanmar Company) — engineering services & general contracting, Yangon.

Live source of truth for page content is `build_site.py`. Most HTML files are **generated**. Prefer editing `build_site.py`, then rebuilding, so image paths and copy stay consistent.

---

## Quick start (local preview)

```bash
cd /path/to/PEMCO
python3 -m http.server 8080
```

Open [http://127.0.0.1:8080/](http://127.0.0.1:8080/)

---

## Rebuild pages after content changes

```bash
python3 build_site.py
```

This regenerates main pages, service pages, and legacy redirect stubs.

**Important:** If you only edit an `.html` file by hand, the next `build_site.py` run will overwrite it. Put lasting changes in `build_site.py` (or update both).

---

## Project layout

```
PEMCO/
├── build_site.py          # Site generator + page content (edit this)
├── index.html             # Generated pages (and siblings)
├── about.html, services.html, projects.html, contact.html
├── civil.html, electrical.html, mechanical.html, …
├── README.md
├── .gitignore
└── assets/
    ├── css/styles.css
    ├── js/main.js, search-data.js
    ├── drawings/tender-drawing-set-example.pdf
    └── images/            # See below
```

Local-only (gitignored): `.venv/`, `_pdf_extract/`

---

## Images

| Path | Purpose |
|------|---------|
| `assets/images/pemco-brand-logo.png` | Header logo |
| `assets/images/service-*.jpg\|png\|jpeg` | Service cards + heroes |
| `assets/images/services-reno.jpg` | Renovation |
| `assets/images/drawing-01.png` … `03.png` | Homepage design strip |
| `assets/images/clients/` | Client marquee logos |
| `assets/images/leadership/` | About leadership photos (named by person) |
| `assets/images/civil-engineering/` etc. | Service page galleries |
| `assets/images/design-drawing/` | Design & Drawing examples |
| `assets/images/projects/` | Portfolio project folders |

### Service card filenames (keep exact names)

- `service-civil.jpg`, `service-electrical.jpg`, `service-mechanical.jpg`
- `service-design.png`, `service-qs.jpeg`, `service-install.jpg`, `services-reno.jpg`

### Client logos

Only files listed in `CLIENT_LOGOS_ROW1` / `CLIENT_LOGOS_ROW2` in `build_site.py` are used. Add a file under `clients/`, register it in those lists, then rebuild.

### Projects

Each project is a folder under `assets/images/projects/`. Titles, order, and image lists live in `PROJECTS_DATA` in `build_site.py`.

---

## Contact form

Static site — no PEMCO server. `assets/js/main.js` posts to **FormSubmit** → `pemco.myanmar@gmail.com`, with `mailto:` fallback.

One-time: activate FormSubmit via the email sent to that Gmail inbox.

---

## Common tasks

| Task | Edit |
|------|------|
| Page copy / scopes / galleries | `build_site.py` → rebuild |
| Swap a photo | Same filename under `assets/images/…` |
| Add project | Folder + `PROJECTS_DATA` + rebuild |
| Styles | `assets/css/styles.css` |
| Search | `assets/js/search-data.js` |
| Form / nav / modal | `assets/js/main.js` |
