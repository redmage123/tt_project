#!/usr/bin/env python3
"""
Convert all markdown files in docs/workshops to PDF format
"""

import os
import sys
import markdown
from weasyprint import HTML, CSS
from pathlib import Path

def convert_md_to_pdf(md_file, pdf_file):
    """Convert a single markdown file to PDF"""
    print(f"Converting {md_file.name}...", end=" ")

    try:
        # Read markdown content
        with open(md_file, 'r', encoding='utf-8') as f:
            md_content = f.read()

        # Convert markdown to HTML
        html_content = markdown.markdown(
            md_content,
            extensions=['tables', 'fenced_code', 'nl2br']
        )

        # Add CSS styling for better PDF output
        css_style = """
        @page {
            size: A4;
            margin: 2cm;
        }
        body {
            font-family: Arial, sans-serif;
            font-size: 11pt;
            line-height: 1.5;
            color: #333;
        }
        h1 {
            font-size: 24pt;
            color: #2c3e50;
            border-bottom: 2px solid #3498db;
            padding-bottom: 10px;
            margin-top: 20px;
        }
        h2 {
            font-size: 18pt;
            color: #34495e;
            margin-top: 18px;
            border-bottom: 1px solid #bdc3c7;
            padding-bottom: 5px;
        }
        h3 {
            font-size: 14pt;
            color: #34495e;
            margin-top: 14px;
        }
        h4 {
            font-size: 12pt;
            color: #7f8c8d;
            margin-top: 12px;
        }
        code {
            background-color: #f4f4f4;
            padding: 2px 6px;
            border-radius: 3px;
            font-family: monospace;
            font-size: 10pt;
        }
        pre {
            background-color: #f4f4f4;
            padding: 10px;
            border-radius: 5px;
            border-left: 3px solid #3498db;
            overflow-x: auto;
        }
        table {
            border-collapse: collapse;
            width: 100%;
            margin: 10px 0;
        }
        th, td {
            border: 1px solid #ddd;
            padding: 8px;
            text-align: left;
        }
        th {
            background-color: #3498db;
            color: white;
        }
        tr:nth-child(even) {
            background-color: #f9f9f9;
        }
        ul, ol {
            margin: 10px 0;
            padding-left: 30px;
        }
        blockquote {
            border-left: 4px solid #3498db;
            padding-left: 15px;
            margin: 10px 0;
            color: #7f8c8d;
            font-style: italic;
        }
        hr {
            border: none;
            border-top: 2px solid #ecf0f1;
            margin: 20px 0;
        }
        """

        # Wrap HTML with proper structure
        full_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>{md_file.stem}</title>
        </head>
        <body>
            {html_content}
        </body>
        </html>
        """

        # Convert HTML to PDF
        HTML(string=full_html).write_pdf(
            pdf_file,
            stylesheets=[CSS(string=css_style)]
        )

        print(f"✓ Created {pdf_file.name}")
        return True

    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def main():
    # Define directories
    workshop_dir = Path("docs/workshops")
    pdf_dir = workshop_dir / "pdf"

    # Create PDF directory if it doesn't exist
    pdf_dir.mkdir(exist_ok=True)

    # Find all markdown files
    md_files = sorted(workshop_dir.glob("*.md"))

    if not md_files:
        print("No markdown files found in docs/workshops/")
        return 1

    print(f"\nFound {len(md_files)} markdown files to convert\n")
    print("=" * 60)

    # Convert each file
    success_count = 0
    for md_file in md_files:
        pdf_file = pdf_dir / f"{md_file.stem}.pdf"
        if convert_md_to_pdf(md_file, pdf_file):
            success_count += 1

    print("=" * 60)
    print(f"\nConversion complete: {success_count}/{len(md_files)} files successful")
    print(f"PDFs saved to: {pdf_dir}/")

    return 0 if success_count == len(md_files) else 1

if __name__ == "__main__":
    sys.exit(main())
