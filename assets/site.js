// Shared behaviour. No dependencies. Everything here is an enhancement:
// every page still works, with plain links, if this file does not run.
//   - mobile menu (the sidebar becomes a drawer)
//   - sidebar sub-menu, counts, previous/next and back-link label (from site-map.js)
//   - "On this page" contents for long articles
//   - footer year
(function () {
  'use strict';
  var root = document.documentElement;
  var body = document.body;
  var R = body.getAttribute('data-root') || '';        // path from this page to the site root ('', '../' or a full URL)
  var PAGE = body.getAttribute('data-page') || '';      // this page, relative to the site root
  var SITE = window.SITE || null;
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  function esc(s) { return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;'); }
  function $(sel, ctx) { return (ctx || document).querySelector(sel); }
  function $$(sel, ctx) { return Array.prototype.slice.call((ctx || document).querySelectorAll(sel)); }

  document.querySelectorAll('[data-year]').forEach(function (el) { el.textContent = new Date().getFullYear(); });

  /* ---------- Old links: projects.html#cricketiq now lives on its own page ---------- */
  if (SITE && PAGE === 'projects.html' && location.hash) {
    var id = location.hash.slice(1), moved = null;
    SITE.projects.forEach(function (p) {
      var slug = p.href.replace(/^projects\//, '').replace(/\.html$/, '');
      if (slug === id) moved = p.href;
    });
    if (moved) { location.replace(R + moved); return; }
  }

  /* ---------- Drawer (phones and tablets) ---------- */
  var menuBtn = $('.menu-btn');
  var sidebar = $('#sidebar');
  function setDrawer(open) {
    var was = root.classList.contains('drawer-open');
    root.classList.toggle('drawer-open', open);
    if (menuBtn) menuBtn.setAttribute('aria-expanded', String(open));
    if (open) { var f = $('#sidebar a'); if (f) f.focus(); }
    else if (was && menuBtn) menuBtn.focus({ preventScroll: true });
  }
  if (menuBtn && sidebar) {
    menuBtn.addEventListener('click', function () { setDrawer(!root.classList.contains('drawer-open')); });
    var scrim = $('.scrim'); if (scrim) scrim.addEventListener('click', function () { setDrawer(false); });
    var closeBtn = $('.side-close'); if (closeBtn) closeBtn.addEventListener('click', function () { setDrawer(false); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && root.classList.contains('drawer-open')) setDrawer(false); });
    var wide = window.matchMedia('(min-width: 901px)');
    var onWide = function (e) { if (e.matches) setDrawer(false); };
    if (wide.addEventListener) wide.addEventListener('change', onWide); else if (wide.addListener) wide.addListener(onWide);
  }

  if (!SITE) return;

  /* ---------- Where am I? ---------- */
  var project = null, note = null;
  SITE.projects.forEach(function (p) { if (p.href === PAGE) project = p; });
  SITE.notes.forEach(function (n) { if (n.href === PAGE) note = n; });
  var groupTitle = {};
  SITE.groups.forEach(function (g) { groupTitle[g.id] = g.title; });

  /* ---------- Counts ---------- */
  $$('[data-count]').forEach(function (el) {
    var k = el.getAttribute('data-count');
    el.textContent = k === 'projects' ? SITE.projects.length : k === 'notes' ? SITE.notes.length : '';
  });

  /* ---------- Contents for long articles ---------- */
  var heads = $$('main article .prose h2');
  heads.forEach(function (h, i) { if (!h.id) h.id = 'section-' + (i + 1); });
  if (heads.length < 3) heads = [];
  function tocItems() {
    return heads.map(function (h) { return '<li><button type="button" data-goto="' + h.id + '">' + esc(h.textContent) + '</button></li>'; }).join('');
  }

  /* ---------- Sidebar sub-menu ---------- */
  var sub = $('[data-subnav]');
  if (sub) {
    var kind = sub.getAttribute('data-subnav');
    var child = function (href, label, extra) {
      var cur = href === PAGE;
      return '<li><a href="' + R + href + '"' + (cur ? ' aria-current="page"' : '') + '>' + esc(label) + (extra || '') + '</a>' +
        (cur && heads.length ? '<ol class="toc" aria-label="On this page">' + tocItems() + '</ol>' : '') + '</li>';
    };
    var html = '';
    if (kind === 'projects') {
      html = '<ul>' + SITE.projects.map(function (p) { return child(p.href, p.title, '<span class="stat">' + esc(p.status) + '</span>'); }).join('') + '</ul>';
    } else if (kind === 'notes') {
      html = '<ul>' + SITE.groups.map(function (g) {
        var items = SITE.notes.filter(function (n) { return n.group === g.id && !n.ext; });
        if (!items.length) return '';
        return '<li class="grp" aria-hidden="true">' + esc(g.title) + '</li>' + items.map(function (n) { return child(n.href, n.title); }).join('');
      }).join('') + '</ul>';
    }
    sub.innerHTML = html;
    var cur = $('a[aria-current="page"]', sub);
    if (cur && cur.scrollIntoView) cur.scrollIntoView({ block: 'nearest' });
  }

  /* ---------- Mobile contents box + scroll tracking ---------- */
  var mbox = $('[data-toc-m]');
  if (mbox && heads.length) mbox.innerHTML = '<details class="toc-m"><summary>On this page</summary><ol class="toc">' + tocItems() + '</ol></details>';
  $$('[data-goto]').forEach(function (b) {
    b.addEventListener('click', function () {
      var t = document.getElementById(b.getAttribute('data-goto'));
      if (!t) return;
      setDrawer(false);
      t.setAttribute('tabindex', '-1');
      t.scrollIntoView({ behavior: reduce ? 'auto' : 'smooth', block: 'start' });
      t.focus({ preventScroll: true });
    });
  });
  var queued = false;
  function spy() {
    queued = false;
    if (!heads.length) return;
    var line = window.innerHeight * 0.3, current = heads[0].id;
    heads.forEach(function (h) { if (h.getBoundingClientRect().top <= line) current = h.id; });
    $$('[data-goto]').forEach(function (b) {
      var on = b.getAttribute('data-goto') === current;
      b.classList.toggle('here', on);
      if (on) b.setAttribute('aria-current', 'location'); else b.removeAttribute('aria-current');
    });
  }
  if (heads.length) {
    window.addEventListener('scroll', function () { if (!queued) { queued = true; requestAnimationFrame(spy); } }, { passive: true });
    spy();
  }

  /* ---------- Previous / next, within the same topic ---------- */
  var pager = $('[data-pager]');
  if (pager) {
    var list, label = '';
    if (project) { list = SITE.projects; label = ' project'; }
    else if (note) {
      list = SITE.notes.filter(function (n) { return n.group === note.group && !n.ext; });
      label = ' in ' + groupTitle[note.group];
    }
    if (list) {
      var i = -1; list.forEach(function (x, k) { if (x.href === PAGE) i = k; });
      var out = '';
      if (i > 0) out += '<a class="prev" href="' + R + list[i - 1].href + '"><small>Previous' + esc(label) + '</small>' + esc(list[i - 1].title) + '</a>';
      if (i > -1 && i < list.length - 1) out += '<a class="next" href="' + R + list[i + 1].href + '"><small>Next' + esc(label) + '</small>' + esc(list[i + 1].title) + '</a>';
      pager.innerHTML = out; pager.hidden = !out;
    }
  }

  /* ---------- "← Back to …" names the page you actually came from ---------- */
  var back = $('.backlink[data-back]');
  if (back && document.referrer) {
    try {
      var baseUrl = new URL(R || './', location.href).href;
      var ref = new URL(document.referrer);
      if (ref.href.indexOf(baseUrl) === 0) {
        var rel = ref.href.slice(baseUrl.length).split('#')[0].split('?')[0] || 'index.html';
        var title = SITE.pages[rel];
        SITE.projects.concat(SITE.notes).forEach(function (x) { if (x.href === rel) title = x.title; });
        if (title && rel !== PAGE) {
          back.setAttribute('href', R + rel);
          back.textContent = '← Back to ' + title;
        }
      }
    } catch (e) { /* keep the default link */ }
  }
})();
