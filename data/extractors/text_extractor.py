"""Text extraction utilities for PDF documents."""

from typing import Any, Dict, List, Optional, Tuple
import logging
import re

from .base import PDFExtractor

logger = logging.getLogger(__name__)


class TextExtractor:
    """Extract and process text from PDF documents."""
    
    def __init__(self, pdf_extractor: Optional[PDFExtractor] = None):
        """Initialize text extractor.
        
        Args:
            pdf_extractor: Optional PDF extractor instance
        """
        self.pdf_extractor = pdf_extractor
    
    def extract_text(self, page_num: Optional[int] = None) -> str:
        """Extract text from PDF pages.
        
        Args:
            page_num: Optional specific page number
            
        Returns:
            Extracted text as string
        """
        text = ""
        
        if self.pdf_extractor:
            try:
                if page_num is not None:
                    # Extract from specific page
                    if hasattr(self.pdf_extractor, 'extract_text_from_page'):
                        text = self.pdf_extractor.extract_text_from_page(page_num)
                else:
                    # Extract from all pages
                    if hasattr(self.pdf_extractor, 'extract_all_text'):
                        text = self.pdf_extractor.extract_all_text()
            except Exception as e:
                logger.error(f"Error extracting text: {e}")
        
        return text
    
    def extract_sections(self, text: str) -> Dict[str, str]:
        """Extract sections from text based on headers.
        
        Args:
            text: Full text to parse
            
        Returns:
            Dictionary of section_name: section_content
        """
        sections = {}
        
        # Simple section detection based on common patterns
        # Look for lines that might be headers (all caps, numbered, etc.)
        lines = text.split('\n')
        current_section = "Introduction"
        current_content = []
        
        for line in lines:
            # Check if line might be a header
            if self._is_likely_header(line):
                # Save previous section
                if current_content:
                    sections[current_section] = '\n'.join(current_content)
                # Start new section
                current_section = line.strip()
                current_content = []
            else:
                current_content.append(line)
        
        # Save last section
        if current_content:
            sections[current_section] = '\n'.join(current_content)
        
        return sections
    
    def extract_keywords(self, text: str, num_keywords: int = 10) -> List[str]:
        """Extract key terms from text.
        
        Args:
            text: Text to analyze
            num_keywords: Number of keywords to extract
            
        Returns:
            List of keywords
        """
        # Simple keyword extraction based on word frequency
        # Remove common words and count occurrences
        
        # Common words to exclude
        stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'were', 'been',
            'be', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would',
            'could', 'should', 'may', 'might', 'must', 'shall', 'can', 'this',
            'that', 'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they'
        }
        
        # Extract words
        words = re.findall(r'\b[a-z]+\b', text.lower())
        
        # Count frequencies
        word_freq = {}
        for word in words:
            if word not in stop_words and len(word) > 3:
                word_freq[word] = word_freq.get(word, 0) + 1
        
        # Sort by frequency and return top keywords
        sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
        return [word for word, freq in sorted_words[:num_keywords]]
    
    def _is_likely_header(self, line: str) -> bool:
        """Check if a line is likely a section header.
        
        Args:
            line: Line to check
            
        Returns:
            True if likely a header
        """
        line = line.strip()
        
        # Empty lines are not headers
        if not line:
            return False
        
        # Check for common header patterns
        # All caps
        if line.isupper() and len(line) > 3:
            return True
        
        # Numbered sections (1., 1.1, etc.)
        if re.match(r'^\d+\.?\d*\.?\s+\w+', line):
            return True
        
        # Short lines might be headers
        if len(line) < 50 and line[0].isupper():
            return True
        
        return False
    
    def search_text(self, pattern: str, case_sensitive: bool = False) -> List[Tuple[int, str]]:
        """Search for pattern in document text.
        
        Args:
            pattern: Regular expression pattern to search
            case_sensitive: Whether search should be case sensitive
            
        Returns:
            List of (page_number, matching_text) tuples
        """
        matches = []
        
        if self.pdf_extractor and hasattr(self.pdf_extractor, 'get_num_pages'):
            flags = 0 if case_sensitive else re.IGNORECASE
            
            for page_num in range(self.pdf_extractor.get_num_pages()):
                page_text = self.extract_text(page_num)
                
                # Find all matches on this page
                for match in re.finditer(pattern, page_text, flags):
                    matches.append((page_num, match.group()))
        
        return matches