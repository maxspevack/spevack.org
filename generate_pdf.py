import markdown
import re
import sys
import os
from bs4 import BeautifulSoup
from weasyprint import HTML, CSS

# Configuration
INPUT_FILE = "resume.md"
OUTPUT_FILE = "resume.pdf"

def clean_url(url):
    """Strip https://, mailto:, and trailing slashes for display."""
    clean = url.replace("https://", "").replace("http://", "").replace("mailto:", "")
    if clean.endswith("/"):
        clean = clean[:-1]
    return clean

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

    # 3. Fix Image Paths (Local file system)
    # Convert /max.jpg to max.jpg so WeasyPrint finds it in CWD
    content = content.replace('src="/max.jpg"', 'src="max.jpg"')

    # 4. Convert to HTML
    # Enable 'markdown.extensions.extra' for better handling of nested structures if needed
    html_raw = markdown.markdown(content, extensions=['extra'])
    soup = BeautifulSoup(html_raw, 'html.parser')

    # 5. Clean ALL inline styles for consistent PDF styling
    for tag in soup.descendants:
        if hasattr(tag, 'attrs') and 'style' in tag.attrs:
            del tag.attrs['style']

    # 6. Extract Header
    # We look for the profile-header div
    header_div = soup.find('div', class_='profile-header')
    
    new_header = soup.new_tag('div', attrs={'class': 'header'})
    
    if header_div:
        # Process Image
        img = header_div.find('img')
        if img:
            img_container = soup.new_tag('div', attrs={'class': 'header-photo'})
            img['class'] = 'profile-photo'
            img_container.append(img)
            new_header.append(img_container)

        # Process Info (Name, Title, Contact)
        info_container = soup.new_tag('div', attrs={'class': 'header-info'})
        
        # Name
        h1 = header_div.find('h1')
        if h1:
            h1['class'] = 'name'
            info_container.append(h1)
        
        # Title (Find by class profile-tagline)
        title_p = header_div.find(class_='profile-tagline')
        if title_p:
            title_p['class'] = 'title'
            info_container.append(title_p)

        # Contact Links
        contact_div = soup.new_tag('div', attrs={'class': 'contact-info'})
        social_div = header_div.find(class_='social-icons')
        
        links_source = social_div.find_all('a') if social_div else []
        for a in links_source:
            href = a.get('href')
            # Skip email mailto prefix for display, keep link
            # Skip PDF download link
            if not href or 'resume.pdf' in href: continue 
            
            link_span = soup.new_tag('span', attrs={'class': 'contact-item'})
            
            # Icon mapping (simple text for PDF)
            label = clean_url(href)
            link_span.string = label + "  "
            contact_div.append(link_span)
        
        info_container.append(contact_div)
        
        # Intro Text (The div after social icons)
        # It's usually the last div in profile-header
        intro_texts = [child for child in header_div.children if child.name == 'div' and not child.get('class')]
        if intro_texts:
             intro_div = soup.new_tag('div', attrs={'class': 'summary'})
             # Copy contents
             for c in intro_texts[0].contents:
                 intro_div.append(c)
             info_container.append(intro_div)

        new_header.append(info_container)
    else:
        print("Warning: profile-header not found.")

    # 7. Flatten and Rebuild Sections
    # The content might be inside a .story-container div or top level
    # We will iterate through all elements that are NOT the header
    
    main_content = soup.new_tag('div', attrs={'class': 'main-content'})
    
    # Locate the start of content. It's either inside story-container or just after header
    story_container = soup.find('div', class_='story-container')
    content_source = story_container if story_container else soup

    # Helper to flush current job to main_content
    def create_entry(company_tag, date_tag, role_tags, content_tags):
        entry = soup.new_tag('div', attrs={'class': 'entry'})
        
        # Header Row: Company | Date
        row1 = soup.new_tag('div', attrs={'class': 'entry-header'})
        
        comp_span = soup.new_tag('span', attrs={'class': 'company'})
        comp_span.append(company_tag.get_text())
        
        date_span = soup.new_tag('span', attrs={'class': 'date'})
        date_span.string = date_tag.get_text() if date_tag else ""
        
        row1.append(comp_span)
        row1.append(date_span)
        entry.append(row1)
        
        # Role(s)
        for r in role_tags:
            r_div = soup.new_tag('div', attrs={'class': 'role'})
            r_div.string = r.get_text()
            entry.append(r_div)
            
        # Content
        details = soup.new_tag('div', attrs={'class': 'details'})
        for c in content_tags:
            details.append(c)
        entry.append(details)
        
        return entry

    # State Machine
    pending_company = None
    pending_date = None
    pending_roles = []
    pending_content = []

    # Iterate elements in content_source
    for tag in content_source.children:
        if tag.name == 'h2':
            # Section Header (Experience / Education)
            # Flush pending
            if pending_company:
                main_content.append(create_entry(pending_company, pending_date, pending_roles, pending_content))
                pending_company, pending_date, pending_roles, pending_content = None, None, [], []
            
            sec_header = soup.new_tag('h3', attrs={'class': 'section-header'})
            sec_header.string = tag.get_text().upper()
            main_content.append(sec_header)

        elif tag.name == 'h3':
            # Job / School
            # Flush pending
            if pending_company:
                main_content.append(create_entry(pending_company, pending_date, pending_roles, pending_content))
                pending_company, pending_date, pending_roles, pending_content = None, None, [], []
            
            pending_company = tag

        elif tag.name == 'p':
            text = tag.get_text().strip()
            # Date detection: Starts with ( and ends with ) or contains date-like patterns
            # In resume.md: *(July 2025 - Present)* which is <em>...</em> inside <p>
            # Markdown usually renders *Text* as <p><em>Text</em></p>
            if pending_company and not pending_date and (text.startswith('(') or text.startswith('*(')):
                 pending_date = tag
            # Role detection: **Role** -> <strong>Role</strong>
            elif pending_company and tag.find('strong') and len(tag.get_text()) < 100:
                # If the paragraph is JUST the role (or mostly), treat as role
                # But sometimes role is separate.
                # In resume.md: **Senior Principal Linux Architect** <br> **Chief of Staff...**
                # This might come as one p with br or multiple.
                # Let's assume lines with <strong> are roles if appear before lists
                pass # Handled by content append, but let's try to extract explicit roles?
                # Simpler: Just dump it into content/details for now, or refine?
                # The user wanted "lighter box". The PDF formatting is separate.
                # Let's try to identify explicit role lines if possible.
                if tag.find('strong'):
                     pending_roles.append(tag)
                else:
                     pending_content.append(tag)
            else:
                if pending_company:
                    pending_content.append(tag)
        
        elif tag.name == 'ul':
            if pending_company:
                pending_content.append(tag)

    # Flush final
    if pending_company:
        main_content.append(create_entry(pending_company, pending_date, pending_roles, pending_content))

    # 8. CSS Styling
    css = """
    @page { size: Letter; margin: 0.5in; }
    body {
        font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
        color: #333;
        font-size: 10pt;
        line-height: 1.4;
    }
    a { color: #333; text-decoration: none; }
    
    /* Header */
    .header {
        display: flex;
        flex-direction: row;
        border-bottom: 2px solid #333;
        padding-bottom: 15px;
        margin-bottom: 15px;
        align-items: center;
    }
    .header-photo {
        flex: 0 0 100px;
        margin-right: 20px;
    }
    .profile-photo {
        width: 100px;
        height: 100px;
        object-fit: cover;
        border-radius: 50%;
        border: 1px solid #ddd;
    }
    .header-info {
        flex: 1;
    }
    .name {
        font-size: 24pt;
        font-weight: bold;
        margin: 0 0 5px 0;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .title {
        font-size: 12pt;
        color: #666;
        margin: 0 0 10px 0;
        font-weight: 600;
    }
    .contact-info {
        font-size: 9pt;
        color: #555;
        margin-bottom: 10px;
    }
    .contact-item {
        margin-right: 15px;
        display: inline-block;
    }
    .contact-item:last-child { margin-right: 0; }
    
    .summary p {
        margin: 0;
        font-size: 9.5pt;
        color: #444;
        font-style: italic;
    }

    /* Sections */
    .section-header {
        font-size: 12pt;
        border-bottom: 1px solid #ccc;
        margin-top: 20px;
        margin-bottom: 10px;
        padding-bottom: 2px;
        color: #000;
        font-weight: bold;
    }
    
    /* Entries */
    .entry {
        margin-bottom: 15px;
        page-break-inside: avoid;
    }
    .entry-header {
        display: flex;
        justify-content: space-between;
        align-items: baseline;
        margin-bottom: 2px;
    }
    .company {
        font-weight: bold;
        font-size: 11pt;
    }
    .date {
        font-size: 9pt;
        font-style: italic;
        color: #666;
    }
    .role {
        font-weight: 600;
        font-size: 10pt;
        margin-bottom: 2px;
        color: #222;
    }
    /* Clean up paragraphs in roles if they exist */
    .role p { margin: 0; display: inline; }
    
    .details {
        font-size: 9.5pt;
    }
    .details ul {
        margin: 2px 0 0 0;
        padding-left: 18px;
    }
    .details li {
        margin-bottom: 2px;
    }
    .details p {
        margin: 2px 0;
    }
    """

    final_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <style>{css}</style>
    </head>
    <body>
        {new_header}
        {main_content}
    </body>
    </html>
    """

    # 9. Render
    print(f"Rendering {INPUT_FILE} to {OUTPUT_FILE} (Resume Layout)...")
    # base_url="." ensures it finds images in the current directory
    HTML(string=final_html, base_url=".").write_pdf(OUTPUT_FILE)
    print("Success!")

if __name__ == "__main__":
    generate_pdf()