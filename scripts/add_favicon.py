import glob

icon_tag = '    <link rel="icon" type="image/jpeg" href="/images/logo.jpg">\n'

for f in glob.glob("frontend/public/*.html"):
    content = open(f, "r", encoding="utf-8").read()
    if 'rel="icon"' not in content:
        content = content.replace("<head>", f"<head>\n{icon_tag}")
        with open(f, "w", encoding="utf-8") as out:
            out.write(content)
print("Favicon added to all pages successfully!")
