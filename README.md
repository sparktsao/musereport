# MuseSpark Research Library

A searchable catalog of HTML research reports on AI systems, agent engineering, evaluation, and industry insights. English and Traditional Chinese reports are included.

## Preview locally

Open `index.html` directly in your browser, or serve this folder:

```sh
python3 -m http.server 8000
```

Visit http://localhost:8000. The catalog has no external dependencies. Individual reports may use externally hosted fonts, scripts, or source links.

## Publish on GitHub Pages

1. Create an empty GitHub repository named `MuseSparkReport` (do not initialize it with a README).
2. Push this folder, replacing `YOUR_USERNAME` below with your GitHub username:

   ```sh
   git add .
   git commit -m "Add research library and GitHub Pages publishing"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/MuseSparkReport.git
   git push -u origin main
   ```

3. In the GitHub repository, open **Settings → Pages → Build and deployment → Source** and select **GitHub Actions**.
4. Open **Actions → Publish report library → Run workflow**. Future pushes to the default branch publish automatically.
5. The live catalog will be at `https://YOUR_USERNAME.github.io/MuseSparkReport/`. The completed workflow also provides the deployed URL.

The workflow supports a default branch named either `main` or `master`. Only root HTML reports and the `assets` folder are published. See [GitHub's custom Pages workflow documentation](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages).

Alternatively, select **Deploy from a branch**, choose your default branch and **/ (root)**. In that mode, regenerate and commit `index.html` whenever you add a report; the Actions workflow above is intended for the GitHub Actions publishing source.

## Add or update reports

1. Copy an `.html` or `.htm` report into the repository root. Keep its supporting images or scripts in `assets/` and use relative links.
2. Optionally add an entry to `reports.json` keyed by its exact filename, with `title`, `description`, `topic`, and `language`. Language values are `English`, `繁體中文`, or `EN / 繁中` for bilingual reports.
3. Run `python3 scripts/build_catalog.py` to refresh the local catalog.
4. Commit and push your changes. The GitHub Actions workflow regenerates the published catalog automatically, so new reports are included even without metadata.

Reports without metadata use their HTML title, the topic `Research`, and an unspecified language. Catalog links are URL-encoded and relative, so spaces, punctuation, and GitHub Pages repository subpaths work correctly. Existing report content is preserved.

## Files

- `index.html`: generated catalog, usable even with JavaScript disabled.
- `assets/catalog.css` and `assets/catalog.js`: responsive styling and search/filter controls.
- `reports.json`: curated report descriptions and categories; entry order defines display order.
- `scripts/catalog.template.html`: edit this to change the catalog layout.
- `scripts/build_catalog.py`: Python standard-library catalog generator.
- `.github/workflows/pages.yml`: GitHub Pages build and deployment.
