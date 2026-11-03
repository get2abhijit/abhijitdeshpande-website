// Shared behaviour: mobile navigation and footer year. No dependencies.
(function () {
  var toggle = document.querySelector('.menu-toggle');
  var nav = document.getElementById('site-nav');

  if (toggle && nav) {
    var setOpen = function (open, returnFocus) {
      nav.classList.toggle('open', open);
      toggle.setAttribute('aria-expanded', String(open));
      if (!open && returnFocus) toggle.focus();
    };

    toggle.addEventListener('click', function () {
      setOpen(toggle.getAttribute('aria-expanded') !== 'true');
    });

    // Close with Escape and return focus to the button.
    document.addEventListener('keydown', function (event) {
      if (event.key === 'Escape' && nav.classList.contains('open')) setOpen(false, true);
    });

    // Close after choosing a link or clicking outside the menu.
    document.addEventListener('click', function (event) {
      if (!nav.classList.contains('open')) return;
      if (event.target.closest('#site-nav a') || (!nav.contains(event.target) && !toggle.contains(event.target))) {
        setOpen(false);
      }
    });

    // Reset when the viewport grows past the mobile breakpoint.
    var desktop = window.matchMedia('(min-width: 701px)');
    var onChange = function (e) { if (e.matches) setOpen(false); };
    if (desktop.addEventListener) desktop.addEventListener('change', onChange);
    else if (desktop.addListener) desktop.addListener(onChange);
  }

  document.querySelectorAll('[data-year]').forEach(function (el) {
    el.textContent = new Date().getFullYear();
  });
})();
