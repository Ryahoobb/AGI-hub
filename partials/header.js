/**
 * AGI HUB shared header loader.
 * Fetches partials/header.html and injects it into #site-header-mount.
 * Adds .active class to the current page nav link.
 * Self-locates base path from its own script src.
 */
(function () {
  var currentScript = document.currentScript;
  if (!currentScript) {
    var scripts = document.getElementsByTagName('script');
    for (var i = scripts.length - 1; i >= 0; i--) {
      if (scripts[i].src && scripts[i].src.indexOf('header.js') !== -1) {
        currentScript = scripts[i];
        break;
      }
    }
  }
  if (!currentScript) return;

  // partials/header.js → strip filename → partials/ → strip partials/ → site base
  var scriptUrl = currentScript.src;
  var partialsBase = scriptUrl.substring(0, scriptUrl.lastIndexOf('/') + 1);
  var siteBase = partialsBase.replace(/partials\/$/, '');

  // Determine current page identifier for active state
  var path = location.pathname.replace(/\/$/, '');
  var fileName = path.substring(path.lastIndexOf('/') + 1).replace(/\.html$/, '');
  if (!fileName || path.endsWith('/AGI-hub') || path === '') fileName = 'index';
  // Article pages all count as "articles"
  if (location.pathname.indexOf('/articles/') !== -1) fileName = 'articles';

  fetch(partialsBase + 'header.html')
    .then(function (r) {
      if (!r.ok) throw new Error('header.html fetch failed: ' + r.status);
      return r.text();
    })
    .then(function (html) {
      html = html.replace(/\{\{base\}\}/g, siteBase);
      var mount = document.getElementById('site-header-mount');
      if (!mount) return;
      var wrapper = document.createElement('div');
      wrapper.innerHTML = html;
      var headerEl = wrapper.firstElementChild;
      mount.parentNode.replaceChild(headerEl, mount);

      // Mark active link
      var links = headerEl.querySelectorAll('[data-page]');
      for (var j = 0; j < links.length; j++) {
        if (links[j].getAttribute('data-page') === fileName) {
          links[j].classList.add('active');
        }
      }

      // Initialize Google Translate widget if the function exists
      if (typeof googleTranslateElementInit === 'function') {
        try { googleTranslateElementInit(); } catch (e) { /* noop */ }
      }
    })
    .catch(function (err) {
      console.warn('[AGI HUB header] ' + err.message);
    });
})();
