import markdown
from weasyprint import HTML, CSS
import requests
import os

# Define paths
CUR_DIR = os.path.dirname(os.path.abspath(__file__))
INDEX_MD_PATH = os.path.join(CUR_DIR, 'index.md')
RESUME_PDF_PATH = os.path.join(CUR_DIR, 'resume.pdf')

# Fetch custom CSS from Dracula Theme
CSS_URL = 'https://draculatheme.com/assets/css/style.css'
try:
    response = requests.get(CSS_URL)
    response.raise_for_status() # Raise an exception for HTTP errors
    css_content = response.text
except requests.exceptions.RequestException as e:
    print(f"Warning: Could not fetch CSS from {CSS_URL}. Using fallback. Error: {e}")
    css_content = "" # Fallback to empty CSS if fetch fails

# Custom PDF styling
CUSTOM_PDF_CSS = """
body { padding: 50px; background-color: #282a36; color: #f8f8f2; font-family: 'Inter', sans-serif; }
h1, h2, h3, h4, h5, h6 { font-family: 'Inter', sans-serif; }
a { color: #8be9fd; text-decoration: none; }
a:hover { text-decoration: underline; }
"""

print(f"Generating resume.pdf from {INDEX_MD_PATH}...")

try:
    # Read Markdown content
    with open(INDEX_MD_PATH, 'r', encoding='utf-8') as f:
        md_content = f.read()

    # Convert Markdown to HTML
    html_content = markdown.markdown(md_content)

    # Combine all HTML and CSS
    full_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap" rel="stylesheet">
        <style>{css_content}</style>
        <style>{CUSTOM_PDF_CSS}</style>
    </head>
    <body>
        {html_content}
    </body>
    </html>
    """

    # Generate PDF using WeasyPrint
    HTML(string=full_html, base_url=CUR_DIR).write_pdf(RESUME_PDF_PATH)

    print(f"Successfully generated {RESUME_PDF_PATH}")

except Exception as e:
    print(f"Error generating PDF: {e}")