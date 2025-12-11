import markdown
import re
import sys
from bs4 import BeautifulSoup, Tag
from weasyprint import HTML

# Configuration
INPUT_FILE = "index.md"
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

    # 3. Convert to HTML
    html_raw = markdown.markdown(content)
    soup = BeautifulSoup(html_raw, 'html.parser')

    # 4. Clean ALL inline styles
    for tag in soup.descendants:
        if hasattr(tag, 'attrs'):
            if 'style' in tag.attrs:
                del tag.attrs['style']

    # 5. Extract and Rebuild Header
    # The first div contains the profile info
    # Note: In standard markdown-to-html, there might not be a wrapping div, 
    # but the previous code assumed one. Let's adapt if needed.
    # Looking at index.md structure, the header is likely the first few elements.
    # The previous code assumed 'header_div = soup.find('div')'. 
    # Let's inspect what markdown usually produces.
    # If the markdown has raw HTML <div> wrapper, it works. 
    # If it's just # Header, it might be h1, p, p...
    
    # We'll try to find the structure assuming the user's specific index.md format.
    # If soup.find('div') is None (because markdown didn't wrap it), we might need to grab the first elements.
    
    header_div = soup.find('div')
    if not header_div:
        # Fallback: Create a div from the first N elements if they look like header?
        # Or maybe the user's markdown has a <div id="header"> or similar.
        # Let's check if there is an image (profile photo) to anchor us.
        img = soup.find('img')
        if img and img.parent.name == 'div':
            header_div = img.parent
    
    if header_div:
        new_header = soup.new_tag('div', attrs={'class': 'header'})
        
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
        
        # Title (first p after h1)
        # Note: Be careful if structure changed.
        title_p = header_div.find('p') # The first p is title?
        if title_p:
            title_p['class'] = 'title'
            info_container.append(title_p)

        # Contact Links
        contact_div = soup.new_tag('div', attrs={'class': 'contact-info'})
        # The second p has the links?
        all_ps = header_div.find_all('p')
        if len(all_ps) > 1:
            links_p = all_ps[1] 
            for a in links_p.find_all('a'):
                href = a.get('href')
                if not href or 'resume.pdf' in href: continue # Skip resume download link
                
                link_span = soup.new_tag('span', attrs={'class': 'contact-item'})
                # Determine icon type or label based on href
                label = clean_url(href)
                link_span.string = label + "  " # Add spacer
                contact_div.append(link_span)
        
        info_container.append(contact_div)
        
        # Intro Text (last p in div)
        if len(all_ps) > 2:
            intro_p = all_ps[-1]
            intro_div = soup.new_tag('div', attrs={'class': 'summary'})
            intro_div.append(intro_p)
            info_container.append(intro_div)

        new_header.append(info_container)
        
        # Replace the old header div with our structured one
        header_div.replace_with(new_header)
    else:
        new_header = "" # Should not happen given previous success

    # 6. Rebuild Sections (Experience, Education)
    # We iterate through siblings to group linear elements into blocks
    
    # Create a wrapper for the main content
    main_content = soup.new_tag('div', attrs={'class': 'main-content'})
    
    # Helper to flush current job to main_content
    def create_entry(company_tag, date_tag, role_tags, content_tags):
        entry = soup.new_tag('div', attrs={'class': 'entry'})
        
        # Header Row: Company | Date
        row1 = soup.new_tag('div', attrs={'class': 'entry-header'})
        
        comp_span = soup.new_tag('span', attrs={'class': 'company'})
        # company_tag is <h2><a>Name</a></h2>
        comp_name = company_tag.get_text()
        comp_span.string = comp_name
        
        date_span = soup.new_tag('span', attrs={'class': 'date'})
        date_span.string = date_tag.get_text() if date_tag else ""
        
        row1.append(comp_span)
        row1.append(date_span)
        entry.append(row1)
        
        # Role(s)
        # Note: sometimes multiple roles.
        for r in role_tags:
            r_div = soup.new_tag('div', attrs={'class': 'role'})
            r_div.string = r.get_text()
            entry.append(r_div)
            
        # Content (ul, p)
        details = soup.new_tag('div', attrs={'class': 'details'})
        for c in content_tags:
            details.append(c)
        entry.append(details)
        
        return entry

    # Parsing state machine
    pending_company = None
    pending_date = None
    pending_roles = []
    pending_content = []

    # Iterate over top-level elements *after* the new header
    # Since we replaced the first div, we need to be careful with navigation
    # Let's just iterate through body children
    
    for tag in list(soup.body.children if soup.body else soup.children):
        if tag.name == 'div' and tag.get('class') == ['header']:
            continue # Skip our new header
        if tag.name == 'hr':
            continue # Skip separators
        
        if tag.name == 'h2':
            # Is this a Section Header (Experience/Education) or a Company Name?
            is_company = tag.find('a') is not None
            
            if not is_company:
                # Flush pending job if any
                if pending_company:
                    main_content.append(create_entry(pending_company, pending_date, pending_roles, pending_content))
                    pending_company, pending_date, pending_roles, pending_content = None, None, [], []
                
                # Start new Section
                section_title = tag.get_text()
                sec_header = soup.new_tag('h3', attrs={'class': 'section-header'})
                sec_header.string = section_title.upper()
                main_content.append(sec_header)
                
            else:
                # It's a Company/School
                # Flush previous job
                if pending_company:
                    main_content.append(create_entry(pending_company, pending_date, pending_roles, pending_content))
                    pending_company, pending_date, pending_roles, pending_content = None, None, [], []
                
                pending_company = tag
        
        elif tag.name == 'p':
            # Could be Date, or Role (if wrapped in p?), or Content
            # Identify Date: usually immediately follows Company
            text = tag.get_text().strip()
            if pending_company and not pending_date and re.match(r'^\(.*\)$', text):
                pending_date = tag
            else:
                # Just content?
                if pending_company:
                    pending_content.append(tag)
        
        elif tag.name == 'strong':
            # Role?
            if pending_company:
                pending_roles.append(tag)
                
        elif tag.name == 'ul':
            if pending_company:
                pending_content.append(tag)

    # Flush final
    if pending_company:
        main_content.append(create_entry(pending_company, pending_date, pending_roles, pending_content))

    # 7. Construct Final HTML
    # CSS
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
        border-radius: 50%; /* Circle */
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
        margin-top: 15px;
        margin-bottom: 10px;
        padding-bottom: 2px;
        color: #000;
    }
    
    /* Entries */
    .entry {
        margin-bottom: 12px;
        page-break-inside: avoid; /* Try to keep jobs together */
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
    }
    .details {
        font-size: 9.5pt;
    }
    .details ul {
        margin: 0;
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

    # 8. Render
    print(f"Rendering {INPUT_FILE} to {OUTPUT_FILE} (Resume Layout)...")
    HTML(string=final_html, base_url=".").write_pdf(OUTPUT_FILE)
    print("Success!")

if __name__ == "__main__":
    generate_pdf()
