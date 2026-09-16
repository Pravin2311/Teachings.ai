// Shared site header behavior: mobile menu toggle + active-link highlighting.
(function () {
  var toggle = document.getElementById('siteHamburger');
  var mobileNav = document.getElementById('siteMobileNav');
  if (toggle && mobileNav) {
    toggle.addEventListener('click', function () {
      var isOpen = mobileNav.classList.toggle('site-open');
      toggle.classList.toggle('site-open', isOpen);
      toggle.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
    });
  }

  var path = window.location.pathname.replace(/\/index\.html$/, '/');
  document.querySelectorAll('.site-nav a, .site-mobile-nav a').forEach(function (link) {
    var linkPath = link.getAttribute('href');
    if (!linkPath) return;
    linkPath = linkPath.replace(/\/index\.html$/, '/');
    if (linkPath === path) {
      link.classList.add('site-nav-active');
    }
  });
})();
