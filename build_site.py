#!/usr/bin/env python3
"""Generate PEMCO static HTML pages with shared chrome."""
import json
from pathlib import Path

ROOT = Path(__file__).parent

HEADER = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{description}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@500;600;700&family=IBM+Plex+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/css/styles.css">
</head>
<body>
<a class="sr-only" href="#main">Skip to content</a>
<header class="site-header">
  <div class="container nav-bar">
    <a class="brand" href="index.html" aria-label="PEMCO home">
      <img src="assets/images/pemco-brand-logo.png" alt="PEMCO - Engineering Services &amp; General Contractor">
    </a>
    <div class="nav-cluster">
      <nav aria-label="Primary">
        <ul class="nav-links">
          <li><a href="index.html" class="{active_home}">Home</a></li>
          <li>
            <button type="button" data-dropdown aria-expanded="false" aria-haspopup="true">About <i class="chevron" aria-hidden="true"></i></button>
            <div class="dropdown" role="menu">
              <a href="about.html">Our Company</a>
              <a href="about.html#leadership">Leadership</a>
              <a href="about.html#facilities">Facilities</a>
            </div>
          </li>
          <li>
            <button type="button" data-dropdown aria-expanded="false" aria-haspopup="true" class="{active_services_btn}">Services <i class="chevron" aria-hidden="true"></i></button>
            <div class="mega" role="menu">
              <div class="mega-col">
                <h4>Core Disciplines</h4>
                <a href="civil.html">Civil Engineering</a>
                <a href="electrical.html">Electrical Engineering</a>
                <a href="mechanical.html">Mechanical Engineering</a>
                <a href="design-drawing.html">Design &amp; Drawing Services</a>
              </div>
              <div class="mega-col">
                <h4>Delivery</h4>
                <a href="quantity-surveyor.html">Quantity Surveyor Services</a>
                <a href="installation-repairs.html">Installation &amp; Repairs</a>
                <a href="renovation.html">Renovation</a>
                <a href="services.html">All Services</a>
              </div>
            </div>
          </li>
          <li><a href="projects.html" class="{active_projects}">Projects</a></li>
          <li><a href="contact.html" class="{active_contact}">Contact</a></li>
          <li><a class="cta-nav" href="contact.html">Request a Quote</a></li>
        </ul>
      </nav>
      <button class="icon-btn" type="button" data-search-open aria-label="Search site">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg>
      </button>
      <button class="icon-btn menu-toggle" type="button" aria-label="Open menu" aria-expanded="false">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16"/></svg>
      </button>
    </div>
  </div>
</header>

<div class="search-overlay" aria-hidden="true">
  <div class="search-panel" role="dialog" aria-modal="true" aria-label="Site search">
    <div class="search-bar">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg>
      <input id="site-search" type="search" placeholder="Search services, projects, drawings…" autocomplete="off">
      <button class="search-close" type="button" data-search-close aria-label="Close search">✕</button>
    </div>
    <div id="search-results" class="search-results"></div>
  </div>
</div>
"""

FOOTER = """
<footer class="site-footer">
  <div class="container footer-grid">
    <div class="footer-brand">
      <strong>PEMCO</strong>
      <p>Progressive Engineer Myanmar Company Limited — engineering services and general contracting since 1996.</p>
    </div>
    <div>
      <h3>Services</h3>
      <div class="footer-links">
        <a href="civil.html">Civil</a>
        <a href="electrical.html">Electrical</a>
        <a href="mechanical.html">Mechanical</a>
        <a href="design-drawing.html">Design &amp; Drawing</a>
      </div>
    </div>
    <div>
      <h3>Company</h3>
      <div class="footer-links">
        <a href="about.html">About</a>
        <a href="projects.html">Projects</a>
        <a href="services.html">All Services</a>
        <a href="contact.html">Contact</a>
      </div>
    </div>
    <div>
      <h3>Head Office</h3>
      <p>#1404–1406, Yuzana Tower, Shwe Gon Taing Junction, Bahan Township, Yangon, Myanmar 11201</p>
      <p style="margin-top:.7rem"><a href="mailto:pemco@myanmar.com.mm">pemco@myanmar.com.mm</a><br><a href="mailto:pemco.myanmar@gmail.com">pemco.myanmar@gmail.com</a></p>
    </div>
  </div>
  <div class="container footer-bottom">
    <span>© 2026 PEMCO Company Limited. All rights reserved.</span>
    <span>Yangon · Fabrication Shop, North Dagon</span>
  </div>
</footer>

<div class="project-modal" id="project-modal" aria-hidden="true" role="dialog" aria-modal="true" aria-label="Project photo gallery">
  <div class="project-modal-backdrop" data-modal-close></div>
  <div class="project-modal-dialog">
    <div class="project-modal-header">
      <div class="project-modal-info">
        <h3 id="project-modal-title">Project Title</h3>
        <p id="project-modal-desc">Project Description</p>
      </div>
      <div class="project-modal-actions">
        <span class="project-modal-counter" id="project-modal-counter">1 / 1</span>
        <button class="project-modal-close" type="button" data-modal-close aria-label="Close photo gallery">✕</button>
      </div>
    </div>
    <div class="project-modal-body">
      <button class="project-modal-nav prev" type="button" id="project-modal-prev" aria-label="Previous photo">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M15 18l-6-6 6-6"/></svg>
      </button>
      <div class="project-modal-stage" id="project-modal-stage">
        <img id="project-modal-img" src="" alt="Project photo">
      </div>
      <button class="project-modal-nav next" type="button" id="project-modal-next" aria-label="Next photo">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M9 18l6-6-6-6"/></svg>
      </button>
    </div>
    <div class="project-modal-footer">
      <div class="project-modal-thumbs" id="project-modal-thumbs"></div>
    </div>
  </div>
</div>

<script src="assets/js/search-data.js"></script>
<script src="assets/js/main.js"></script>
</body>
</html>
"""


def chrome(active=""):
    return {
        "active_home": "is-active" if active == "home" else "",
        "active_services_btn": "is-active" if active == "services" else "",
        "active_projects": "is-active" if active == "projects" else "",
        "active_contact": "is-active" if active == "contact" else "",
        "active_about": "is-active" if active == "about" else "",
    }


# Client logos split across two streaming rows
CLIENT_LOGOS_ROW1 = [
    ("totalenergies.svg", "TotalEnergies"),
    ("marina-bay-sands.png", "Marina Bay Sands"),
    ("komatsu.svg", "Komatsu"),
    ("unicef.svg", "UNICEF"),
    ("jica.svg", "JICA"),
    ("mitsui-mark.svg", "Mitsui"),
    ("nokia.svg", "Nokia"),
    ("mitsubishi.svg", "Mitsubishi"),
    ("chatrium.png", "Chatrium"),
    ("cp-seed.svg", "CP Seed"),
]

CLIENT_LOGOS_ROW2 = [
    ("mpt.png", "MPT"),
    ("zamil.png", "Zamil Steel"),
    ("okamura.png", "Okamura"),
    ("japan-embassy.svg", "Embassy of Japan"),
    ("australian-embassy.svg", "Australian Embassy"),
    ("asia-optical.svg", "Asia Optical"),
    ("hotel-nikko.svg", "Hotel Nikko"),
    ("strand-hotel.svg", "The Strand"),
    ("acecook.png", "Acecook"),
]


def clients_marquee(section_id="clients", heading="Selected clients & partners"):
    def make_row(logos, is_reverse=False):
        items = "".join(
            f'<div class="marquee-item"><img src="assets/images/clients/{src}" alt="{name.replace("&", "&amp;")}"></div>'
            for src, name in logos
        )
        row_class = "marquee-row marquee-row-reverse" if is_reverse else "marquee-row"
        return (
            f'<div class="{row_class}">'
            f'<div class="marquee-group">{items}{items}</div>'
            f'<div class="marquee-group" aria-hidden="true">{items}{items}</div>'
            '</div>'
        )

    return f"""
  <section class="clients-section" id="{section_id}" aria-label="Clients and partners">
    <div class="section-head">
      <span class="eyebrow">Clients &amp; partners</span>
      <h2>{heading}</h2>
    </div>
    <div class="marquee">
      {make_row(CLIENT_LOGOS_ROW1, is_reverse=True)}
      {make_row(CLIENT_LOGOS_ROW2, is_reverse=False)}
    </div>
  </section>
"""


def page(title, description, active, body):
    return HEADER.format(title=title, description=description, **chrome(active)) + body + FOOTER


PROJECTS_DATA = [
    {
        "id": "thilawa-substation",
        "title": "230kV Thilawa Substation",
        "desc": "Civil, electrical & mechanical works",
        "tag": "Power & Infrastructure",
        "cover": "assets/images/projects/Thilawa-Subsation/230kV-Thilawa-Substation/01.jpg",
        "images": [
            "assets/images/projects/Thilawa-Subsation/230kV-Thilawa-Substation/01.jpg",
            "assets/images/projects/Thilawa-Subsation/230kV-Thilawa-Substation/02.png",
            "assets/images/projects/Thilawa-Subsation/230kV-Thilawa-Substation/03.jpg",
            "assets/images/projects/Thilawa-Subsation/230kV-Thilawa-Substation/04.png",
        ],
    },
    {
        "id": "thilawa-port",
        "title": "Thilawa Port Extension",
        "desc": "Mechanical & electrical installation",
        "tag": "Port Infrastructure",
        "cover": "assets/images/projects/Thilawa-Subsation/Thilawa-port-Extension/01.jpg",
        "images": [
            "assets/images/projects/Thilawa-Subsation/Thilawa-port-Extension/01.jpg",
            "assets/images/projects/Thilawa-Subsation/Thilawa-port-Extension/02.jpg",
            "assets/images/projects/Thilawa-Subsation/Thilawa-port-Extension/03.jpg",
            "assets/images/projects/Thilawa-Subsation/Thilawa-port-Extension/04.jpg",
            "assets/images/projects/Thilawa-Subsation/Thilawa-port-Extension/05.jpg",
            "assets/images/projects/Thilawa-Subsation/Thilawa-port-Extension/06.jpg",
        ],
    },
    {
        "id": "water-purification",
        "title": "Water & Wastewater Plants",
        "desc": "Thilawa SEZ treatment facilities",
        "tag": "Water & Environmental",
        "cover": "assets/images/projects/Thilawa-Subsation/Water-Purification-Plant%20%26%20Sewage-Water-Treatment/01.png",
        "images": [
            "assets/images/projects/Thilawa-Subsation/Water-Purification-Plant%20%26%20Sewage-Water-Treatment/01.png",
            "assets/images/projects/Thilawa-Subsation/Water-Purification-Plant%20%26%20Sewage-Water-Treatment/02.png",
            "assets/images/projects/Thilawa-Subsation/Water-Purification-Plant%20%26%20Sewage-Water-Treatment/03.png",
            "assets/images/projects/Thilawa-Subsation/Water-Purification-Plant%20%26%20Sewage-Water-Treatment/04.png",
            "assets/images/projects/Thilawa-Subsation/Water-Purification-Plant%20%26%20Sewage-Water-Treatment/05.png",
        ],
    },
    {
        "id": "ywama-power-plant",
        "title": "50MW Ywama Power Plant",
        "desc": "Power plant civil & M&E works",
        "tag": "Power Generation",
        "cover": "assets/images/projects/50MW-Ywama-Power-Plant/01.png",
        "images": [
            "assets/images/projects/50MW-Ywama-Power-Plant/01.png",
            "assets/images/projects/50MW-Ywama-Power-Plant/02.png",
            "assets/images/projects/50MW-Ywama-Power-Plant/03.png",
            "assets/images/projects/50MW-Ywama-Power-Plant/04.png",
            "assets/images/projects/50MW-Ywama-Power-Plant/05.png",
        ],
    },
    {
        "id": "marina-bay-acmv",
        "title": "ACMV System Work at Marina Bay",
        "desc": "Air-conditioning & mechanical ventilation",
        "tag": "Mechanical & HVAC",
        "cover": "assets/images/projects/ACMV-System-Work-at-Marina-Bay/01.jpg",
        "images": [
            "assets/images/projects/ACMV-System-Work-at-Marina-Bay/01.jpg",
            "assets/images/projects/ACMV-System-Work-at-Marina-Bay/02.jpg",
            "assets/images/projects/ACMV-System-Work-at-Marina-Bay/03.jpg",
            "assets/images/projects/ACMV-System-Work-at-Marina-Bay/04.jpg",
            "assets/images/projects/ACMV-System-Work-at-Marina-Bay/05.jpg",
            "assets/images/projects/ACMV-System-Work-at-Marina-Bay/06.jpg",
        ],
    },
    {
        "id": "asia-optical",
        "title": "Asia Optical Steel Structure Erection",
        "desc": "Structural steel fabrication & erection",
        "tag": "Structural Steel",
        "cover": "assets/images/projects/Asia-Optical-Steel-Structure-Erection%20/01.jpg",
        "images": [
            "assets/images/projects/Asia-Optical-Steel-Structure-Erection%20/01.jpg",
            "assets/images/projects/Asia-Optical-Steel-Structure-Erection%20/02.jpg",
            "assets/images/projects/Asia-Optical-Steel-Structure-Erection%20/03.jpg",
            "assets/images/projects/Asia-Optical-Steel-Structure-Erection%20/04.jpg",
            "assets/images/projects/Asia-Optical-Steel-Structure-Erection%20/05.jpg",
        ],
    },
    {
        "id": "komatsu-reman",
        "title": "Komatsu Remanufacturing",
        "desc": "Industrial facility M&E packages",
        "tag": "Industrial Facility",
        "cover": "assets/images/projects/Komat%27su-Remanufacturing/01.png",
        "images": [
            "assets/images/projects/Komat%27su-Remanufacturing/01.png",
            "assets/images/projects/Komat%27su-Remanufacturing/02.png",
            "assets/images/projects/Komat%27su-Remanufacturing/03.jpg",
            "assets/images/projects/Komat%27su-Remanufacturing/04.jpg",
        ],
    },
    {
        "id": "muse-mall",
        "title": "MUSE Shopping Mall",
        "desc": "Commercial M&E & interiors",
        "tag": "Commercial",
        "cover": "assets/images/projects/MUSE-Shopping-Mall/01.jpg",
        "images": [
            "assets/images/projects/MUSE-Shopping-Mall/01.jpg",
            "assets/images/projects/MUSE-Shopping-Mall/02.jpg",
            "assets/images/projects/MUSE-Shopping-Mall/03.jpg",
            "assets/images/projects/MUSE-Shopping-Mall/04.jpg",
            "assets/images/projects/MUSE-Shopping-Mall/05.jpg",
        ],
    },
    {
        "id": "myanmar-kaido",
        "title": "Myanmar Kaido",
        "desc": "Factory and facility construction",
        "tag": "Civil & Construction",
        "cover": "assets/images/projects/Myanmar-kaido/01.jpg",
        "images": [
            "assets/images/projects/Myanmar-kaido/01.jpg",
            "assets/images/projects/Myanmar-kaido/02.jpg",
        ],
    },
    {
        "id": "naypyidaw-airport",
        "title": "Nay Pyi Daw Airport",
        "desc": "Airport infrastructure works",
        "tag": "Aviation & Infrastructure",
        "cover": "assets/images/projects/Nay-Pyi-Daw-Airport/01.jpg",
        "images": [
            "assets/images/projects/Nay-Pyi-Daw-Airport/01.jpg",
            "assets/images/projects/Nay-Pyi-Daw-Airport/02.png",
            "assets/images/projects/Nay-Pyi-Daw-Airport/03.png",
            "assets/images/projects/Nay-Pyi-Daw-Airport/04.png",
        ],
    },
    {
        "id": "yadana-platform",
        "title": "Yadana Platform",
        "desc": "Offshore oil & gas platform works",
        "tag": "Energy & Offshore",
        "cover": "assets/images/projects/Yadana-Platform/01.jpg",
        "images": [
            "assets/images/projects/Yadana-Platform/01.jpg",
            "assets/images/projects/Yadana-Platform/02.jpg",
            "assets/images/projects/Yadana-Platform/03.jpg",
            "assets/images/projects/Yadana-Platform/04.jpg",
        ],
    },
]


def render_project_tile(p, extra_class=""):
    title = p["title"]
    desc = p["desc"]
    cover = p["cover"]
    images = p["images"]
    img_json = json.dumps(images).replace('"', "&quot;")
    count = len(images)
    count_label = f"{count} Photos" if count > 1 else "1 Photo"
    return f"""                <figure class="project-tile {extra_class}" tabindex="0" role="button" aria-label="View {title} gallery ({count_label})" data-gallery-title="{title}" data-gallery-desc="{desc}" data-gallery-images="{img_json}">
                  <img src="{cover}" alt="{title}" loading="lazy">
                  <span class="project-tile-badge"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="2"/><circle cx="8.5" cy="8.5" r="1.5"/><path d="m21 15-5-5L5 21"/></svg> {count_label}</span>
                  <figcaption><h3>{title}</h3><p>{desc}</p></figcaption>
                </figure>"""


PAGES = {}

PAGES["index.html"] = page(
    "PEMCO Engineering | Engineering Services & General Contractor",
    "PEMCO Company Limited — electrical, mechanical, civil engineering, design & drawing, and construction services in Myanmar since 1996.",
    "home",
    """
<main id="main">
"""
    + """
  <section class="hero">
    <div class="hero-media" role="img" aria-label="PEMCO project building"></div>
    <div class="hero-content">
      <div class="hero-brand">PEMCO<span>Since 1996 · Yangon, Myanmar</span></div>
      <h1>Engineering partners for complex builds</h1>
      <p>Hire PEMCO for electrical, mechanical, and civil delivery — plus design &amp; drawing outsourcing for international teams.</p>
      <div class="hero-actions">
        <a class="btn btn-primary" href="services.html">Explore Services</a>
        <a class="btn btn-secondary" href="contact.html">Talk to Our Team</a>
      </div>
    </div>
  </section>

  <section class="section">
    <div class="container">
      <div class="section-head reveal">
        <span class="eyebrow">How clients hire us</span>
        <h2>Clear service paths for project owners and consultants</h2>
        <p>Organized for the way procurement teams search: by engineering discipline, then by delivery need.</p>
      </div>
      <div class="capability-grid">
        <a class="capability reveal" href="civil.html">
          <img src="assets/images/service-civil.jpg" alt="Civil engineering project">
          <div class="capability-body">
            <span>Discipline</span>
            <h3>Civil Engineering</h3>
            <p>Factories, buildings, roads, survey, and turnkey civil works.</p>
          </div>
        </a>
        <a class="capability reveal" href="electrical.html">
          <img src="assets/images/service-electrical.jpg" alt="Electrical engineering project">
          <div class="capability-body">
            <span>Discipline</span>
            <h3>Electrical Engineering</h3>
            <p>Power, lighting, earthing, automation, and ELV systems.</p>
          </div>
        </a>
        <a class="capability reveal" href="mechanical.html">
          <img src="assets/images/service-mechanical.jpg" alt="Mechanical engineering project">
          <div class="capability-body">
            <span>Discipline</span>
            <h3>Mechanical Engineering</h3>
            <p>Steel, piping, HVAC, plumbing, tanks, and machine setting.</p>
          </div>
        </a>
        <a class="capability reveal" href="design-drawing.html">
          <img src="assets/images/service-design.jpg" alt="Design and drawing sample">
          <div class="capability-body">
            <span>Outsourcing</span>
            <h3>Design &amp; Drawing</h3>
            <p>Tender and construction drawings for international clients.</p>
          </div>
        </a>
        <a class="capability reveal" href="quantity-surveyor.html">
          <img src="assets/images/service-qs.jpg" alt="Quantity surveying documentation">
          <div class="capability-body">
            <span>Commercial</span>
            <h3>Quantity Surveyor</h3>
            <p>Measurement, costing, and tender documentation support.</p>
          </div>
        </a>
        <a class="capability reveal" href="installation-repairs.html">
          <img src="assets/images/service-install.jpg" alt="Installation and repairs project">
          <div class="capability-body">
            <span>Delivery</span>
            <h3>Installation &amp; Repairs</h3>
            <p>M&amp;E installation, commissioning support, and maintenance.</p>
          </div>
        </a>
      </div>
    </div>
  </section>

  <section class="section section-tone">
    <div class="container split">
      <div class="split-media reveal" style="background-image:url('assets/images/office.jpg')"></div>
      <div class="split-copy reveal">
        <span class="eyebrow">Why PEMCO</span>
        <h2>Built for owners who need reliable engineering execution</h2>
        <p>PEMCO Co., Ltd. (Progressive Engineer Myanmar Company) has delivered industrial, commercial, power, and infrastructure works across Myanmar since 1996.</p>
        <p>From fabrication shop capacity in North Dagon to site installation teams, we support full project lifecycles — design, construction, M&amp;E, and renovation.</p>
        <ul class="split-list">
          <li>Head office at Yuzana Tower, Bahan Township, Yangon</li>
          <li>Dedicated electrical, mechanical, civil, design, QS, and renovation sections</li>
          <li>Proven delivery on power plants, factories, ports, and interiors</li>
        </ul>
        <a class="btn btn-outline" href="about.html">About the company</a>
      </div>
    </div>
  </section>
"""
    + clients_marquee()
    + """
  <section class="section section-dark">
    <div class="container">
      <div class="section-head reveal">
        <span class="eyebrow">Track record</span>
        <h2>Projects that demonstrate multi-discipline capability</h2>
        <p>Selected works from PEMCO’s company profile — industrial, power, commercial, and social infrastructure.</p>
      </div>
      <div class="project-carousel reveal" data-project-carousel>
        <div class="project-carousel-viewport">
          <div class="project-carousel-track">
            <div class="project-carousel-slide">
              <div class="project-grid">
"""
    + "\n".join(render_project_tile(p) for p in PROJECTS_DATA[:6])
    + """
              </div>
            </div>
            <div class="project-carousel-slide">
              <div class="project-grid">
"""
    + "\n".join(render_project_tile(p) for p in PROJECTS_DATA[6:])
    + """
              </div>
            </div>
          </div>
        </div>
        <div class="project-carousel-controls">
          <button class="project-carousel-btn" type="button" data-carousel-prev aria-label="Previous projects">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M15 18l-6-6 6-6"/></svg>
          </button>
          <div class="project-carousel-dots" data-carousel-dots></div>
          <button class="project-carousel-btn" type="button" data-carousel-next aria-label="Next projects">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M9 18l6-6-6-6"/></svg>
          </button>
        </div>
      </div>
      <div style="margin-top:1.6rem" class="reveal">
        <a class="btn btn-secondary" href="projects.html">View project portfolio</a>
      </div>
      <div class="stats reveal">
        <div class="stat"><strong>1996</strong><span>Established in Myanmar</span></div>
        <div class="stat"><strong>3</strong><span>Core engineering disciplines</span></div>
        <div class="stat"><strong>M&amp;E</strong><span>Fabrication + site installation</span></div>
        <div class="stat"><strong>QS</strong><span>Commercial support in-house</span></div>
      </div>
    </div>
  </section>

  <section class="section">
    <div class="container">
      <div class="section-head reveal">
        <span class="eyebrow">Design outsourcing</span>
        <h2>Drawing support for international companies</h2>
        <p>Need tender or construction drawings aligned to electrical, mechanical, or civil scopes? Contact us for quotes.</p>
      </div>
      <div class="drawing-grid reveal">
        <figure>
          <img src="assets/images/drawing-01.jpg" alt="Sample tender drawing layout">
          <figcaption>Sample tender drawing set</figcaption>
        </figure>
        <figure>
          <img src="assets/images/drawing-02.jpg" alt="Sample interior layout drawing">
          <figcaption>Layout &amp; detailing support</figcaption>
        </figure>
        <figure>
          <img src="assets/images/drawing-03.jpg" alt="Sample elevation drawing">
          <figcaption>Elevation &amp; joinery packages</figcaption>
        </figure>
      </div>
      <div style="margin-top:1.5rem" class="reveal">
        <a class="btn btn-primary" href="design-drawing.html">Design &amp; Drawing Services</a>
      </div>
    </div>
  </section>

  <section class="section" style="padding-top:0">
    <div class="container">
      <div class="cta-band reveal">
        <div>
          <h2>Ready to scope your next package?</h2>
          <p>Tell us whether you need construction, M&amp;E installation, renovation, or drawing outsourcing.</p>
        </div>
        <a class="btn btn-primary" href="contact.html">Contact PEMCO</a>
      </div>
    </div>
  </section>
</main>
""",
)

def leadership_html():
    leaders = [
        ("U Nay Soe Aung", "Managing Director"),
        ("U Aung Ko", "General Manager"),
        ("U Yin Sein", "Board of Director"),
        ("U Aung Aung Kyaw", "Board of Director"),
        ("U Ye Htut Aye", "Board of Director"),
        ("U Khin Maung Lin", "Board of Director"),
        ("U Htun Htun Oo", "Board of Director"),
        ("U Saw Yan Aung Thein", "Board of Director"),
        ("U Ko Ko Naing", "Board of Director"),
    ]
    cards = []
    for name, title in leaders:
        src = f"assets/images/leadership/{name}.jpg"
        cards.append(
            f"""
        <article class="leader-card reveal">
          <div class="leader-photo">
            <img src="{src}" alt="{name}" loading="lazy">
          </div>
          <h3>{name}</h3>
          <p class="leader-title">{title}</p>
        </article>"""
        )
    return f"""
  <section class="section section-tone" id="leadership">
    <div class="container">
      <div class="section-head reveal">
        <span class="eyebrow">Leadership</span>
        <h2>Board and management</h2>
        <p>PEMCO is guided by an experienced leadership team across construction and engineering delivery.</p>
      </div>
      <div class="leadership-grid">
        {''.join(cards)}
      </div>
    </div>
  </section>
"""


PAGES["about.html"] = page(
    "About PEMCO | Progressive Engineer Myanmar Company",
    "Learn about PEMCO Co., Ltd. — established 1996/1997 in Yangon with electrical, mechanical, civil, design, QS, and renovation capability.",
    "about",
    f"""
<main id="main">
  <section class="page-hero" style="--page-bg:url('assets/images/office.jpg')">
    <div class="container">
      <span class="eyebrow" style="color:#ffb3bd">About</span>
      <h1>Progressive Engineer Myanmar Company</h1>
      <p>PEMCO Company Limited delivers engineering services and general contracting from Yangon — with fabrication capacity and multi-discipline project teams.</p>
    </div>
  </section>

  <section class="section">
    <div class="container content-grid">
      <div class="content-block reveal">
        <h2>Company profile</h2>
        <p>PEMCO Co., Ltd. (Progressive Engineer Myanmar Company) was established in the mid-1990s and operates as an engineering services and general contractor serving industrial, commercial, power, and infrastructure clients.</p>
        <p>Our organization includes Construction, Electrical, Mechanical, Civil, Engineering Service, Renovation, Design &amp; Drawing, Quantity Surveying, Quality Control, and Safety Administration functions.</p>
        <ul class="detail-list">
          <li><b>01</b><span><strong>Company</strong><br>PEMCO Co., Ltd. (Progressive Engineer Myanmar Company)</span></li>
          <li><b>02</b><span><strong>Established</strong><br>1996 / 1997 · Yangon, Myanmar</span></li>
          <li><b>03</b><span><strong>Head Office</strong><br>#1404, 1405, 1406 Yuzana Tower, Shwe Gon Taing Junction, Bahan Township, Yangon 11201</span></li>
          <li><b>04</b><span><strong>Fabrication Shop</strong><br>E(12), D(14), Economic Development Zone, North Dagon Township, Yangon</span></li>
        </ul>
      </div>
      <aside class="side-panel reveal">
        <h3>Connect with PEMCO</h3>
        <p>Speak with our team about project delivery, fabrication, and multi-discipline engineering support.</p>
        <ul>
          <li>Head office in Bahan Township, Yangon</li>
          <li>Fabrication shop in North Dagon</li>
          <li>Multi-discipline project teams</li>
        </ul>
        <a class="btn btn-primary" href="contact.html">Contact leadership team</a>
      </aside>
    </div>
  </section>

  {leadership_html()}

  <section class="section" id="facilities">
    <div class="container split">
      <div class="split-media reveal" style="background-image:url('assets/images/hero.jpg')"></div>
      <div class="split-copy reveal">
        <span class="eyebrow">Facilities</span>
        <h2>Office, fabrication, and site delivery</h2>
        <p>Head office operations in Bahan Township support project management, design, QS, and commercial coordination.</p>
        <p>Our North Dagon fabrication shop supports steel structure, tank, and related mechanical fabrication ahead of site installation.</p>
        <ul class="split-list">
          <li>Head Office tel: +95-1-559678 / 559751 / 554885</li>
          <li>Additional lines: +95-1-558446 · +95-9-454241563 · +95-9-977126591</li>
          <li>Fabrication shop tel: +95-1-586054</li>
          <li>Email: pemco@myanmar.com.mm · pemco.myanmar@gmail.com</li>
        </ul>
      </div>
    </div>
  </section>
</main>
""",
)

def gallery_html(folder, count=5, captions=None, layout="gallery-stack"):
    from pathlib import Path
    if captions is not None:
        count = min(count, len(captions))
    files = sorted(Path(f"assets/images/{folder}").glob("*.jpg"))[:count]
    if not files:
        return ""
    figs = []
    for i, f in enumerate(files):
        caption = (captions[i] if captions and i < len(captions) else f"Project photo {i+1}")
        figs.append(
            f'<figure class="reveal"><img src="assets/images/{folder}/{f.name}" alt="{caption}" loading="lazy"><figcaption>{caption}</figcaption></figure>'
        )
    grid_class = "gallery-grid"
    if layout:
        grid_class += f" {layout}"
    return f"""
  <section class="section section-tone">
    <div class="container">
      <div class="photo-gallery">
        <h2>Project photos</h2>
        <p class="gallery-lead">Selected delivery photos from PEMCO project work.</p>
        <div class="{grid_class}">
          {''.join(figs)}
        </div>
      </div>
    </div>
  </section>
"""


def service_page(title, desc, hero_img, eyebrow, heading, intro, items, side_title, side_points, gallery_folder, gallery_captions=None, extra="", gallery_layout="gallery-stack"):
    lis = "\n".join(
        f'<li id="{anchor}"><b>{code}</b><span><strong>{name}</strong><br>{blurb}</span></li>'
        for code, anchor, name, blurb in items
    )
    side = "\n".join(f"<li>{p}</li>" for p in side_points)
    # Keep showcase balanced: 1 featured + even pairs
    captions = list(gallery_captions or [])[:5]
    return page(
        title,
        desc,
        "services",
        f"""
<main id="main">
  <section class="page-hero" style="--page-bg:url('{hero_img}')">
    <div class="container">
      <span class="eyebrow" style="color:#ffb3bd">{eyebrow}</span>
      <h1>{heading}</h1>
      <p>{intro}</p>
    </div>
  </section>
  <section class="section">
    <div class="container content-grid">
      <div class="content-block reveal">
        <h2>Scope of work</h2>
        <ul class="detail-list">
          {lis}
        </ul>
        {extra}
      </div>
      <aside class="side-panel reveal">
        <h3>{side_title}</h3>
        <ul>{side}</ul>
        <a class="btn btn-primary" href="contact.html">Request a quote</a>
      </aside>
    </div>
  </section>
  {gallery_html(gallery_folder, count=5, captions=captions, layout=gallery_layout)}
</main>
""",
    )

PAGES["electrical.html"] = service_page(
    "Electrical Engineering | PEMCO",
    "PEMCO electrical engineering: power distribution, lighting, earthing, automation, ELV, generators, and maintenance.",
    "assets/images/service-electrical.jpg",
    "Electrical Engineering",
    "Power, protection, and intelligent electrical systems",
    "From distribution and lighting to ELV and automation — PEMCO installs and maintains electrical systems for industrial and commercial facilities.",
    [
        ("A", "power", "Electrical Power Distribution & Installation", "LV/MV distribution packages for buildings, factories, and industrial plants."),
        ("B", "earthing", "Electrical Earthing & Lightning Protection", "Earthing networks and lightning protection for facility safety compliance."),
        ("C", "lighting", "Electrical Lighting Design & Installation", "Functional and efficient lighting design with installation delivery."),
        ("D", "elv", "Communication & Protection Systems", "PABX, computer network, public address, MATV, CCTV, and fire alarm systems."),
        ("E", "automation", "Electrical Automation", "Control and automation support for plant and building systems."),
        ("F", "power-plant", "Power Plant MEP Work", "Electrical/MEP support for power generation and switchyard environments."),
        ("G", "generator", "Generator Installation", "Generator set installation including related room and support works."),
        ("H", "maintenance", "Electrical Maintenance Work", "Inspection, repair, and upkeep for existing electrical assets."),
    ],
    "Related services",
    ["Mechanical M&E packages", "Design & drawing for electrical layouts", "Installation & repairs", "Quantity surveying for electrical BOQs"],
    "electrical-engineering",
    [
        "Substation & power distribution works",
        "Industrial electrical installation",
        "Switchyard and plant systems",
        "Facility power packages",
        "Commercial electrical delivery",
        "Site electrical commissioning support",
    ],
)

PAGES["mechanical.html"] = service_page(
    "Mechanical Engineering | PEMCO",
    "PEMCO mechanical engineering: steel structures, fuel tanks, hydrant piping, HVAC, plumbing, and machine installation.",
    "assets/images/service-mechanical.jpg",
    "Mechanical Engineering",
    "Fabrication-backed mechanical installation",
    "PEMCO combines fabrication shop capacity with site teams for steel, tanks, piping, HVAC, plumbing, and equipment setting.",
    [
        ("A", "steel", "Steel Structure Fabrication & Installation", "Fabricate and erect structural steel for factories, warehouses, and industrial frames."),
        ("B", "tank", "Fuel Tank Fabrication & Installation", "Tank fabrication and site installation for fuel storage requirements."),
        ("C", "hydrant", "MS Hydrant Piping System (Welded Type)", "Welded mechanical hydrant piping installation for fire protection networks."),
        ("D", "machine", "Machine Setting & Installation", "Alignment and installation of production and process equipment."),
        ("E", "plumbing", "Plumbing & Sanitary System Installation", "Water supply, drainage, and sanitary systems for buildings and plants."),
        ("F", "generator", "Generator Installation Work", "Mechanical installation support for generator packages."),
        ("G", "hvac", "Air Conditioning & Refrigeration", "ACMV and refrigeration works for commercial and industrial spaces."),
        ("H", "power-mep", "Power Plant MEP Work", "Mechanical portions of power plant MEP packages."),
    ],
    "Best for",
    ["Factories and warehouses", "Fuel and process facilities", "Hotels and commercial buildings", "Power and industrial plants"],
    "mechanical-engineering",
    [
        "Steel and plant mechanical works",
        "Industrial fabrication & install",
        "Process and piping packages",
        "Factory mechanical systems",
        "Power Plant MEP Work",
        "Equipment setting projects",
    ],
)

PAGES["civil.html"] = service_page(
    "Civil Engineering | PEMCO",
    "PEMCO civil engineering: factory and building construction, construction management, surveying, structural design, roads, and renovation.",
    "assets/images/service-civil.jpg",
    "Civil Engineering",
    "Construction delivery from survey to handover",
    "Civil packages covering factories, buildings, roads, supervision, and structural design — including turnkey contracting.",
    [
        ("A", "factory", "Factory & Building Construction", "New-build factories, offices, warehouses, and commercial buildings."),
        ("B", "cm", "Construction Management and Supervision", "On-site management and supervision for controlled project delivery."),
        ("C", "turnkey", "Turn Key Civil Work Contracting", "Single-point civil contracting across coordinated work packages."),
        ("D", "survey", "Topographic and Construction Survey", "Survey support for design, setting-out, and construction control."),
        ("E", "design", "Design and Drawings", "Civil design documentation coordinated with project requirements."),
        ("F", "structural", "Structural Design and Calculations", "Structural engineering design and calculation support."),
        ("G", "interior", "Interior Design and Decoration", "Interior fit-out and decoration for offices, hotels, and commercial spaces."),
        ("H", "reno", "Building Renovation and Maintenance", "Upgrade and maintain existing building assets."),
        ("I", "road", "Road Construction", "Road and related civil infrastructure works."),
    ],
    "Also consider",
    ["Design & Drawing outsourcing", "Quantity Surveyor Services", "Installation & Repairs for M&E", "Full renovation packages"],
    "civil-engineering",
    [
        "Factory & building construction",
        "Industrial facility delivery",
        "Commercial building works",
        "Community and school builds",
        "Warehouse and SEZ projects",
    ],
)

PAGES["design-drawing.html"] = service_page(
    "Design & Drawing Services | PEMCO",
    "PEMCO design and drawing outsourcing for international companies — electrical, mechanical, and civil documentation. Contact for quotes.",
    "assets/images/service-design.jpg",
    "Design & Drawing Services",
    "Outsourced drawings for international project teams",
    "PEMCO provides design and drawing support across electrical, mechanical, and civil scopes. International companies can contact us by email for quotations.",
    [
        ("01", "me", "Electrical / Mechanical / Civil Drawings", "Coordinated design packages aligned to the discipline you are hiring."),
        ("02", "tender", "Tender & Construction Documentation", "Drawing sets prepared for tender issue and construction coordination."),
        ("03", "structural", "Structural Design & Calculations", "Structural documentation and calculation support."),
        ("04", "interior", "Interior Design Drawings", "Interior layouts, elevations, and detailing packages."),
        ("05", "example", "Example Capability", "Sample tender drawing set available for reference on this page."),
    ],
    "Request a quote",
    [
        "Email: pemco@myanmar.com.mm",
        "Email: pemco.myanmar@gmail.com",
        "Share scope, discipline, and delivery format",
        "Ideal for consultants and overseas partners",
    ],
    "design-drawing",
    [
        "Tender drawing cover set",
        "Layout plan documentation",
        "General arrangement drawings",
        "Elevation packages",
        "Partition & detail drawings",
        "Joinery and finish documentation",
    ],
    extra="""
    <div style="margin-top:2rem" id="example">
      <h2>Example tender drawing set</h2>
      <p>Reference samples from a tender drawing package, illustrating layout, elevation, and detailing deliverables.</p>
      <div class="drawing-grid">
        <figure><img src="assets/images/drawing-01.jpg" alt="Tender drawing sample 1"><figcaption>Cover / content reference</figcaption></figure>
        <figure><img src="assets/images/drawing-02.jpg" alt="Tender drawing sample 2"><figcaption>Layout documentation</figcaption></figure>
        <figure><img src="assets/images/drawing-03.jpg" alt="Tender drawing sample 3"><figcaption>Detail package sample</figcaption></figure>
      </div>
      <p style="margin-top:1rem"><a class="btn btn-outline" href="assets/drawings/tender-drawing-set-example.pdf" target="_blank" rel="noopener">Open sample PDF</a></p>
    </div>
    """,
)

PAGES["quantity-surveyor.html"] = service_page(
    "Quantity Surveyor Services | PEMCO",
    "PEMCO quantity surveying services for measurement, costing, BOQ, and tender support.",
    "assets/images/service-qs.jpg",
    "Quantity Surveyor Services",
    "Commercial control for construction packages",
    "Our QS section supports owners and project teams with measurement, cost planning, and tender documentation.",
    [
        ("01", "measure", "Measurement & Take-off", "Quantity take-off aligned to drawings and specifications."),
        ("02", "boq", "Bill of Quantities Support", "Structured BOQ preparation for tender and contracting."),
        ("03", "cost", "Cost Estimation", "Estimate support for budgeting and package comparison."),
        ("04", "tender", "Tender Documentation Support", "Commercial documentation coordinated with design and site teams."),
    ],
    "Works well with",
    ["Design & Drawing Services", "Civil construction packages", "M&E installation scopes", "Renovation budgeting"],
    "quantity-surveyor",
    [
        "Drawing-based measurement",
        "Tender documentation support",
        "Commercial coordination",
        "BOQ preparation references",
        "Cost planning packages",
        "Project commercial support",
    ],
)

PAGES["installation-repairs.html"] = service_page(
    "Installation & Repairs | PEMCO",
    "PEMCO mechanical and electrical installation, repairs, and maintenance for industrial and commercial facilities.",
    "assets/images/service-install.jpg",
    "Installation & Repairs",
    "Mechanical & electrical installation you can hand over",
    "Installation and repairing capability covering steel, tanks, piping, machines, plumbing, generators, HVAC, power distribution, ELV, and electrical maintenance.",
    [
        ("A", "steel", "Steel Structure Fabrication & Installation", "Shop fabrication with site erection."),
        ("B", "tank", "Fuel Tank Fabrication & Installation", "Tank systems fabricated and installed."),
        ("C", "piping", "Hydrant Piping & Plumbing Systems", "Welded hydrant piping plus plumbing & sanitary installation."),
        ("D", "equipment", "Machine Setting & Generator Installation", "Equipment setting and generator package installation."),
        ("E", "hvac", "Air Conditioning & Refrigeration", "ACMV installation for comfort and process spaces."),
        ("F", "power", "Electrical Power, Lighting & Protection", "Distribution, lighting, earthing, and lightning protection."),
        ("G", "elv", "Communication & Protection Systems", "PABX, network, PA, MATV, CCTV, fire alarm."),
        ("H", "maintain", "Electrical Maintenance & Automation", "Ongoing maintenance and automation support."),
    ],
    "Typical clients",
    ["Factories and SEZ facilities", "Power and process plants", "Commercial buildings and hotels", "Port and infrastructure assets"],
    "installation-repairs",
    [
        "Port M&E installation",
        "Substation installation packages",
        "Plant mechanical install",
        "Warehouse system installation",
        "Commercial M&E fit-out",
        "Industrial commissioning support",
    ],
)

PAGES["renovation.html"] = service_page(
    "Renovation | PEMCO",
    "PEMCO building renovation, interior upgrades, and maintenance for offices, hotels, and industrial facilities.",
    "assets/images/service-reno.jpg",
    "Renovation",
    "Upgrade existing assets with coordinated trades",
    "Renovation and maintenance packages that combine civil, interior, electrical, and mechanical works for live or phased facilities.",
    [
        ("01", "building", "Building Renovation & Maintenance", "Structural and architectural upgrades for existing buildings."),
        ("02", "interior", "Interior Fit-out & Decoration", "Office, hotel, and commercial interior renovation."),
        ("03", "me", "M&E Upgrade Works", "Electrical, air-conditioning, plumbing, and ELV upgrades."),
    ],
    "Recent renovation contexts",
    ["Office renovations", "Hotel interiors", "Call centers and retail counters", "Factory and warehouse upgrades"],
    "renovation",
    [
        "Office renovation works",
        "Hotel interior upgrades",
        "Call center / commercial fit-out",
        "Interior decoration packages",
        "Building upgrade delivery",
    ],
)

PAGES["services.html"] = page(
    "Services | PEMCO Engineering",
    "Explore PEMCO services: electrical, mechanical, civil, design & drawing, quantity surveying, installation & repairs, and renovation.",
    "services",
    """
<main id="main">
  <section class="page-hero" style="--page-bg:url('assets/images/project-04.jpg')">
    <div class="container">
      <span class="eyebrow" style="color:#ffb3bd">Services</span>
      <h1>Hire by discipline or delivery need</h1>
      <p>Use the categories below to find the right PEMCO team — then open a page for detailed scope items.</p>
    </div>
  </section>
  <section class="section">
    <div class="container">
      <div class="section-head reveal">
        <span class="eyebrow">Service map</span>
        <h2>Construction &amp; engineering categories</h2>
      </div>
      <div class="service-board">
        <a class="service-card reveal" href="civil.html">
          <img src="assets/images/service-civil.jpg" alt="">
          <div>
            <h3>Civil Engineering</h3>
            <p>Factories, buildings, roads, survey, structural design, turnkey civil works.</p>
            <span class="link">View scope →</span>
          </div>
        </a>
        <a class="service-card reveal" href="electrical.html">
          <img src="assets/images/service-electrical.jpg" alt="">
          <div>
            <h3>Electrical Engineering</h3>
            <p>Power distribution, lighting, earthing, automation, ELV, generators, maintenance.</p>
            <span class="link">View scope →</span>
          </div>
        </a>
        <a class="service-card reveal" href="mechanical.html">
          <img src="assets/images/service-mechanical.jpg" alt="">
          <div>
            <h3>Mechanical Engineering</h3>
            <p>Steel, tanks, piping, HVAC, plumbing, machine setting, power plant MEP.</p>
            <span class="link">View scope →</span>
          </div>
        </a>
        <a class="service-card reveal" href="design-drawing.html">
          <img src="assets/images/service-design.jpg" alt="">
          <div>
            <h3>Design &amp; Drawing Services</h3>
            <p>Outsourcing for international companies — contact email for quotes.</p>
            <span class="link">View scope →</span>
          </div>
        </a>
        <a class="service-card reveal" href="quantity-surveyor.html">
          <img src="assets/images/service-qs.jpg" alt="">
          <div>
            <h3>Quantity Surveyor Services</h3>
            <p>Measurement, BOQ, cost estimation, and tender commercial support.</p>
            <span class="link">View scope →</span>
          </div>
        </a>
        <a class="service-card reveal" href="installation-repairs.html">
          <img src="assets/images/service-install.jpg" alt="">
          <div>
            <h3>Installation &amp; Repairs</h3>
            <p>Full mechanical &amp; electrical installation list with maintenance capability.</p>
            <span class="link">View scope →</span>
          </div>
        </a>
        <a class="service-card reveal" href="renovation.html">
          <img src="assets/images/service-reno.jpg" alt="">
          <div>
            <h3>Renovation</h3>
            <p>Building renovation, interiors, and coordinated M&amp;E upgrades.</p>
            <span class="link">View scope →</span>
          </div>
        </a>
      </div>
    </div>
  </section>
</main>
""",
)

PAGES["projects.html"] = page(
    "Projects | PEMCO Engineering",
    "Selected PEMCO projects across power, industrial, ports, commercial interiors, and social infrastructure.",
    "projects",
    """
<main id="main">
  <section class="page-hero" style="--page-bg:url('assets/images/projects/Thilawa-Subsation/230kV-Thilawa-Substation/01.jpg')">
    <div class="container">
      <span class="eyebrow" style="color:#ffb3bd">Projects</span>
      <h1>Selected works from PEMCO’s portfolio</h1>
      <p>Representative projects drawn from company profile records — demonstrating multi-discipline delivery across Myanmar.</p>
    </div>
  </section>
"""
    + clients_marquee(section_id="project-clients", heading="Clients behind the portfolio")
    + """
  <section class="section">
    <div class="container">
      <div class="project-grid">
"""
    + "\n".join(render_project_tile(p, "reveal") for p in PROJECTS_DATA)
    + """
      </div>
      <div class="cta-band reveal" style="margin-top:2rem">
        <div>
          <h2>Need a reference list for your tender?</h2>
          <p>Contact us for capability statements aligned to electrical, mechanical, or civil packages.</p>
        </div>
        <a class="btn btn-primary" href="contact.html">Request references</a>
      </div>
    </div>
  </section>
</main>
""",
)

PAGES["contact.html"] = page(
    "Contact PEMCO | Request a Quote",
    "Contact PEMCO Company Limited in Yangon for engineering, construction, and design outsourcing quotations.",
    "contact",
    """
<main id="main">
  <section class="page-hero" style="--page-bg:url('assets/images/office.jpg')">
    <div class="container">
      <span class="eyebrow" style="color:#ffb3bd">Contact</span>
      <h1>Tell us what you need built or drawn</h1>
      <p>Project owners, consultants, and international partners can reach PEMCO for construction, M&amp;E, renovation, or design outsourcing quotes.</p>
    </div>
  </section>
  <section class="section">
    <div class="container contact-grid">
      <div class="contact-card reveal">
        <h2>PEMCO Company Limited</h2>
        <div class="contact-lines">
          <div>
            <h3>Head Office</h3>
            <p>#1404, 1405, 1406, Yuzana Tower,<br>Shwe Gon Taing Junction, Bahan Township,<br>Yangon, Myanmar 11201</p>
          </div>
          <div>
            <h3>Phone</h3>
            <p>+95-1-559678<br>+95-1-559751<br>+95-1-554885<br>+95-1-558446<br>+95-9-454241563<br>+95-9-977126591</p>
          </div>
          <div>
            <h3>Email</h3>
            <p><a href="mailto:pemco@myanmar.com.mm">pemco@myanmar.com.mm</a><br>
            <a href="mailto:pemco.myanmar@gmail.com">pemco.myanmar@gmail.com</a></p>
          </div>
          <div>
            <h3>Fabrication Shop</h3>
            <p>E(12), D(14), Economic Development Zone,<br>North Dagon Township, Yangon<br>Tel: +95-1-586054</p>
          </div>
        </div>
      </div>
      <form class="contact-form reveal" action="mailto:pemco@myanmar.com.mm" method="post" enctype="text/plain">
        <label>Name
          <input name="name" type="text" required placeholder="Your name">
        </label>
        <label>Company
          <input name="company" type="text" placeholder="Company or organization">
        </label>
        <label>Email
          <input name="email" type="email" required placeholder="name@company.com">
        </label>
        <label>Service interest
          <select name="service">
            <option>Civil Engineering</option>
            <option>Electrical Engineering</option>
            <option>Mechanical Engineering</option>
            <option>Design &amp; Drawing Outsourcing</option>
            <option>Quantity Surveyor Services</option>
            <option>Installation &amp; Repairs</option>
            <option>Renovation</option>
            <option>General enquiry</option>
          </select>
        </label>
        <label>Project details
          <textarea name="message" required placeholder="Share location, scope, timeline, and any drawing requirements."></textarea>
        </label>
        <button class="btn btn-primary" type="submit">Send via email</button>
        <p class="form-note">This form opens your email client to message PEMCO. You can also write directly to pemco@myanmar.com.mm.</p>
      </form>
    </div>
  </section>
</main>
""",
)

# Redirect stubs for old URLs
REDIRECTS = {
    "our-story.html": "about.html",
    "leadership-team.html": "about.html#leadership",
    "health-safety-quality.html": "about.html",
    "building-factory-construction.html": "civil.html#factory",
    "construction-management.html": "civil.html#cm",
    "surveying-services.html": "civil.html#survey",
    "engineering-design.html": "design-drawing.html",
    "structural-engineering.html": "civil.html#structural",
    "structural-steel-work.html": "mechanical.html#steel",
    "mechanical-services.html": "mechanical.html",
    "electrical-services.html": "electrical.html",
    "elv-communication-system.html": "electrical.html#elv",
    "hvac-system.html": "mechanical.html#hvac",
    "plumbing-sanitary-system.html": "mechanical.html#plumbing",
    "power-generation.html": "electrical.html#power-plant",
    "interior-design.html": "civil.html#interior",
    "renovation-maintenance.html": "renovation.html",
    "road-construction.html": "civil.html#road",
}

def redirect_page(target):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta http-equiv="refresh" content="0; url={target}">
<link rel="canonical" href="{target}">
<title>Redirecting…</title>
<script>location.replace({target!r});</script>
</head>
<body>
<p>Redirecting to <a href="{target}">{target}</a>…</p>
</body>
</html>
"""


def main():
    for name, html in PAGES.items():
        (ROOT / name).write_text(html, encoding="utf-8")
        print("wrote", name)
    for old, new in REDIRECTS.items():
        (ROOT / old).write_text(redirect_page(new), encoding="utf-8")
        print("redirect", old, "->", new)
    (ROOT / "README.md").write_text(
        """# PEMCO Company Limited — Website

Modern static website for PEMCO (Progressive Engineer Myanmar Company).

## Run locally

```bash
python3 -m http.server 8080
```

Open http://127.0.0.1:8080/

## Structure

- `index.html` — home
- `services.html` + discipline pages — hireable categories
- `projects.html` — portfolio from company profile
- `design-drawing.html` — outsourcing + sample tender drawings
- `assets/` — CSS, JS, images, sample PDF
""",
        encoding="utf-8",
    )
    print("done")


if __name__ == "__main__":
    main()
