"""Base PDF extraction functionality."""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
import logging

# Note: PDF libraries will be imported when dependencies are installed
try:
    import PyPDF2
    import pdfplumber
    import tabula
    PDF_LIBS_AVAILABLE = True
except ImportError:
    PDF_LIBS_AVAILABLE = False
    logging.warning("PDF processing libraries not installed. Run: pip install PyPDF2 pdfplumber tabula-py")


class PDFExtractor(ABC):
    """Base class for PDF data extraction."""
    
    def __init__(self, file_path: Union[str, Path]):
        """Initialize with PDF file path."""
        self.file_path = Path(file_path)
        if not self.file_path.exists():
            raise FileNotFoundError(f"PDF file not found: {self.file_path}")
        
        if not PDF_LIBS_AVAILABLE:
            raise ImportError(
                "PDF processing libraries not installed. "
                "Run: pip install PyPDF2 pdfplumber tabula-py"
            )
    
    @abstractmethod
    def extract(self) -> Dict[str, Any]:
        """Extract data from PDF.
        
        Returns:
            Dictionary containing extracted data
        """
        pass
    
    def get_page_count(self) -> int:
        """Get number of pages in PDF."""
        with open(self.file_path, 'rb') as file:
            pdf = PyPDF2.PdfReader(file)
            return len(pdf.pages)
    
    def extract_text_from_page(self, page_num: int) -> str:
        """Extract text from specific page.
        
        Args:
            page_num: Page number (0-indexed)
            
        Returns:
            Extracted text
        """
        with open(self.file_path, 'rb') as file:
            pdf = PyPDF2.PdfReader(file)
            if page_num >= len(pdf.pages):
                raise ValueError(f"Page {page_num} does not exist")
            return pdf.pages[page_num].extract_text()
    
    def find_pages_with_keyword(self, keyword: str) -> List[int]:
        """Find pages containing specific keyword.
        
        Args:
            keyword: Keyword to search for
            
        Returns:
            List of page numbers containing keyword
        """
        pages = []
        with open(self.file_path, 'rb') as file:
            pdf = PyPDF2.PdfReader(file)
            for i, page in enumerate(pdf.pages):
                text = page.extract_text().lower()
                if keyword.lower() in text:
                    pages.append(i)
        return pages