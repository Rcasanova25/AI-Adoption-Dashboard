"""Enhanced PDF extraction implementation with table and chart support."""

import logging
import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union

import pandas as pd

from .base import PDFExtractor

# Import PDF libraries
try:
    import fitz  # PyMuPDF for better text extraction
    import pdfplumber
    import PyPDF2
    import tabula

    PDF_LIBS_AVAILABLE = True
except ImportError as e:
    PDF_LIBS_AVAILABLE = False
    logging.warning(f"PDF processing libraries not fully installed: {e}")

logger = logging.getLogger(__name__)


class PDFExtractor:
    """Enhanced PDF extractor with advanced table and data extraction."""

    def __init__(self, file_path: Union[str, Path]):
        """Initialize PDF extractor."""
        self.file_path = Path(file_path)
        self._metadata = None
        self._cached_text = {}
        self._cached_tables = {}

    def extract(self) -> Dict[str, Any]:
        """Extract all data from PDF."""
        return {
            "metadata": self.extract_metadata(),
            "text": self.extract_all_text(),
            "tables": self.extract_all_tables(),
            "sections": self.extract_sections(),
        }

    def extract_metadata(self) -> Dict[str, Any]:
        """Extract PDF metadata."""
        if self._metadata:
            return self._metadata

        with open(self.file_path, "rb") as file:
            pdf = PyPDF2.PdfReader(file)
            info = pdf.metadata or {}

            self._metadata = {
                "title": info.get("/Title", ""),
                "author": info.get("/Author", ""),
                "subject": info.get("/Subject", ""),
                "creator": info.get("/Creator", ""),
                "creation_date": info.get("/CreationDate", ""),
                "pages": len(pdf.pages),
                "file_size": self.file_path.stat().st_size,
            }

        return self._metadata

    def extract_all_text(self) -> str:
        """Extract all text from PDF."""
        if "all" in self._cached_text:
            return self._cached_text["all"]

        text_parts = []

        # Try pdfplumber first for better text extraction
        try:
            with pdfplumber.open(self.file_path) as pdf:
                for page in pdf.pages:
                    text = page.extract_text()
                    if text:
                        text_parts.append(text)
        except Exception as e:
            logger.warning(f"pdfplumber extraction failed, falling back to PyPDF2: {e}")
            # Fallback to PyPDF2
            with open(self.file_path, "rb") as file:
                pdf = PyPDF2.PdfReader(file)
                for page in pdf.pages:
                    text = page.extract_text()
                    if text:
                        text_parts.append(text)

        full_text = "\n\n".join(text_parts)
        self._cached_text["all"] = full_text
        return full_text

    def extract_text_range(self, start_page: int, end_page: int) -> str:
        """Extract text from page range."""
        cache_key = f"{start_page}-{end_page}"
        if cache_key in self._cached_text:
            return self._cached_text[cache_key]

        text_parts = []

        try:
            with pdfplumber.open(self.file_path) as pdf:
                for i in range(start_page, min(end_page + 1, len(pdf.pages))):
                    page = pdf.pages[i]
                    text = page.extract_text()
                    if text:
                        text_parts.append(text)
        except Exception as e:
            logger.error(f"Error extracting text range: {e}")

        result = "\n\n".join(text_parts)
        self._cached_text[cache_key] = result
        return result

    def extract_tables(
        self, page_range: Optional[Tuple[int, int]] = None, table_settings: Optional[Dict] = None
    ) -> List[pd.DataFrame]:
        """Extract tables from PDF pages.

        Args:
            page_range: Optional tuple of (start_page, end_page)
            table_settings: Optional tabula settings

        Returns:
            List of DataFrames containing table data
        """
        cache_key = str(page_range) if page_range else "all"
        if cache_key in self._cached_tables:
            return self._cached_tables[cache_key]

        tables = []

        # Default table settings
        if table_settings is None:
            table_settings = {
                "lattice": True,  # Use lattice mode for tables with lines
                "pages": "all" if not page_range else f"{page_range[0]+1}-{page_range[1]+1}",
                "pandas_options": {"header": 0},
            }

        try:
            # Try tabula for table extraction
            dfs = tabula.read_pdf(str(self.file_path), **table_settings)

            # Clean and process tables
            for df in dfs:
                if not df.empty:
                    # Clean column names
                    df.columns = [str(col).strip() for col in df.columns]
                    # Remove empty rows
                    df = df.dropna(how="all")
                    # Reset index
                    df = df.reset_index(drop=True)
                    tables.append(df)

        except Exception as e:
            logger.warning(f"Tabula extraction failed: {e}")

            # Fallback to pdfplumber
            try:
                with pdfplumber.open(self.file_path) as pdf:
                    if page_range:
                        pages = pdf.pages[page_range[0] : page_range[1] + 1]
                    else:
                        pages = pdf.pages

                    for page in pages:
                        page_tables = page.extract_tables()
                        for table in page_tables:
                            if table and len(table) > 1:
                                # Convert to DataFrame
                                df = pd.DataFrame(table[1:], columns=table[0])
                                # Clean
                                df = df.dropna(how="all")
                                df = df.reset_index(drop=True)
                                tables.append(df)

            except Exception as e2:
                logger.error(f"Both table extraction methods failed: {e2}")

        self._cached_tables[cache_key] = tables
        return tables

    def extract_all_tables(self) -> List[pd.DataFrame]:
        """Extract all tables from PDF."""
        return self.extract_tables()

    def find_table_by_keywords(
        self, keywords: List[str], context_lines: int = 5
    ) -> Optional[pd.DataFrame]:
        """Find table near keywords in text.

        Args:
            keywords: Keywords to search for
            context_lines: Lines of context to check around keywords

        Returns:
            DataFrame if table found, None otherwise
        """
        # Find pages with keywords
        relevant_pages = set()
        for keyword in keywords:
            pages = self.find_pages_with_keyword(keyword)
            relevant_pages.update(pages)

        if not relevant_pages:
            return None

        # Extract tables from relevant pages
        for page_num in sorted(relevant_pages):
            tables = self.extract_tables(page_range=(page_num, page_num))

            # Check if any table contains keywords
            for table in tables:
                table_str = table.to_string().lower()
                if any(keyword.lower() in table_str for keyword in keywords):
                    return table

        return None

    def extract_sections(self) -> Dict[str, str]:
        """Extract sections based on common headers."""
        sections = {}
        full_text = self.extract_all_text()

        # Common section patterns
        section_patterns = [
            r"(?:^|\n)(\d+\.?\s+[A-Z][^.\n]{10,50})\n",  # Numbered sections
            r"(?:^|\n)([A-Z][^.\n]{10,50})\n(?=\n)",  # Uppercase headers
            r"(?:^|\n)((?:Introduction|Methodology|Results|Discussion|Conclusion|Abstract|Summary|Executive Summary)[^.\n]*)\n",
        ]

        # Find all section headers
        headers = []
        for pattern in section_patterns:
            matches = re.finditer(pattern, full_text, re.MULTILINE)
            for match in matches:
                header = match.group(1).strip()
                start = match.end()
                headers.append((header, start))

        # Sort by position
        headers.sort(key=lambda x: x[1])

        # Extract section content
        for i, (header, start) in enumerate(headers):
            # Find end of section (start of next section or end of text)
            end = headers[i + 1][1] if i + 1 < len(headers) else len(full_text)

            # Extract content
            content = full_text[start:end].strip()

            # Clean header for use as key
            key = re.sub(r"^\d+\.?\s*", "", header)  # Remove numbering
            key = re.sub(r"[^\w\s]", "", key)  # Remove special chars
            key = key.strip().lower().replace(" ", "_")

            sections[key] = content

        return sections

    def extract_data_by_pattern(
        self, pattern: str, page_range: Optional[Tuple[int, int]] = None
    ) -> List[Dict[str, str]]:
        """Extract data matching regex pattern.

        Args:
            pattern: Regex pattern to match
            page_range: Optional page range to search

        Returns:
            List of dictionaries with matched data
        """
        if page_range:
            text = self.extract_text_range(page_range[0], page_range[1])
        else:
            text = self.extract_all_text()

        matches = []
        for match in re.finditer(pattern, text, re.MULTILINE | re.IGNORECASE):
            match_dict = {
                "match": match.group(0),
                "groups": match.groups(),
                "position": match.start(),
            }

            # Add named groups if present
            if match.groupdict():
                match_dict.update(match.groupdict())

            matches.append(match_dict)

        return matches

    def extract_numeric_data(
        self,
        keywords: List[str],
        value_pattern: str = r"([\d,]+\.?\d*)\s*(%|percent|million|billion|trillion)?",
    ) -> Dict[str, List[Tuple[float, str]]]:
        """Extract numeric data associated with keywords.

        Args:
            keywords: Keywords to search near numbers
            value_pattern: Regex pattern for numeric values

        Returns:
            Dictionary mapping keywords to list of (value, unit) tuples
        """
        text = self.extract_all_text()
        results = {}

        for keyword in keywords:
            results[keyword] = []

            # Find keyword occurrences
            keyword_pattern = re.compile(
                rf"{re.escape(keyword)}.{{0,100}}{value_pattern}", re.IGNORECASE
            )

            matches = keyword_pattern.finditer(text)
            for match in matches:
                try:
                    # Extract number and unit
                    number_str = match.group(1).replace(",", "")
                    number = float(number_str)
                    unit = match.group(2) if match.lastindex >= 2 else ""

                    results[keyword].append((number, unit))
                except ValueError:
                    continue

        return results
