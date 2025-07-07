#!/usr/bin/env python3
"""Automatically add missing extract_text_from_page method to PDFExtractor."""

import re

def patch_pdf_extractor():
    """Add missing method to PDFExtractor class."""
    
    file_path = "C:\Users\rcasa\OneDrive\Documents\ai-adoption-dashboard\data\extractors\pdf_extractor.py"
    
    # The method to add
    new_method = '''    def extract_text_from_page(self, page_number: int) -> str:
        """Extract text from a specific page.
        
        Args:
            page_number: Page number to extract (0-indexed)
            
        Returns:
            Extracted text from the page
        """
        cache_key = f"page_{page_number}"
        if cache_key in self._cached_text:
            return self._cached_text[cache_key]
        
        text = ""
        
        try:
            # Use pdfplumber first for better text extraction
            with pdfplumber.open(self.file_path) as pdf:
                if page_number < len(pdf.pages):
                    page = pdf.pages[page_number]
                    text = page.extract_text() or ""
        except Exception as e:
            logger.warning(f"pdfplumber extraction failed for page {page_number}, falling back to PyPDF2: {e}")
            
            # Fallback to PyPDF2
            try:
                with open(self.file_path, "rb") as file:
                    pdf = PyPDF2.PdfReader(file)
                    if page_number < len(pdf.pages):
                        page = pdf.pages[page_number]
                        text = page.extract_text() or ""
            except Exception as e2:
                logger.error(f"Both PDF extraction methods failed for page {page_number}: {e2}")
        
        self._cached_text[cache_key] = text
        return text

'''
    
    try:
        # Read the file
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if method already exists
        if 'def extract_text_from_page' in content:
            print("✅ extract_text_from_page method already exists!")
            return True
        
        # Find where to insert the method (after extract_text_range)
        pattern = r'(    def extract_text_range.*?return result\n)'
        match = re.search(pattern, content, re.DOTALL)
        
        if match:
            # Insert after extract_text_range method
            insert_pos = match.end()
            new_content = content[:insert_pos] + '\n' + new_method + content[insert_pos:]
            
            # Create backup
            backup_path = file_path + '.backup'
            with open(backup_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"📁 Backup created: {backup_path}")
            
            # Write the patched file
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            print("✅ Successfully added extract_text_from_page method!")
            return True
        else:
            print("❌ Could not find insertion point. Please add manually.")
            print("   Add the method after the extract_text_range method.")
            return False
            
    except FileNotFoundError:
        print(f"❌ File not found: {file_path}")
        print("   Make sure you're running this from the correct directory.")
        return False
    except Exception as e:
        print(f"❌ Error patching file: {e}")
        return False

if __name__ == "__main__":
    print("🔧 Patching PDFExtractor with missing method...")
    
    success = patch_pdf_extractor()
    
    if success:
        print("\n🧪 Test your app now:")
        print("streamlit run app.py")
        
        print("\n💡 If something goes wrong, restore from backup:")
        print("copy pdf_extractor.py.backup pdf_extractor.py")
    else:
        print("\n📝 Manual fix needed:")
        print("1. Open pdf_extractor.py")
        print("2. Find the extract_text_range method")
        print("3. Add the extract_text_from_page method after it")