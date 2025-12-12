import markdown
import re
import sys
import os
from bs4 import BeautifulSoup
from weasyprint import HTML, CSS
from weasyprint.text.fonts import FontConfiguration

# Configuration
INPUT_FILE = "resume.md"
OUTPUT_FILE = "resume.pdf"
DEBUG_HTML_FILE = "debug_resume.html"

def generate_pdf():
    # 1. Read Markdown
    try:
        with open(INPUT_FILE, "r") as f:
            raw_content = f.read()
    except FileNotFoundError:
        print(f"Error: {INPUT_FILE} not found.")
        sys.exit(1)

    # 2. Strip Front Matter
    content = re.sub(r'^---\n.+?---\n', '', raw_content, flags=re.DOTALL)

    # 3. Strip HTML Wrappers
    # We strip the specific div that wraps the main content for the website layout.
    # The regex now handles attributes like markdown="1"
    content = re.sub(r'<div class="story-container"[^>]*>', '', content)
    content = content.replace('</div>', '')

    # 4. Pre-process Image Paths for PDF
    # WeasyPrint needs to find the image locally.
    content = content.replace('src="/max.jpg"', 'src="max.jpg"')

    # 5. Convert to HTML
    # Enable 'extra' to handle tables or other md features if they exist
    html_body = markdown.markdown(content, extensions=['extra'])
    
    # 6. Build Full HTML Document with CSS
    # Updated Font URL: Removed Georgia (system font), keeping Special Elite and Courier Prime.
    css = """
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
        font-family: 'Georgia', serif; /* System font fallback works well in WeasyPrint */
        font-size: 10pt;
        line-height: 1.4;
        color: #2f2f2f;
        background-color: #ffffff;
        margin: 0;
        padding: 0;
    }

    /* Typography */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Special Elite', cursive;
        color: #2f2f2f;
        font-weight: 400;
        margin-top: 1em;
        margin-bottom: 0.5em;
    }

    a {
        color: #2c3e50;
        text-decoration: none;
        border-bottom: 1px dotted #2c3e50;
    }

    /* Header / Profile Styling */
    .profile-header {
        display: flex;
        flex-direction: column;
        align-items: center;
        border-bottom: 2px solid #2f2f2f;
        padding-bottom: 20px;
        margin-bottom: 20px;
    }

    .identity-row {
        display: flex;
        flex-direction: row;
        align-items: center;
        justify-content: center;
        gap: 30px;
        margin-bottom: 15px;
    }

    /* Photo */
    .profile-photo {
        width: 120px;
        height: 120px;
        border-radius: 50%;
        border: 2px solid #2f2f2f;
        object-fit: cover;
    }

    /* Name */
    h1 {
        font-size: 28pt;
        margin: 0;
        line-height: 1;
        border-bottom: none;
    }

    .profile-tagline {
        font-family: 'Courier Prime', monospace;
        font-size: 11pt;
        color: #555;
        font-style: italic;
        margin: 5px 0 15px 0;
        text-align: center;
    }

    /* Contact / Social */
    .social-icons {
        margin-bottom: 15px;
        text-align: center;
        font-family: 'Courier Prime', monospace;
        font-size: 9pt;
    }
    .social-icons a {
        margin: 0 10px;
        display: inline-block;
        border-bottom: none;
    }

    .profile-header div[style] {
        max-width: 100% !important;
        text-align: center !important;
        font-style: italic;
        color: #444;
        font-size: 10pt;
    }

    /* Content Styling */
    .story-container {
        border: 1px solid #dcdcdc;
        border-left: 4px solid #2c3e50;
        padding: 20px;
        background-color: #fcfcfc;
    }

    h2 {
        font-size: 16pt;
        border-bottom: 1px solid #dcdcdc;
        padding-bottom: 5px;
        margin-top: 25px;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    h3 {
        font-size: 13pt;
        margin-bottom: 2px;
        margin-top: 20px;
    }
    
    h3 a {
        font-weight: bold; 
        border: none;
        color: #000;
    }

    p em {
        font-family: 'Courier Prime', monospace;
        font-size: 9pt;
        color: #666;
        display: block;
        margin-bottom: 5px;
    }

    strong {
        font-weight: 700;
        color: #2c3e50;
    }

    ul {
        margin-top: 5px;
        padding-left: 1.2em;
    }
    li {
        margin-bottom: 4px;
        text-align: justify;
    }

    a[href$=".pdf"] { display: none; }
    """.strip()

    full_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>Max Spevack - Resume</title>
        <style>{css}</style>
    </head>
    <body>
        {html_body}
    </body>
    </html>
    """

    # 7. Post-Processing HTML
    soup = BeautifulSoup(full_html, 'html.parser')
    
    # Text replacements for icons
    icon_map = {
        'fa-envelope': 'Email',
        'fa-file-pdf': 'PDF',
        'fa-linkedin': 'LinkedIn',
        'fa-github': 'GitHub'
    }
    
    for i_tag in soup.find_all('i'):
        classes = i_tag.get('class', [])
        for cls in classes:
            if cls in icon_map:
                new_span = soup.new_tag('span')
                new_span.string = icon_map[cls]
                i_tag.replace_with(new_span)
                break
    
    # Link Text Cleanup
    for a_tag in soup.select('.social-icons a'):
        href = a_tag.get('href')
        if not href: continue
        
        display_text = href.replace('mailto:', '').replace('https://', '').replace('www.', '')
        
        # If the link has the new span we just added, we're good.
        # If it has nothing (was empty), set text.
        if 'linkedin' in href:
            if not a_tag.get_text().strip(): a_tag.string = "LinkedIn"
        elif 'github' in href:
            if not a_tag.get_text().strip(): a_tag.string = "GitHub"
        elif '@' in href:
            # For email, show the address if possible, or just "Email"
             if not a_tag.get_text().strip(): a_tag.string = display_text

    final_html = str(soup)

    # Save Debug HTML
    with open(DEBUG_HTML_FILE, "w") as f:
        f.write(final_html)
    print(f"Debug HTML saved to {DEBUG_HTML_FILE}")

    # 8. Render
    print(f"Rendering {INPUT_FILE} to {OUTPUT_FILE}...")
    font_config = FontConfiguration()
    HTML(string=final_html, base_url=".").write_pdf(OUTPUT_FILE, font_config=font_config)
    print("Success!")

if __name__ == "__main__":
    generate_pdf()