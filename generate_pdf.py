import markdown
import sys
import os
from bs4 import BeautifulSoup
from weasyprint import HTML, CSS
from weasyprint.text.fonts import FontConfiguration

# Configuration
INPUT_FILE = "resume.md"
OUTPUT_FILE = "resume.pdf"
DEBUG_HTML_FILE = "debug_resume.html"
CSS_FILE = "assets/css/resume.css"

def generate_pdf():
    # 1. Read Markdown Content
    try:
        with open(INPUT_FILE, "r") as f:
            raw_content = f.read()
    except FileNotFoundError:
        print(f"Error: {INPUT_FILE} not found.")
        sys.exit(1)

    # 2. Separate Front Matter (YAML) from Content
    # We use a simple split because we don't need the YAML data for the PDF
    if raw_content.startswith("---"):
        parts = raw_content.split("---", 2)
        if len(parts) >= 3:
            content_body = parts[2]
        else:
            content_body = raw_content
    else:
        content_body = raw_content

    # 3. Convert Markdown to HTML
    # We convert the *entire* body first, then parse it with BS4
    html_raw = markdown.markdown(content_body, extensions=['extra'])
    soup = BeautifulSoup(html_raw, 'html.parser')

    # 4. Extract Sections (Robust Parsing)
    # The resume structure is: <div class="profile-header">...</div> <div class="story-container">...</div>
    
    profile_header = soup.find('div', class_='profile-header')
    story_container = soup.find('div', class_='story-container')

    if not profile_header or not story_container:
        print("Error: Could not find 'profile-header' or 'story-container' divs in the markdown.")
        print("Ensure resume.md matches the expected structure.")
        sys.exit(1)

    # 5. Fix Image Paths for WeasyPrint
    # WeasyPrint needs file paths relative to execution root, so leading slash must be removed
    for img in soup.find_all('img'):
        src = img.get('src', '')
        if src.startswith('/'):
            img['src'] = src.lstrip('/')

    # 6. Fix Icons and Links (Header)
    # Convert FontAwesome <i> tags to text spans
    icon_map = {'fa-envelope': 'Email', 'fa-file-pdf': 'PDF', 'fa-linkedin': 'LinkedIn', 'fa-github': 'GitHub'}
    for i_tag in profile_header.find_all('i'):
        classes = i_tag.get('class', [])
        for cls in classes:
            if cls in icon_map:
                new_span = soup.new_tag('span')
                new_span.string = icon_map[cls]
                i_tag.replace_with(new_span)
                break
    
    # Clean up Social Links
    for a_tag in profile_header.select('.social-icons a'):
        href = a_tag.get('href')
        if not href: continue
        
        # Remove empty text/icon links or redundant PDF links in the PDF version
        if href.endswith('.pdf'):
            a_tag.decompose()
            continue

        display_text = href.replace('mailto:', '').replace('https://', '').replace('www.', '')
        if 'linkedin' in href and not a_tag.get_text().strip(): a_tag.string = "LinkedIn"
        elif 'github' in href and not a_tag.get_text().strip(): a_tag.string = "GitHub"
        elif '@' in href and not a_tag.get_text().strip(): a_tag.string = display_text

    # 7. Load External CSS
    try:
        with open(CSS_FILE, "r") as f:
            vintage_css = f.read()
    except FileNotFoundError:
        print(f"Warning: {CSS_FILE} not found. PDF will lack styling.")
        vintage_css = ""

    # 8. Print-Specific CSS Overrides
    # We append this to the loaded CSS
    print_css = """
    @import url('https://fonts.googleapis.com/css2?family=Courier+Prime:ital,wght@0,400;0,700;1,400&family=Special+Elite&display=swap');
    
    @page {
        size: Letter;
        margin: 0.5in;
        @bottom-right {
            content: "Page " counter(page) " of " counter(pages);
            font-family: 'Courier Prime', monospace;
            font-size: 8pt;
            color: #555;
        }
    }

    body {
        background-image: none; /* No newsprint texture for PDF readability */
        background-color: #ffffff;
        font-size: 10pt; /* Ensure readable base size */
    }

    a {
        text-decoration: none;
        color: var(--accent-primary);
    }
    
    /* Ensure colors map correctly if variables aren't supported fully by older WeasyPrint versions
       (Though recent ones support vars). Just in case, we rely on vintage.css being robust. */

    /* Hide the PDF download link if it survived the soup cleanup */
    a[href$=".pdf"] { display: none; }
    """

    # 9. Construct Final HTML
    full_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>Max Spevack - Resume</title>
        <style>
            {vintage_css}
            {print_css}
        </style>
    </head>
    <body>
        {str(profile_header)}
        {str(story_container)}
    </body>
    </html>
    """

    # Save Debug HTML (for inspection, but now ignored by git)
    with open(DEBUG_HTML_FILE, "w") as f:
        f.write(full_html)
    print(f"Debug HTML saved to {DEBUG_HTML_FILE}")

    # 10. Render PDF
    print(f"Rendering {INPUT_FILE} to {OUTPUT_FILE}...")
    font_config = FontConfiguration()
    HTML(string=full_html, base_url=".").write_pdf(OUTPUT_FILE, font_config=font_config)
    print("Success!")

if __name__ == "__main__":
    generate_pdf()