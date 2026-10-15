import glob

html_files = glob.glob('*.html')
print('Found html files:', html_files)

for f in html_files:
    with open(f, 'r', encoding='utf-8') as fp:
        content = fp.read()
    
    # fix css paths
    content = content.replace('/frontend/src/css/style.css', 'style.css')
    content = content.replace('/frontend/src/css/rtl.css', 'rtl.css')
    # fix js paths
    content = content.replace('/frontend/src/js/i18n.js', 'i18n.js')
    content = content.replace('/frontend/src/js/api.js', 'api.js')
    content = content.replace('/frontend/src/js/app.js', 'app.js')
    # fix logo
    content = content.replace('/images/logo.jpg', 'images/logo.jpg')
    content = content.replace('/public/images/logo.jpg', 'images/logo.jpg')
    
    # fix root page links
    for p in ['index.html', 'about.html', 'history.html', 'leadership.html', 'news-events.html', 'professionals.html', 'membership.html', 'verify.html', 'contact.html', 'admin.html']:
        content = content.replace(f'href="/{p}"', f'href="{p}"')
        content = content.replace(f'href="/{p}#', f'href="{p}#')
        content = content.replace(f'href="/{p}?', f'href="{p}?')

    with open(f, 'w', encoding='utf-8') as fp:
        fp.write(content)

print('All HTML files normalized for GitHub Pages and relative paths!')
