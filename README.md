# spevack.org 👤

This is the source code for my personal website and resume, hosted at [spevack.org](https://spevack.org).

---

## 🏗 Architecture

The site is a hybrid static build:
*   **Website:** Built with **Jekyll**, hosted on GitHub Pages.
*   **Resume (PDF):** Built with **Python** & **WeasyPrint** for pixel-perfect print layout.

### Theming
*   **Website Theme:** Custom "Vintage Clamour" CSS (`assets/css/vintage.css`).
*   **Resume Theme:** Custom "Clean Professional" CSS (`assets/css/resume.css`).

---

## 🤖 Automation

The `Makefile` handles the dual-build process.

### 1. PDF Generation
`generate_pdf.py` parses `resume.md`, applies `assets/css/resume.css`, and renders `resume.pdf`. This ensures the PDF content is always in sync with the Markdown source but styled for print.

```bash
make generate-pdf
```

### 2. Publishing
The publish target generates the PDF, adds artifacts, and pushes to GitHub (triggering the Pages build).

```bash
make publish-resume
```

---

## 📂 File Structure

*   **`index.md`**: Landing page (Personal Brand + Project Portfolio).
*   **`resume.md`**: Professional CV (Source for PDF and `/resume/` page).
*   **`assets/`**: CSS and Images.
*   **`_layouts/`**: Jekyll templates.

---

*Part of the Gemini Workspace.*