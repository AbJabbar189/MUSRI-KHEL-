import re

def update_leadership():
    with open('leadership.html', 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Add mobile-toggle button if not present in header-actions
    if 'class="mobile-toggle"' not in content:
        content = content.replace(
            '<div class="header-actions">\n                <a href="membership.html" class="btn btn-gold" data-i18n="btn_join">آن لائن ممبرشپ</a>\n            </div>',
            '<div class="header-actions">\n                <a href="membership.html" class="btn btn-gold" data-i18n="btn_join">آن لائن ممبرشپ</a>\n                <button class="mobile-toggle" aria-label="Toggle navigation">☰</button>\n            </div>'
        )

    # 2. Update page-banner
    banner_old = '<section style="background: linear-gradient(135deg, #072718 0%, #0D472B 100%); color: #fff; padding: 50px 0; text-align: center; border-bottom: 3px solid var(--secondary);">'
    if banner_old in content:
        content = content.replace(banner_old, '<section class="page-banner">')

    # 3. For each card in #cabinetCardsContainer, wrap everything between </div> of avatar-wrap and end of cabinet-card into <div class="cabinet-card-content">
    # Pattern to match cabinet-card:
    # <div class="cabinet-card[^"]*"[^>]*>...</div>
    cards_container_match = re.search(r'(<div id="cabinetCardsContainer" class="cabinet-grid">)(.*?)(</div>\s*<!-- /cabinetCardsContainer -->|</div>\s*<!-- VIEW 2:)', content, re.DOTALL)
    if not cards_container_match:
        print("Cards container regex didn't match directly, checking fallback...")
        cards_container_match = re.search(r'(<div id="cabinetCardsContainer" class="cabinet-grid">)(.*?)(</div>\s*<!--\s*==+)', content, re.DOTALL)
        if not cards_container_match:
            cards_container_match = re.search(r'(<div id="cabinetCardsContainer" class="cabinet-grid">)(.*?)(</div>\s*<!-- VIEW 2)', content, re.DOTALL)

    if not cards_container_match:
        print("Could not find cards container boundaries")
        return

    container_header = cards_container_match.group(1)
    cards_block = cards_container_match.group(2)
    container_end = cards_container_match.group(3)

    # Let's parse each card in cards_block
    # Pattern for each card:
    # (<!--\s*\d+\.[^>]*-->\s*<div class="cabinet-card[^"]*"[^>]*>)(.*?)(</div>\s*(?=<!--\s*\d+\.|\Z))
    card_pattern = re.compile(
        r'(<!--\s*\d+\.[^\n]*-->\s*<div class="cabinet-card[^"]*"[^>]*>\s*'
        r'<span class="cabinet-card-number"[^>]*>.*?</span>\s*'
        r'<div class="cabinet-avatar-wrap"[^>]*>.*?</div>\s*)'
        r'(.*?)(</div>\s*(?=<!--\s*\d+\.|\s*\Z))',
        re.DOTALL
    )

    def wrap_card(m):
        prefix = m.group(1)
        body = m.group(2).strip()
        suffix = m.group(3)
        if 'class="cabinet-card-content"' in body:
            return m.group(0)
        new_body = f'\n                    <div class="cabinet-card-content">\n                        {body}\n                    </div>\n                '
        return prefix + new_body + suffix

    new_cards_block = card_pattern.sub(wrap_card, cards_block)
    new_content = content[:cards_container_match.start(2)] + new_cards_block + content[cards_container_match.end(2):]

    with open('leadership.html', 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("leadership.html updated successfully!")

if __name__ == '__main__':
    update_leadership()
