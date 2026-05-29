# ThemeParkMaps.net

A nostalgic theme park map archive and guide directory built with [Eleventy](https://www.11ty.dev/) for static hosting on GitHub Pages.

## Local Development

```bash
npm install
npm run dev
```

Eleventy serves the site locally, usually at `http://localhost:8080`.

## Production Build

```bash
npm run build
```

The generated static site is written to `_site/`.

## GitHub Pages Setup

1. Push this repository to GitHub.
2. In GitHub, open `Settings` -> `Pages`.
3. Set `Source` to `GitHub Actions`.
4. Push to the `main` branch. The workflow at `.github/workflows/deploy.yml` will build the site and deploy `_site/`.
5. For `themeparkmaps.net`, point your DNS records at GitHub Pages and keep `src/CNAME` set to `themeparkmaps.net`.

## Updating Content

- Parks, maps, and years are in `src/_data/`.
- Blog posts are Markdown files in `src/blog/` and are listed automatically.
- Page templates are in `src/`.
- Images live in `src/assets/img/`.
- Replace the placeholder SVGs with real scans or public-domain photos when ready, then update the image paths in the data files.
