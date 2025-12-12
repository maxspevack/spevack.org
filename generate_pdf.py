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

    # 3. Split Header and Body
    # The header is valid HTML in the markdown file.
    # The body is Markdown wrapped in a div.
    
    # We'll use a simple regex to find the end of the profile-header div.
    # It ends with </div>. Since there are nested divs, we need to be careful.
    # But visually in the file, it's the first big block of HTML.
    
    # Alternative: Parse the WHOLE thing as HTML? No, because the body is Markdown.
    
    # Let's match the <div class="profile-header"> ... </div> block.
    # Since regex is bad at nested HTML, we'll try to split by the known boundary.
    # The boundary is the start of <div class="story-container" ...>
    
    parts = re.split(r'(<div class="story-container"[^>]*>)', content)
    
    if len(parts) < 3:
        # Fallback: Maybe the div isn't there (old version?) or regex failed.
        # Let's assume everything is markdown? No, header is HTML.
        print("Warning: Could not split header and body by story-container. attempting fallback.")
        header_raw = content
        body_raw = ""
    else:
        header_raw = parts[0] # Everything before the story-container
        # parts[1] is the opening tag
        # parts[2] is the rest (content + closing div)
        body_raw = parts[2]
        
        # Remove the closing </div> at the end of the body
        # It's usually the very last line or close to it.
        body_raw = body_raw.replace('</div>', '')

    # 4. Process Header (HTML)
    header_raw = header_raw.replace('src="/max.jpg"', 'src="max.jpg"')
    soup_header = BeautifulSoup(header_raw, 'html.parser')
    
    # Fix Header Icons/Links
    icon_map = {'fa-envelope': 'Email', 'fa-file-pdf': 'PDF', 'fa-linkedin': 'LinkedIn', 'fa-github': 'GitHub'}
    for i_tag in soup_header.find_all('i'):
        classes = i_tag.get('class', [])
        for cls in classes:
            if cls in icon_map:
                new_span = soup_header.new_tag('span')
                new_span.string = icon_map[cls]
                i_tag.replace_with(new_span)
                break
    
    # Fix Links
    for a_tag in soup_header.select('.social-icons a'):
        href = a_tag.get('href')
        if not href: continue
        display_text = href.replace('mailto:', '').replace('https://', '').replace('www.', '')
        if 'linkedin' in href and not a_tag.get_text().strip(): a_tag.string = "LinkedIn"
        elif 'github' in href and not a_tag.get_text().strip(): a_tag.string = "GitHub"
        elif '@' in href and not a_tag.get_text().strip(): a_tag.string = display_text

    final_header_html = str(soup_header)

    # 5. Process Body (Markdown)
    # Now that we stripped the wrapper, it's pure markdown.
    html_body = markdown.markdown(body_raw, extensions=['extra'])

    # 6. Build CSS (Correct Fonts)
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
        font-family: 'Georgia', serif;
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
    """

    # 7. Construct Final HTML
    full_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>Max Spevack - Resume</title>
        <style>{css}</style>
    </head>
    <body>
        {final_header_html}
        <div class="main-content">
            {html_body}
        </div>
    </body>
    </html>
    """

    # Save Debug HTML
    with open(DEBUG_HTML_FILE, "w") as f:
        f.write(full_html)
    print(f"Debug HTML saved to {DEBUG_HTML_FILE}")

    # 8. Render
    print(f"Rendering {INPUT_FILE} to {OUTPUT_FILE}...")
    font_config = FontConfiguration()
    HTML(string=full_html, base_url=".").write_pdf(OUTPUT_FILE, font_config=font_config)
    print("Success!")

if __name__ == "__main__":
    generate_pdf()
