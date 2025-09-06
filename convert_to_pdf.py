
import os
import markdown
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from bs4 import BeautifulSoup

# ====== Register Calibri font (make sure you have Calibri.ttf in same folder or system path) ======
pdfmetrics.registerFont(TTFont("Calibri", "/Users/navidfarhang/Documents/GitHub/Ml_in_production/calibri.ttf"))



# Paths
folder_path = "/Users/navidfarhang/Documents/GitHub/Ml_in_production"
output_pdf = "book.pdf"

# PDF document
doc = SimpleDocTemplate(
    output_pdf,
    rightMargin=72, leftMargin=72,
    topMargin=72, bottomMargin=72
)

# Styles
styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name="Justify", fontName="Calibri", fontSize=11, leading=14, alignment=4))
styles.add(ParagraphStyle(name="MyHeading1", fontName="Calibri", fontSize=18, leading=22, spaceAfter=12))
styles.add(ParagraphStyle(name="MyHeading2", fontName="Calibri", fontSize=14, leading=18, spaceAfter=10))
styles.add(ParagraphStyle(name="Link", fontName="Calibri", fontSize=11, textColor="blue", underline=True, alignment=4))

story = []

# Loop through markdown files
for filename in sorted(os.listdir(folder_path)):
    if filename.endswith(".md"):
        file_path = os.path.join(folder_path, filename)
        with open(file_path, "r", encoding="utf-8") as f:
            md_text = f.read()

        # Convert markdown → HTML
        html_text = markdown.markdown(md_text)

        # Parse HTML
        soup = BeautifulSoup(html_text, "html.parser")

        for elem in soup.descendants:
            if elem.name == "h1":
                story.append(Paragraph(elem.text, styles["MyHeading1"]))
                story.append(Spacer(1, 12))
            elif elem.name == "h2":
                story.append(Paragraph(elem.text, styles["MyHeading2"]))
                story.append(Spacer(1, 10))
            elif elem.name == "p":
                story.append(Paragraph(elem.text, styles["Justify"]))
                story.append(Spacer(1, 8))
            elif elem.name == "a":  # hyperlink
                href = elem.get("href", "")
                link_html = f'<a href="{href}" color="blue">{elem.text}</a>'
                story.append(Paragraph(link_html, styles["Link"]))
                story.append(Spacer(1, 8))
            elif elem.name == "img":
                img_path = elem["src"]
                if not os.path.isabs(img_path):
                    img_path = os.path.join(folder_path, img_path)

                if os.path.exists(img_path):
                    try:
                        img = Image(img_path, width=6*inch, height=4*inch)
                        story.append(img)
                        story.append(Spacer(1, 12))
                    except Exception as e:
                        print(f"⚠️ Could not load image {img_path}: {e}")

# Build PDF
doc.build(story)

print(f"✅ PDF saved as {output_pdf}")
