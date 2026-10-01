(() => {
  'use strict';

  const pagePrefix = window.location.pathname.includes('/pages/') ? '../' : '';

  // Age notice: the site remains readable without JavaScript; this only controls the UI layer.
  const ageGate = document.querySelector('.age-gate');
  const ageDenied = document.querySelector('.age-denied');
  const acceptAge = document.querySelector('[data-age-yes]');
  const declineAge = document.querySelector('[data-age-no]');
  const mainContent = document.querySelector('main');
  const ageStorageKey = 'vapsoloes-age-confirmed';

  const focusableSelector = 'a[href], button:not([disabled]), summary, input, select, textarea, [tabindex]:not([tabindex="-1"])';
  const focusFirstIn = (container) => {
    container?.querySelector(focusableSelector)?.focus();
  };
  const hideAgeGate = () => {
    if (ageGate) ageGate.hidden = true;
  };

  try {
    if (window.localStorage.getItem(ageStorageKey) === 'true') hideAgeGate();
  } catch {
    // Storage can be unavailable in private browsing; the notice still works for this visit.
  }
  if (ageGate && !ageGate.hidden) focusFirstIn(ageGate);

  acceptAge?.addEventListener('click', () => {
    try {
      window.localStorage.setItem(ageStorageKey, 'true');
    } catch {
      // No persistent storage available.
    }
    hideAgeGate();
    mainContent?.focus();
  });

  declineAge?.addEventListener('click', () => {
    hideAgeGate();
    if (ageDenied) {
      ageDenied.hidden = false;
      focusFirstIn(ageDenied);
    }
  });

  // Keep keyboard focus inside the active age dialog until the visitor chooses an action.
  document.addEventListener('keydown', (event) => {
    if (event.key !== 'Tab') return;
    const activeDialog = ageDenied && !ageDenied.hidden
      ? ageDenied
      : (ageGate && !ageGate.hidden ? ageGate : null);
    if (!activeDialog) return;
    const focusable = [...activeDialog.querySelectorAll(focusableSelector)];
    if (!focusable.length) return;
    const first = focusable[0];
    const last = focusable[focusable.length - 1];
    if (!activeDialog.contains(document.activeElement)) {
      event.preventDefault();
      (event.shiftKey ? last : first).focus();
      return;
    }
    if (event.shiftKey && document.activeElement === first) {
      event.preventDefault();
      last.focus();
    } else if (!event.shiftKey && document.activeElement === last) {
      event.preventDefault();
      first.focus();
    }
  });

  // Mobile navigation.
  const menuButton = document.querySelector('.menu-button');
  const mainNavigation = document.querySelector('.nav-links');
  const closeMenu = () => {
    if (!mainNavigation || !menuButton) return;
    mainNavigation.classList.remove('open');
    menuButton.setAttribute('aria-expanded', 'false');
  };

  menuButton?.addEventListener('click', () => {
    if (!mainNavigation) return;
    const isOpen = mainNavigation.classList.toggle('open');
    menuButton.setAttribute('aria-expanded', String(isOpen));
  });

  mainNavigation?.querySelectorAll('a').forEach((link) => {
    link.addEventListener('click', closeMenu);
  });

  document.addEventListener('click', (event) => {
    if (!mainNavigation?.classList.contains('open')) return;
    const target = event.target;
    if (target instanceof Node && !mainNavigation.contains(target) && !menuButton?.contains(target)) {
      closeMenu();
    }
  });

  // Product thumbnails are progressively enhanced here; the product cards keep their text links in HTML.
  const productImages = {
    'SIXER 180K': 'images/products/vapsolo-sixer-180k.webp',
    'Master 70K': 'images/products/vapsolo-master-70k.webp',
    'Twins 20K': 'images/products/vapsolo-twins-20k.webp',
    'Mars 50K': 'images/products/vapsolo-mars-50k.webp',
    'Quads 80K': 'images/products/vapsolo-quads-80k.webp',
    'Super 15K': 'images/products/vapsolo-super-15k.webp',
    'King Pro 65K': 'images/products/vapsolo-king-pro-65k.webp',
    'Twins Pro 50K': 'images/products/vapsolo-twins-pro-50k.webp',
    'Triple Pro 60K': 'images/products/vapsolo-triple-pro-60k.webp'
  };

  document.querySelectorAll('.product-card').forEach((card) => {
    const visual = card.querySelector('.product-visual');
    const title = card.querySelector('h3');
    if (!visual || !title || visual.querySelector('img')) return;
    const productName = title.textContent.trim().replace(/^VapSolo\s+/i, '');
    const imagePath = productImages[productName];
    if (!imagePath) return;

    const image = document.createElement('img');
    image.src = `${pagePrefix}${imagePath}`;
    image.alt = title.textContent.trim();
    image.width = 1024;
    image.height = 1024;
    image.loading = 'lazy';
    image.decoding = 'async';
    visual.append(image);
  });

  // Product pages retired from the catalogue retain their destination only when such links are present.
  const retiredProductPages = {
    'vapsolo-king-pro-40k.html': 'vapsolo-king-pro-65k.html'
  };
  document.querySelectorAll('a[href]').forEach((link) => {
    const destination = retiredProductPages[link.getAttribute('href')?.split('/').pop()];
    if (destination) link.setAttribute('href', `${pagePrefix}pages/${destination}`.replace('pages/pages/', 'pages/'));
  });
})();
