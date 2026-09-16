#!/usr/bin/env python3
"""Injects the shared site-header (CSS link + header markup + JS include) into
a list of HTML files. Idempotent: skips any file that already links
/css/site-header.css. Used to roll out the header built for index.html /
curriculum/index.html to the rest of the hub/index pages.
"""
import sys

HEADER_HTML = '''<header class="site-header">
  <div class="site-header-inner">
    <a href="/index.html" class="site-logo">\U0001F393 Teachings<span class="site-logo-dot">.ai</span></a>
    <nav class="site-nav" aria-label="Primary">
      <a href="/ages/index.html">By Age</a>
      <a href="/worksheets/index.html">Worksheets</a>
      <a href="/reading/index.html">Reading</a>
      <a href="/parents/index.html">Parents</a>
      <a href="/teachers/index.html">Teachers</a>
    </nav>
    <div class="site-header-cta">
      <a href="/games.html" class="site-btn site-btn-primary">\U0001F3AE Play Games</a>
      <button class="site-hamburger" id="siteHamburger" aria-label="Open menu" aria-expanded="false">
        <span></span><span></span><span></span>
      </button>
    </div>
  </div>
  <nav class="site-mobile-nav" id="siteMobileNav" aria-label="Mobile">
    <a href="/games.html" class="site-mobile-primary">\U0001F3AE Play Games</a>
    <a href="/ages/index.html">By Age</a>
    <a href="/worksheets/index.html">Worksheets Library</a>
    <a href="/reading/index.html">Reading Library</a>
    <a href="/math/index.html">Math Activities</a>
    <a href="/science/index.html">Science Activities</a>
    <a href="/coding/index.html">Coding for Kids</a>
    <a href="/curriculum/index.html">Homeschool Curriculum</a>
    <a href="/parents/index.html">For Parents</a>
    <a href="/teachers/index.html">For Teachers</a>
  </nav>
</header>

'''

CSS_LINK = '<link rel="stylesheet" href="/css/site-header.css">'
JS_TAG = '  <script src="/js/site-header.js" defer></script>\n'


def inject(path):
    with open(path, encoding='utf-8') as f:
        content = f.read()

    if 'site-header.css' in content:
        return 'skipped (already has header)'

    if '</head>' not in content or '<body>' not in content or '</body>' not in content:
        return 'SKIPPED (missing </head>, <body>, or </body> — needs manual review)'

    # 1) CSS link before </head>
    content = content.replace('</head>', f'  {CSS_LINK}\n</head>', 1)

    # 2) Header markup right after <body>
    content = content.replace('<body>', '<body>\n\n' + HEADER_HTML, 1)

    # 3) JS include right before </body>
    content = content.replace('</body>', JS_TAG + '</body>', 1)

    with open(path, 'w', encoding='utf-8', newline='') as f:
        f.write(content)

    return 'injected'


if __name__ == '__main__':
    files = sys.argv[1:]
    if not files:
        print('Usage: inject_site_header.py <file1.html> <file2.html> ...')
        sys.exit(1)
    for f in files:
        try:
            result = inject(f)
            print(f'{f}: {result}')
        except Exception as e:
            print(f'{f}: ERROR - {e}')
