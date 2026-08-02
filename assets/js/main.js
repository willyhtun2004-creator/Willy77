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
      { threshold: 0.14 }
    );
    revealEls.forEach((el) => io.observe(el));
  } else {
    revealEls.forEach((el) => el.classList.add("is-visible"));
  }

  onScroll();
  window.addEventListener("scroll", onScroll, { passive: true });
})();
