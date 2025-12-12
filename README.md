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
*   `generate_pdf.py`: Python script (using WeasyPrint) that transpiles `resume.md` into `resume.pdf`. **Crucially, this script ingests `vintage.css` directly**, ensuring the PDF always matches the website's design.
*   `_layouts/default.html`: The HTML wrapper. It links the vintage CSS, FontAwesome, and handles the favicons.
*   `max.jpg`: Profile picture.
*   `CNAME`: Configures the custom domain `spevack.org`.

## 🤖 Automation

### PDF Resume Generation
The repository uses a local build process (via `Makefile`) to generate the PDF artifact before pushing.

1.  **Generate:** `make generate-pdf` builds `resume.pdf` from `resume.md`, applying `vintage.css` styles.
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