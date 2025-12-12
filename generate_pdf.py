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

    # 3. Strip HTML Wrappers (PDF generation doesn't need them, it applies its own CSS)
    # Remove <div class="story-container" ...> and closing </div>
    content = re.sub(r'<div class="story-container"[^>]*>', '', content)
    content = content.replace('</div>', '')

    # 4. Pre-process Image Paths for PDF
    # WeasyPrint needs to find the image locally.
    # If the markdown has src="/max.jpg", change it to "max.jpg" (assuming script runs in same dir)
    content = content.replace('src="/max.jpg"', 'src="max.jpg"')

    # 4. Convert to HTML
    # We use 'extra' for better feature support
    html_body = markdown.markdown(content, extensions=['extra'])
    
    # 5. Build Full HTML Document with CSS
    # Note: We explicitly import the Google Fonts here so WeasyPrint can try to fetch them.
    # However, WeasyPrint sometimes struggles with web fonts if not installed locally.
    # We will provide a robust font stack fallback.
    
    css = """
    @import url('https://fonts.googleapis.com/css2?family=Special+Elite&family=Courier+Prime:ital,wght@0,400;0,700;1,400&family=Georgia:ital,wght@0,400;0,700;1,400&display=swap');
    
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
        background-color: #ffffff; /* White paper for PDF */
        margin: 0;
        padding: 0;
    }

    /* Typography */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Special Elite', cursive;
        color: #2f2f2f;
        font-weight: 400; /* Special Elite is naturally bold */
        margin-top: 1em;
        margin-bottom: 0.5em;
    }

    a {
        color: #2c3e50; /* Slate */
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
        flex-direction: row; /* Ensure side-by-side */
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
        border-bottom: none; /* Override default h1 style */
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
    /* We assume FontAwesome won't render in PDF easily without local fonts.
       So we'll use text content if possible, or just the links.
       Ideally, we'd replace icons with text labels for PDF. 
       We'll do a quick regex fix in Python below to swap icons for text. */

    .profile-header div[style] {
        /* The summary block */
        max-width: 100% !important;
        text-align: center !important;
        font-style: italic;
        color: #444;
        font-size: 10pt;
    }

    /* Content Styling */
    .story-container {
        /* Remove box shadow/border for print to save ink/clean look, 
           or keep it if "light box" is desired. Let's keep it subtle. */
        border: 1px solid #dcdcdc;
        border-left: 4px solid #2c3e50; /* Slate accent */
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
    
    /* Company Name Link */
    h3 a { 
        font-weight: bold; 
        border: none;
        color: #000;
    }

    /* Date / Role line */
    p em {
        font-family: 'Courier Prime', monospace;
        font-size: 9pt;
        color: #666;
        display: block;
        margin-bottom: 5px;
    }

    /* Roles */
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

    /* Hide PDF download link in PDF */
    a[href$=".pdf"] { display: none; }
    """.strip()

    # 6. HTML Template
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

    # 7. Post-Processing HTML (Quick Fixes)
    # Replace FontAwesome icons with Text for PDF readability
    soup = BeautifulSoup(full_html, 'html.parser')
    
    # Map common FA classes to text
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
                # Replace <i> with text span
                new_span = soup.new_tag('span')
                new_span.string = icon_map[cls]
                i_tag.replace_with(new_span)
                break
    
    # Clean up the social links (add spacing)
    for a_tag in soup.select('.social-icons a'):
        # Get the URL
        href = a_tag.get('href')
        if not href: continue
        
        # If it's the email, strip mailto
        display_text = href.replace('mailto:', '').replace('https://', '').replace('www.', '')
        
        # If we replaced the icon with text, append the URL or format nicely
        # Current state: <a><span>Email</span></a>
        # Desired: <a>Email: max...</a> or just the text
        
        if a_tag.find('span'):
            label = a_tag.find('span').string
            # For PDF, let's just show the Label linking to the URL, 
            # maybe add the actual text if it's not obvious?
            # Actually, standard resume header: "max.spevack@gmail.com | linkedin.com/in/..."
            # Let's replace the content of the A tag with the clean URL or label
            if 'linkedin' in href:
                a_tag.string = "LinkedIn"
            elif 'github' in href:
                a_tag.string = "GitHub"
            elif '@' in href:
                 a_tag.string = display_text
            
            
    final_html = str(soup)

    # 8. Render
    print(f"Rendering {INPUT_FILE} to {OUTPUT_FILE}...")
    font_config = FontConfiguration()
    HTML(string=final_html, base_url=".").write_pdf(OUTPUT_FILE, font_config=font_config)
    print("Success!")

if __name__ == "__main__":
    generate_pdf()
