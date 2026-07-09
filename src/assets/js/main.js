document.addEventListener("DOMContentLoaded", () => {
  // Mobile menu toggle
  const menuToggle = document.querySelector("[data-menu-toggle]");
  const siteNav = document.querySelector("[data-site-nav]");

  if (menuToggle && siteNav) {
    menuToggle.addEventListener("click", () => {
      const isOpen = siteNav.classList.toggle("is-open");
      menuToggle.setAttribute("aria-label", isOpen ? "Close navigation" : "Open navigation");
    });
  }

  // Live filtering on Archive page
  const filterInput = document.querySelector("[data-filter-input]");
  const filterItems = document.querySelectorAll("[data-filter-item]");

  function runFilter(query) {
    query = query.trim().toLowerCase();
    filterItems.forEach((item) => {
      const haystack = item.dataset.filterItem.toLowerCase();
      item.classList.toggle("is-hidden", query.length > 0 && !haystack.includes(query));
    });
  }

  if (filterInput && filterItems.length) {
    filterInput.addEventListener("input", () => {
      runFilter(filterInput.value);
    });

    // Check for query parameter on page load (e.g. ?q=disney)
    const urlParams = new URLSearchParams(window.location.search);
    const initialQuery = urlParams.get("q");
    if (initialQuery) {
      filterInput.value = initialQuery;
      runFilter(initialQuery);
    }
  }

  // Home Page search redirection
  const heroSearchInput = document.querySelector("[data-hero-search-input]");
  const heroSearchBtn = document.querySelector("[data-hero-search-btn]");

  function doHeroSearch() {
    if (heroSearchInput) {
      const query = heroSearchInput.value.trim();
      if (query) {
        window.location.href = `/maps/?q=${encodeURIComponent(query)}`;
      } else {
        window.location.href = "/maps/";
      }
    }
  }

  if (heroSearchInput && heroSearchBtn) {
    heroSearchBtn.addEventListener("click", doHeroSearch);
    heroSearchInput.addEventListener("keydown", (e) => {
      if (e.key === "Enter") {
        doHeroSearch();
      }
    });
  }

  // Hero showcase year switcher
  const yearSwitcher = document.querySelector("[data-hero-year-switcher]");
  const heroMapImage = document.getElementById("hero-map-image");

  if (yearSwitcher && heroMapImage) {
    const yearLinks = yearSwitcher.querySelectorAll("a");
    yearLinks.forEach((link) => {
      link.addEventListener("click", (e) => {
        e.preventDefault();
        
        // Remove active class from all links
        yearLinks.forEach((l) => l.classList.remove("is-selected"));
        
        // Add active class to clicked link
        link.classList.add("is-selected");
        
        // Update image source and alt text
        const src = link.dataset.src;
        const alt = link.dataset.alt;
        if (src) heroMapImage.src = src;
        if (alt) heroMapImage.alt = alt;
      });
    });
  }
});
