# spevack.org

This is the source code for my personal website and resume, hosted at [spevack.org](https://spevack.org).

## 🏗 Architecture

The site is built using **Jekyll** and hosted on **GitHub Pages**. It prioritizes minimalism and maintainability by separating content from presentation using a remote theme.

*   **Theme:** [Dracula Theme for Jekyll](https://draculatheme.com/gh-pages) (`dracula/gh-pages`).
*   **Content:** Single-page Markdown (`index.md`).
*   **Layout:** Overridden default layout (`_layouts/default.html`) to provide a custom header and favicon support while inheriting the theme's styling.

## 📂 File Structure

*   `index.md`: The single source of truth for the resume content. Written in standard Markdown with minimal inline HTML for the header.
*   `_config.yml`: Jekyll configuration file defining the remote theme and site metadata.
*   `_layouts/default.html`: The HTML wrapper that overrides the theme's default. It links the theme's CSS, FontAwesome, and handles the favicons.
*   `max.jpg`: Profile picture.
*   `CNAME`: Configures the custom domain `spevack.org`.

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
