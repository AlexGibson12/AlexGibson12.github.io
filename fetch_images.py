"""Download every image the posts load from external sites into images/ and point the pages at the local copies.

Run from the site folder:  python3 fetch_images.py
Add --dry-run to list what it would do without downloading or editing anything.
Safe to run more than once: images already downloaded are skipped.
"""
import hashlib
import os
import re
import sys
import urllib.request

DRY_RUN = "--dry-run" in sys.argv
HERE = os.path.dirname(os.path.abspath(__file__))
POSTS = os.path.join(HERE, "posts")
IMAGES = os.path.join(HERE, "images")
IMG_SRC = re.compile(r'<img([^>]*?)src="(https?://[^"]+)"')

os.makedirs(IMAGES, exist_ok=True)
downloaded = failed = 0

for name in sorted(os.listdir(POSTS)):
    if not name.endswith(".html"):
        continue
    path = os.path.join(POSTS, name)
    with open(path, encoding="utf-8") as fh:
        html = fh.read()

    def localise(match):
        global downloaded, failed
        attrs, url = match.group(1), match.group(2)
        ext = os.path.splitext(url.split("?")[0])[1].lower()
        if ext not in (".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg"):
            ext = ".png"
        filename = hashlib.sha1(url.encode()).hexdigest()[:16] + ext
        target = os.path.join(IMAGES, filename)
        if DRY_RUN:
            print(f"{name}: {url} -> images/{filename}")
            return match.group(0)
        if not os.path.exists(target):
            try:
                req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
                with urllib.request.urlopen(req, timeout=30) as resp, open(target, "wb") as out:
                    out.write(resp.read())
                downloaded += 1
            except Exception as err:
                failed += 1
                print(f"FAILED {url}: {err}  (left as a remote link)")
                return match.group(0)
        return f'<img{attrs}src="../images/{filename}"'

    new_html = IMG_SRC.sub(localise, html)
    if not DRY_RUN and new_html != html:
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(new_html)

if not DRY_RUN:
    print(f"Downloaded {downloaded} images, {failed} failed. Pages now use the copies in images/.")
