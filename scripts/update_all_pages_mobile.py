import os
import re

TOGGLE_BTN = '<button class="mobile-toggle" aria-label="Toggle navigation">☰</button>'

def update_page(filename):
    if not os.path.exists(filename):
        return
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()

    orig = content

    # 1. Standard banner replacement
    banner_inline_regex = re.compile(r'<section style="background:\s*linear-gradient\(135deg,\s*#072718\s*0%,\s*#0D472B\s*100%\);\s*color:\s*#fff;\s*padding:\s*\d+px\s*0;\s*text-align:\s*center;\s*border-bottom:\s*3px\s*solid\s*var\(--secondary\);">')
    content = banner_inline_regex.sub('<section class="page-banner">', content)

    # 2. Add mobile-toggle if missing
    if 'class="mobile-toggle"' not in content:
        # Check if header-actions exists
        if '<div class="header-actions">' in content:
            # Insert button before closing </div> of header-actions
            content = re.sub(
                r'(<div class="header-actions">[\s\S]*?)(</div>)',
                r'\1    <button class="mobile-toggle" aria-label="Toggle navigation">☰</button>\n            \2',
                content,
                count=1
            )
        else:
            # In files like verify.html where header-actions is missing
            content = content.replace(
                '</nav>\n        </div>\n    </header>',
                '</nav>\n            <div class="header-actions">\n                <a href="membership.html" class="btn btn-gold" data-i18n="btn_join">آن لائن ممبرشپ</a>\n                <button class="mobile-toggle" aria-label="Toggle navigation">☰</button>\n            </div>\n        </div>\n    </header>'
            )

    # 3. For verify.html, ensure app.js and full nav-menu are present
    if filename == 'verify.html':
        if 'src="app.js"' not in content:
            content = content.replace(
                '</body>',
                '<script src="i18n.js"></script>\n    <script src="app.js"></script>\n</body>'
            )
        # Update nav menu if incomplete
        if '<li><a href="about.html"' not in content:
            nav_old = '''            <nav>
                <ul class="nav-menu">
                    <li><a href="index.html" class="nav-link" data-i18n="nav_home">صفحہ اول</a></li>
                    <li><a href="membership.html" class="nav-link" data-i18n="nav_membership">ممبرشپ پورٹل</a></li>
                    <li><a href="verify.html" class="nav-link active" data-i18n="nav_verify">کارڈ تصدیق</a></li>
                    <li><a href="contact.html" class="nav-link" data-i18n="nav_contact">رابطہ</a></li>
                </ul>
            </nav>'''
            nav_new = '''            <nav>
                <ul class="nav-menu">
                    <li><a href="index.html" class="nav-link" data-i18n="nav_home">صفحہ اول</a></li>
                    <li><a href="about.html" class="nav-link" data-i18n="nav_about">ہمارے متعلق</a></li>
                    <li><a href="history.html" class="nav-link" data-i18n="nav_history">برادری تاریخ</a></li>
                    <li><a href="leadership.html" class="nav-link" data-i18n="nav_leadership">قیادت و کمیٹیاں</a></li>
                    <li><a href="news-events.html" class="nav-link" data-i18n="nav_news">خبریں و سرگرمیاں</a></li>
                    <li><a href="professionals.html" class="nav-link" data-i18n="nav_professionals">علماء و پروفیشنلز</a></li>
                    <li><a href="membership.html" class="nav-link" data-i18n="nav_membership">ممبرشپ پورٹل</a></li>
                    <li><a href="verify.html" class="nav-link active" data-i18n="nav_verify">کارڈ تصدیق</a></li>
                    <li><a href="contact.html" class="nav-link" data-i18n="nav_contact">رابطہ</a></li>
                </ul>
            </nav>'''
            content = content.replace(nav_old, nav_new)

    if content != orig:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated {filename}")
    else:
        print(f"No changes needed for {filename}")

def main():
    pages = [
        'index.html',
        'about.html',
        'history.html',
        'leadership.html',
        'news-events.html',
        'professionals.html',
        'membership.html',
        'verify.html',
        'contact.html'
    ]
    for p in pages:
        update_page(p)

if __name__ == '__main__':
    main()
