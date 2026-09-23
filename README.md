# aashna-shah.com

Personal academic website for Aashna P. Shah. Plain static HTML/CSS — no build step, no Jekyll.

- `index.html` — main page (About, Education, Experience, Research, Publications, Talks, Service)
- `gallery/index.html` — photo gallery
- `assets/css/style.css` — all styles (light + dark mode)
- `assets/img/research/*.svg` — research thumbnails
- `assets/img/gallery/*.jpg` — web-sized gallery photos
- `.nojekyll` — tells GitHub Pages to serve the files as-is

## Updating

- **New paper**: add a `.ref` block under `#publications` in `index.html` (and a `.pub-item` under `#research` if it should be featured).
- **New photos**: resize to ~1400px on the long edge, drop into `assets/img/gallery/`, add a `<figure>` in `gallery/index.html`.

The previous Jekyll (academicpages) source is kept in `_archive/jekyll-site/` for reference and is not served.
