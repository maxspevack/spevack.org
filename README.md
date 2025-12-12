# spevack.org

This is the source code for my personal website and resume, hosted at [spevack.org](https://spevack.org).

## 🏗 Architecture

The site is built using **Jekyll** and hosted on **GitHub Pages**. It is designed to allow distinct styling for the public website and the downloadable resume.

*   **Website Theme:** Custom "Vintage Clamour" CSS (`assets/css/vintage.css`).
*   **Resume Theme:** Custom "Clean Professional" CSS (`assets/css/resume.css`).
*   **Palette (Website):**
    *   Background (Cream Paper): `#fdfbf7`
    *   Text (Ink Black): `#2f2f2f`
    *   Accents: Slate `#2c3e50`, Urgent Red `#c0392b`
*   **Content:**
    *   `index.md`: Landing page with "Daily Clamour" feature.
    *   `resume.md`: Professional resume.
    *   `fishwrap.md`: "Vibe-Coding" engineering story.

## 📂 File Structure

*   `assets/css/vintage.css`: The stylesheet for the Jekyll-rendered website.
*   `assets/css/resume.css`: The stylesheet exclusively used by `generate_pdf.py` for the PDF resume.
*   `generate_pdf.py`: Python script (using WeasyPrint) that transpiles `resume.md` into `resume.pdf`. **Crucially, this script ingests `assets/css/resume.css` directly**, ensuring the PDF has a consistent, professional look independent of the website's brand.
*   `_layouts/default.html`: The HTML wrapper for the Jekyll site. It links `assets/css/vintage.css`.
*   `max.jpg`: Profile picture.
*   `CNAME`: Configures the custom domain `spevack.org`.

## 🤖 Automation

### PDF Resume Generation
The repository uses a local build process (via `Makefile`) to generate the PDF artifact before pushing.

1.  **Generate:** `make generate-pdf` builds `resume.pdf` from `resume.md`, applying the `assets/css/resume.css` styles.
2.  **Publish:** `make publish-resume` generates the PDF and pushes all changed artifacts to GitHub.

### Setup
The project manages its own Python virtual environment for PDF generation:

```bash
# Setup Python venv and install dependencies
make install
```

## 🚀 Deployment

The site deploys automatically via GitHub Pages whenever a commit is pushed to the `main` branch.

## 🛠 Local Development

To run locally (requires Ruby & Bundler for the site, Python for the PDF):

```bash
# Run the local server at http://127.0.0.1:4000
make serve
```
