# AlexGibson12.github.io

Personal site. Plain static HTML, no build step.

- `index.html`: homepage (bio, papers, list of posts)
- `posts/`: one page per post
- `images/`: images used in the posts
- `cv.pdf`: CV
- `style.css`: shared styles (light and dark mode)

Maths is rendered in the browser with KaTeX. If a post ever links an external image, `fetch_images.py` copies it into `images/`; a GitHub Action runs it automatically when posts change.

## Adding a post

Copy an existing file in `posts/`, replace the title, date and body, and add a line to the Writing list in `index.html`.
