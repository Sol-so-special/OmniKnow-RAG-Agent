"""
Run this script to generate test PDF:
  python scripts/generate_test_pdf.py
  
REQUIREMENTS:
  This script needs the reportlab package.
  Install it before running:
      pip install reportlab
"""

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from pathlib import Path

output_dir = Path("tests/fixtures")
output_dir.mkdir(parents=True, exist_ok=True)

pdf_path = output_dir / "test_document.pdf"

c = canvas.Canvas(str(pdf_path), pagesize=letter)
c.drawString(100, 750, "Test Document for OmniKnow RAG Agent")
c.drawString(100, 730, "This is a test PDF for automated testing.")
c.drawString(100, 710, "Content: Machine learning and AI research.")
c.save()

print(f"✅ Created test PDF at: {pdf_path}")