#!/usr/bin/env python3
"""
Check if PDF files are in the correct location for the AI Adoption Dashboard.
"""

import os
from pathlib import Path
from typing import List, Tuple

def check_pdf_files() -> Tuple[List[str], List[str]]:
    """Check which PDF files are present and which are missing."""
    
    # Expected PDF location
    pdf_dir = Path("AI adoption resources") / "AI dashboard resources 1"
    
    # Required PDF files
    required_pdfs = [
        "hai_ai_index_report_2025.pdf",
        "the-state-of-ai-how-organizations-are-rewiring-to-capture-value_final.pdf",
        "oecd-artificial-intelligence-review-2025.pdf",
        "cost-benefit-analysis-artificial-intelligence-evidence-from-a-field-experiment-on-gpt-4o-1.pdf",
        "the-economic-impact-of-large-language-models.pdf",
        "gs-new-decade-begins.pdf",
        "nvidia-cost-trends-ai-inference-at-scale.pdf",
        "wpiea2024231-print-pdf.pdf",
        "w30957.pdf",
        "Machines of mind_ The case for an AI-powered productivity boom.pdf"
    ]
    
    found_pdfs = []
    missing_pdfs = []
    
    # Check each PDF
    for pdf_name in required_pdfs:
        pdf_path = pdf_dir / pdf_name
        if pdf_path.exists():
            found_pdfs.append(pdf_name)
        else:
            missing_pdfs.append(pdf_name)
    
    return found_pdfs, missing_pdfs

def main():
    """Run the PDF check and display results."""
    print("=" * 60)
    print("AI Adoption Dashboard - PDF File Check")
    print("=" * 60)
    
    # Check if directory exists
    pdf_dir = Path("AI adoption resources") / "AI dashboard resources 1"
    
    if not pdf_dir.exists():
        print(f"\n❌ PDF directory does not exist!")
        print(f"\nExpected location: {pdf_dir.absolute()}")
        print("\nCreating directory for you...")
        pdf_dir.mkdir(parents=True, exist_ok=True)
        print(f"✅ Created: {pdf_dir.absolute()}")
        print("\nNow place your PDF files in this directory.")
        return
    
    print(f"\n📁 Checking PDFs in: {pdf_dir.absolute()}")
    
    # Check PDFs
    found, missing = check_pdf_files()
    
    print(f"\n📊 Status: {len(found)}/10 PDFs found")
    print("-" * 40)
    
    if found:
        print("\n✅ Found PDFs:")
        for pdf in found:
            print(f"   • {pdf}")
    
    if missing:
        print("\n❌ Missing PDFs:")
        for pdf in missing:
            print(f"   • {pdf}")
    
    # Summary
    print("\n" + "=" * 60)
    if len(found) == 10:
        print("🎉 All PDFs are in place! The dashboard will use real data.")
    elif len(found) > 0:
        print(f"⚠️  {len(missing)} PDFs are missing. The dashboard will use demo data.")
    else:
        print("❌ No PDFs found. The dashboard will use demo data.")
    
    print("\nTo use real data, place all 10 PDFs in:")
    print(f"{pdf_dir.absolute()}")
    print("=" * 60)

if __name__ == "__main__":
    main()