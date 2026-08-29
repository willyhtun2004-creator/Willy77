(function () {
  const header = document.querySelector(".site-header");
  const menuToggle = document.querySelector(".menu-toggle");
  const navLinks = document.querySelector(".nav-links");
  const dropdownTriggers = document.querySelectorAll("[data-dropdown]");
  const searchOpenBtns = document.querySelectorAll("[data-search-open]");
  const searchOverlay = document.querySelector(".search-overlay");
  const searchInput = document.querySelector("#site-search");
  const searchResults = document.querySelector("#search-results");
  const searchClose = document.querySelector("[data-search-close]");

  function onScroll() {
    if (!header) return;
    header.classList.toggle("is-scrolled", window.scrollY > 8);
  }

  function closeDropdowns() {
    dropdownTriggers.forEach((btn) => {
      btn.setAttribute("aria-expanded", "false");
      btn.parentElement.classList.remove("has-open");
      const panel = btn.parentElement.querySelector(".dropdown, .mega");
      if (panel) panel.classList.remove("open");
    });
  }

  dropdownTriggers.forEach((btn) => {
    btn.addEventListener("click", (e) => {
      e.preventDefault();
      const parent = btn.parentElement;
      const panel = parent.querySelector(".dropdown, .mega");
      const willOpen = !panel.classList.contains("open");
      closeDropdowns();
      if (willOpen) {
        panel.classList.add("open");
        parent.classList.add("has-open");
        btn.setAttribute("aria-expanded", "true");
      }
    });
  });

  document.addEventListener("click", (e) => {
    if (!e.target.closest(".nav-links")) closeDropdowns();
  });

  if (menuToggle && navLinks) {
    menuToggle.addEventListener("click", () => {
      const open = navLinks.classList.toggle("is-open");
      menuToggle.setAttribute("aria-expanded", open ? "true" : "false");
      if (!open) closeDropdowns();
    });
  }

  function openSearch() {
    if (!searchOverlay) return;
    searchOverlay.classList.add("open");
    searchOverlay.setAttribute("aria-hidden", "false");
    document.body.style.overflow = "hidden";
    setTimeout(() => searchInput && searchInput.focus(), 30);
    renderSearch(searchInput ? searchInput.value : "");
  }

  function closeSearch() {
    if (!searchOverlay) return;
    searchOverlay.classList.remove("open");
    searchOverlay.setAttribute("aria-hidden", "true");
    document.body.style.overflow = "";
  }

  searchOpenBtns.forEach((btn) => btn.addEventListener("click", openSearch));
  if (searchClose) searchClose.addEventListener("click", closeSearch);
  if (searchOverlay) {
    searchOverlay.addEventListener("click", (e) => {
      if (e.target === searchOverlay) closeSearch();
    });
  }

  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") {
      closeSearch();
      closeDropdowns();
    }
    if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === "k") {
      e.preventDefault();
      openSearch();
    }
  });

  function highlight(text, query) {
    if (!query) return text;
    const safe = query.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
    return text.replace(new RegExp(`(${safe})`, "ig"), "<em>$1</em>");
  }

  function renderSearch(query) {
    if (!searchResults) return;
    const q = (query || "").trim().toLowerCase();
    const data = window.PEMCO_SEARCH || [];

    if (!q) {
      searchResults.innerHTML =
        '<p class="search-hint">Search services, projects, design outsourcing, or contact details.</p>';
      return;
    }

    const matches = data
      .map((item) => {
        const hay = `${item.title} ${item.keywords} ${item.excerpt}`.toLowerCase();
        let score = 0;
        q.split(/\s+/).forEach((part) => {
          if (hay.includes(part)) score += part.length;
          if (item.title.toLowerCase().includes(part)) score += 8;
        });
        return { item, score };
      })
      .filter((m) => m.score > 0)
      .sort((a, b) => b.score - a.score)
      .slice(0, 10);

    if (!matches.length) {
      searchResults.innerHTML =
        '<p class="search-empty">No matches found. Try “electrical”, “tender drawing”, or “Thilawa”.</p>';
      return;
    }

    searchResults.innerHTML = matches
      .map(
        ({ item }) => `
      <a class="search-item" href="${item.url}">
        <strong>${highlight(item.title, q)}</strong>
        <span>${highlight(item.excerpt, q)}</span>
      </a>`
      )
      .join("");
  }

  if (searchInput) {
    searchInput.addEventListener("input", () => renderSearch(searchInput.value));
  }

  // Auto-tag key sections and components for smooth emergence
  document
    .querySelectorAll(
      ".section-head, .capability, .project-tile, .leader-card, .service-card, .drawing-grid figure, .photo-gallery figure, .stats > div, .split-media, .split-copy, .content-block, .side-panel, .cta-band, .clients-section, .footer-grid > div"
    )
    .forEach((el) => {
      if (!el.classList.contains("reveal")) {
        el.classList.add("reveal");
      }
    });

  const revealEls = document.querySelectorAll(".reveal");
  if ("IntersectionObserver" in window && revealEls.length) {
    const io = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add("is-visible");
            io.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.06, rootMargin: "0px 0px -30px 0px" }
    );
    revealEls.forEach((el) => io.observe(el));
  } else {
    revealEls.forEach((el) => el.classList.add("is-visible"));
  }

  onScroll();
  window.addEventListener("scroll", onScroll, { passive: true });

  document.querySelectorAll("[data-project-carousel]").forEach((carousel) => {
    const track = carousel.querySelector(".project-carousel-track");
    const slides = carousel.querySelectorAll(".project-carousel-slide");
    const prevBtn = carousel.querySelector("[data-carousel-prev]");
    const nextBtn = carousel.querySelector("[data-carousel-next]");
    const dotsHost = carousel.querySelector("[data-carousel-dots]");
    if (!track || !slides.length) return;

    let index = 0;
    let touchStartX = 0;

    if (dotsHost) {
      dotsHost.innerHTML = "";
      slides.forEach((_, i) => {
        const dot = document.createElement("button");
        dot.type = "button";
        dot.className = "project-carousel-dot" + (i === 0 ? " is-active" : "");
        dot.setAttribute("aria-label", `Show projects slide ${i + 1}`);
        dot.addEventListener("click", () => {
          goTo(i);
        });
        dotsHost.appendChild(dot);
      });
    }

    const dots = dotsHost ? dotsHost.querySelectorAll(".project-carousel-dot") : [];

    function goTo(nextIndex) {
      if (nextIndex >= slides.length) {
        index = 0;
      } else if (nextIndex < 0) {
        index = slides.length - 1;
      } else {
        index = nextIndex;
      }
      track.style.transform = `translateX(-${index * 100}%)`;
      dots.forEach((dot, i) => dot.classList.toggle("is-active", i === index));
      if (prevBtn) prevBtn.disabled = false;
      if (nextBtn) nextBtn.disabled = false;
    }

    if (prevBtn) {
      prevBtn.addEventListener("click", () => {
        goTo(index - 1);
      });
    }
    if (nextBtn) {
      nextBtn.addEventListener("click", () => {
        goTo(index + 1);
      });
    }

    carousel.addEventListener(
      "touchstart",
      (e) => {
        touchStartX = e.changedTouches[0].clientX;
      },
      { passive: true }
    );

    carousel.addEventListener(
      "touchend",
      (e) => {
        const delta = e.changedTouches[0].clientX - touchStartX;
        if (Math.abs(delta) >= 40) {
          goTo(delta < 0 ? index + 1 : index - 1);
        }
      },
      { passive: true }
    );

    goTo(0);
  });

  // Project Photo Gallery Lightbox Modal
  const projectModal = document.getElementById("project-modal");
  const modalTitle = document.getElementById("project-modal-title");
  const modalDesc = document.getElementById("project-modal-desc");
  const modalCounter = document.getElementById("project-modal-counter");
  const modalImg = document.getElementById("project-modal-img");
  const modalStage = document.getElementById("project-modal-stage");
  const modalPrev = document.getElementById("project-modal-prev");
  const modalNext = document.getElementById("project-modal-next");
  const modalThumbs = document.getElementById("project-modal-thumbs");
  const modalCloseBtns = document.querySelectorAll("[data-modal-close]");

  let currentProjectImages = [];
  let currentImageIndex = 0;
  let modalTouchStartX = 0;

  function openProjectGallery(tile) {
    if (!projectModal) return;
    try {
      const rawImages = tile.getAttribute("data-gallery-images");
      currentProjectImages = rawImages ? JSON.parse(rawImages) : [];
    } catch (e) {
      currentProjectImages = [];
    }

    if (!currentProjectImages.length) {
      const img = tile.querySelector("img");
      if (img && img.src) currentProjectImages = [img.src];
    }

    const title = tile.getAttribute("data-gallery-title") || (tile.querySelector("h3") ? tile.querySelector("h3").textContent : "Project Gallery");
    const desc = tile.getAttribute("data-gallery-desc") || (tile.querySelector("p") ? tile.querySelector("p").textContent : "");

    if (modalTitle) modalTitle.textContent = title;
    if (modalDesc) modalDesc.textContent = desc;

    renderThumbs();
    showProjectImage(0);

    projectModal.classList.add("is-open");
    projectModal.setAttribute("aria-hidden", "false");
    document.body.style.overflow = "hidden";
  }

  function closeProjectGallery() {
    if (!projectModal) return;
    projectModal.classList.remove("is-open");
    projectModal.setAttribute("aria-hidden", "true");
    document.body.style.overflow = "";
  }

  function showProjectImage(index) {
    if (!currentProjectImages.length) return;
    if (index >= currentProjectImages.length) {
      currentImageIndex = 0;
    } else if (index < 0) {
      currentImageIndex = currentProjectImages.length - 1;
    } else {
      currentImageIndex = index;
    }

    if (modalImg) {
      modalImg.style.opacity = "0.4";
      modalImg.src = currentProjectImages[currentImageIndex];
      modalImg.alt = (modalTitle ? modalTitle.textContent : "Project") + " photo " + (currentImageIndex + 1);
      modalImg.onload = () => {
        modalImg.style.opacity = "1";
      };
    }

    if (modalCounter) {
      modalCounter.textContent = (currentImageIndex + 1) + " / " + currentProjectImages.length;
    }

    if (modalThumbs) {
      const thumbBtns = modalThumbs.querySelectorAll(".project-modal-thumb");
      thumbBtns.forEach((btn, i) => {
        const isActive = i === currentImageIndex;
        btn.classList.toggle("is-active", isActive);
        if (isActive) {
          btn.scrollIntoView({ behavior: "smooth", block: "nearest", inline: "center" });
        }
      });
    }

    const single = currentProjectImages.length <= 1;
    if (modalPrev) modalPrev.style.display = single ? "none" : "";
    if (modalNext) modalNext.style.display = single ? "none" : "";
  }

  function renderThumbs() {
    if (!modalThumbs) return;
    modalThumbs.innerHTML = "";
    if (currentProjectImages.length <= 1) {
      if (modalThumbs.parentElement) modalThumbs.parentElement.style.display = "none";
      return;
    }
    if (modalThumbs.parentElement) modalThumbs.parentElement.style.display = "";
    currentProjectImages.forEach((src, i) => {
      const btn = document.createElement("button");
      btn.type = "button";
      btn.className = "project-modal-thumb" + (i === 0 ? " is-active" : "");
      btn.setAttribute("aria-label", "View photo " + (i + 1));
      const thumbImg = document.createElement("img");
      thumbImg.src = src;
      thumbImg.alt = "Thumbnail " + (i + 1);
      thumbImg.loading = "lazy";
      btn.appendChild(thumbImg);
      btn.addEventListener("click", () => showProjectImage(i));
      modalThumbs.appendChild(btn);
    });
  }

  if (modalPrev) {
    modalPrev.addEventListener("click", (e) => {
      e.stopPropagation();
      showProjectImage(currentImageIndex - 1);
    });
  }

  if (modalNext) {
    modalNext.addEventListener("click", (e) => {
      e.stopPropagation();
      showProjectImage(currentImageIndex + 1);
    });
  }

  modalCloseBtns.forEach((btn) => btn.addEventListener("click", closeProjectGallery));

  document.addEventListener("keydown", (e) => {
    if (!projectModal || !projectModal.classList.contains("is-open")) return;
    if (e.key === "Escape") {
      closeProjectGallery();
    } else if (e.key === "ArrowLeft") {
      showProjectImage(currentImageIndex - 1);
    } else if (e.key === "ArrowRight") {
      showProjectImage(currentImageIndex + 1);
    }
  });

  if (modalStage) {
    modalStage.addEventListener(
      "touchstart",
      (e) => {
        modalTouchStartX = e.changedTouches[0].clientX;
      },
      { passive: true }
    );
    modalStage.addEventListener(
      "touchend",
      (e) => {
        const delta = e.changedTouches[0].clientX - modalTouchStartX;
        if (Math.abs(delta) >= 40) {
          showProjectImage(delta < 0 ? currentImageIndex + 1 : currentImageIndex - 1);
        }
      },
      { passive: true }
    );
  }

  // Bind project tiles (skip inert placeholders such as the Home "More" tile)
  document.querySelectorAll(".project-tile").forEach((tile) => {
    if (tile.matches("a, .project-tile-more")) return;
    tile.addEventListener("click", () => openProjectGallery(tile));
    tile.addEventListener("keydown", (e) => {
      if (e.key === "Enter" || e.key === " ") {
        e.preventDefault();
        openProjectGallery(tile);
      }
    });
  });

  // Contact form → send to pemco.myanmar@gmail.com via FormSubmit
  const contactForm = document.querySelector("#contact-form");
  if (contactForm) {
    const submitBtn = document.querySelector("#contact-submit");
    const statusEl = document.querySelector("#contact-form-status");
    contactForm.addEventListener("submit", async (e) => {
      e.preventDefault();
      if (!statusEl || !submitBtn) return;

      statusEl.hidden = false;
      statusEl.className = "form-status";
      statusEl.textContent = "Sending…";
      submitBtn.disabled = true;

      const data = new FormData(contactForm);
      const payload = Object.fromEntries(data.entries());

      try {
        const res = await fetch("https://formsubmit.co/ajax/pemco.myanmar@gmail.com", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Accept: "application/json",
          },
          body: JSON.stringify(payload),
        });
        const result = await res.json().catch(() => ({}));
        if (!res.ok) throw new Error(result.message || "Send failed");

        statusEl.className = "form-status is-success";
        statusEl.textContent = "Message sent. PEMCO will reply to your email shortly.";
        contactForm.reset();
      } catch (err) {
        statusEl.className = "form-status is-error";
        statusEl.textContent =
          "Could not send right now. Please email pemco.myanmar@gmail.com directly.";
      } finally {
        submitBtn.disabled = false;
      }
    });
  }
})();
