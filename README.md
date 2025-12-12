# spevack.org

This is the source code for my personal website and resume, hosted at [spevack.org](https://spevack.org).

## 🏗 Architecture

The site is built using **Jekyll** and hosted on **GitHub Pages**. It is designed to match the "Vintage" aesthetic of [The Daily Clamour](https://dailyclamour.com).

*   **Theme:** Custom "Vintage Clamour" CSS (no remote theme dependency).
*   **Palette:**
    *   Background (Cream Paper): `#fdfbf7`
    *   Text (Ink Black): `#2f2f2f`
    *   Accents: Slate `#2c3e50`, Urgent Red `#c0392b`
*   **Content:**
    *   `index.md`: Landing page with "Daily Clamour" feature.
    *   `resume.md`: Professional resume.
    *   `fishwrap.md`: "Vibe-Coding" engineering story.

## 📂 File Structure

*   `assets/css/vintage.css`: The source of truth for the site's styling.
*   `generate_pdf.py`: Python script (using WeasyPrint) that transpiles `resume.md` into `resume.pdf`.
*   `_layouts/default.html`: The HTML wrapper. It links the vintage CSS, FontAwesome, and handles the favicons.
*   `max.jpg`: Profile picture.
*   `CNAME`: Configures the custom domain `spevack.org`.

## 🤖 Automation

### PDF Resume Generation
The repository includes a **Git Pre-Commit Hook** (`.git/hooks/pre-commit`) that automatically ensures `resume.pdf` is always in sync with `resume.md`.

1.  When you commit a change to `resume.md`.
2.  The hook runs `generate_pdf.py` (using the `fishwrap` Python environment).
3.  The script converts the Markdown to a clean, print-optimized HTML structure and renders it to PDF.
4.  The updated `resume.pdf` is automatically added to the commit.

You can also generate it manually:
```bash
make pdf
```

## 🚀 Deployment

The site deploys automatically via GitHub Pages whenever a commit is pushed to the `main` branch.

## 🛠 Local Development

To run locally (requires Ruby & Bundler):

```bash
# Setup dependencies
make install

# Run the local server at http://127.0.0.1:4000
make serve
```

Alternatively, you can run the commands directly:

```bash
bundle install
bundle exec jekyll serve
```
