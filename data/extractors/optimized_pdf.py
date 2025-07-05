"""Optimized PDF extractor with lazy loading and caching."""

import hashlib
import io
import logging
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

import pandas as pd

from data.extractors.pdf import PDFExtractor
from performance.cache_manager import CacheKeyGenerator, get_cache
from performance.monitor import PerformanceContext, track_performance

logger = logging.getLogger(__name__)


class OptimizedPDFExtractor(PDFExtractor):
    """Optimized PDF extractor with performance enhancements."""

    def __init__(
        self, file_path: Union[str, Path], cache_enabled: bool = True, max_workers: int = 2
    ):
        """Initialize optimized PDF extractor.

        Args:
            file_path: Path to PDF file
            cache_enabled: Enable caching
            max_workers: Max workers for parallel processing
        """
        super().__init__(file_path)
        self.cache_enabled = cache_enabled
        self.cache = get_cache() if cache_enabled else None
        self.max_workers = max_workers

        # Lazy loading
        self._metadata = None
        self._page_cache = {}
        self._text_cache = {}
        self._table_cache = {}

        # File hash for cache invalidation
        self._file_hash = None

    def _get_file_hash(self) -> str:
        """Get file hash for cache key generation."""
        if self._file_hash is None:
            # Calculate file hash
            hash_md5 = hashlib.md5()
            with open(self.file_path, "rb") as f:
                # Read in chunks to handle large files
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_md5.update(chunk)
            self._file_hash = hash_md5.hexdigest()
        return self._file_hash

    @track_performance("pdf_metadata", threshold=0.1)
    def get_metadata(self) -> Dict[str, Any]:
        """Get PDF metadata without loading full content."""
        if self._metadata is not None:
            return self._metadata

        # Check cache
        if self.cache_enabled:
            cache_key = f"pdf_meta:{self._get_file_hash()}"
            cached = self.cache.get(cache_key)
            if cached:
                self._metadata = cached
                return cached

        # Extract metadata
        try:
            with open(self.file_path, "rb") as file:
                reader = PyPDF2.PdfReader(file)

                self._metadata = {
                    "pages": len(reader.pages),
                    "title": (
                        reader.metadata.get("/Title", "Unknown") if reader.metadata else "Unknown"
                    ),
                    "author": (
                        reader.metadata.get("/Author", "Unknown") if reader.metadata else "Unknown"
                    ),
                    "subject": reader.metadata.get("/Subject", "") if reader.metadata else "",
                    "creator": reader.metadata.get("/Creator", "") if reader.metadata else "",
                    "file_size": Path(self.file_path).stat().st_size,
                    "file_hash": self._get_file_hash(),
                }

                # Cache metadata
                if self.cache_enabled:
                    self.cache.set(cache_key, self._metadata, memory_ttl=3600)

                return self._metadata

        except Exception as e:
            logger.error(f"Error extracting metadata: {e}")
            return {}

    @track_performance("pdf_extract_text", threshold=2.0)
    def extract_text(
        self, start_page: Optional[int] = None, end_page: Optional[int] = None, lazy: bool = True
    ) -> str:
        """Extract text from PDF with lazy loading option.

        Args:
            start_page: Starting page (0-indexed)
            end_page: Ending page (exclusive)
            lazy: Use lazy loading for individual pages

        Returns:
            Extracted text
        """
        metadata = self.get_metadata()
        total_pages = metadata.get("pages", 0)

        if total_pages == 0:
            return ""

        # Determine page range
        start = start_page or 0
        end = min(end_page or total_pages, total_pages)

        # Check if full text is cached
        if start == 0 and end == total_pages and self.cache_enabled:
            cache_key = f"pdf_text:{self._get_file_hash()}:full"
            cached = self.cache.get(cache_key)
            if cached:
                return cached

        # Extract text
        if lazy:
            # Lazy extraction - load pages as needed
            text_parts = []
            for page_num in range(start, end):
                page_text = self._extract_page_text_lazy(page_num)
                text_parts.append(page_text)

            full_text = "\n".join(text_parts)
        else:
            # Extract all at once
            full_text = self._extract_text_range(start, end)

        # Cache if full document
        if start == 0 and end == total_pages and self.cache_enabled:
            cache_key = f"pdf_text:{self._get_file_hash()}:full"
            self.cache.set(cache_key, full_text, disk_only=True, disk_ttl=3600)

        return full_text

    def _extract_page_text_lazy(self, page_num: int) -> str:
        """Extract text from a single page with caching."""
        # Check page cache
        if page_num in self._text_cache:
            return self._text_cache[page_num]

        # Check disk cache
        if self.cache_enabled:
            cache_key = f"pdf_page:{self._get_file_hash()}:{page_num}"
            cached = self.cache.get(cache_key)
            if cached:
                self._text_cache[page_num] = cached
                return cached

        # Extract page
        with PerformanceContext(f"extract_page_{page_num}"):
            try:
                with open(self.file_path, "rb") as file:
                    reader = PyPDF2.PdfReader(file)
                    page = reader.pages[page_num]
                    text = page.extract_text()

                # Cache result
                self._text_cache[page_num] = text
                if self.cache_enabled:
                    cache_key = f"pdf_page:{self._get_file_hash()}:{page_num}"
                    self.cache.set(cache_key, text, memory_ttl=600)

                return text

            except Exception as e:
                logger.error(f"Error extracting page {page_num}: {e}")
                return ""

    def _extract_text_range(self, start: int, end: int) -> str:
        """Extract text from page range."""
        try:
            with open(self.file_path, "rb") as file:
                reader = PyPDF2.PdfReader(file)
                text_parts = []

                for page_num in range(start, end):
                    page = reader.pages[page_num]
                    text_parts.append(page.extract_text())

                return "\n".join(text_parts)

        except Exception as e:
            logger.error(f"Error extracting text range: {e}")
            return ""

    @track_performance("pdf_extract_tables", threshold=3.0)
    def extract_tables(
        self, pages: Optional[Union[str, List[int]]] = None, parallel: bool = True
    ) -> List[pd.DataFrame]:
        """Extract tables from PDF with parallel processing.

        Args:
            pages: Page numbers to extract from
            parallel: Use parallel processing

        Returns:
            List of DataFrames
        """
        # Check cache
        if self.cache_enabled:
            cache_key = f"pdf_tables:{self._get_file_hash()}:{pages}"
            cached = self.cache.get(cache_key)
            if cached:
                return cached

        # Determine pages
        if pages is None:
            metadata = self.get_metadata()
            pages = list(range(metadata.get("pages", 0)))
        elif pages == "all":
            metadata = self.get_metadata()
            pages = list(range(metadata.get("pages", 0)))
        elif isinstance(pages, int):
            pages = [pages]

        # Extract tables
        if parallel and len(pages) > 1:
            tables = self._extract_tables_parallel(pages)
        else:
            tables = self._extract_tables_sequential(pages)

        # Cache result
        if self.cache_enabled:
            cache_key = f"pdf_tables:{self._get_file_hash()}:{pages}"
            self.cache.set(cache_key, tables, disk_only=True, disk_ttl=3600)

        return tables

    def _extract_tables_parallel(self, pages: List[int]) -> List[pd.DataFrame]:
        """Extract tables from multiple pages in parallel."""
        all_tables = []

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Submit tasks
            futures = {executor.submit(self._extract_page_tables, page): page for page in pages}

            # Collect results
            for future in futures:
                try:
                    page_tables = future.result()
                    all_tables.extend(page_tables)
                except Exception as e:
                    page = futures[future]
                    logger.error(f"Error extracting tables from page {page}: {e}")

        return all_tables

    def _extract_tables_sequential(self, pages: List[int]) -> List[pd.DataFrame]:
        """Extract tables sequentially."""
        all_tables = []

        for page in pages:
            try:
                page_tables = self._extract_page_tables(page)
                all_tables.extend(page_tables)
            except Exception as e:
                logger.error(f"Error extracting tables from page {page}: {e}")

        return all_tables

    def _extract_page_tables(self, page_num: int) -> List[pd.DataFrame]:
        """Extract tables from a single page."""
        # Check cache
        if page_num in self._table_cache:
            return self._table_cache[page_num]

        try:
            # Use camelot for better table extraction
            tables = camelot.read_pdf(
                str(self.file_path),
                pages=str(page_num + 1),  # camelot uses 1-based indexing
                flavor="stream",
                suppress_stdout=True,
            )

            # Convert to DataFrames
            dataframes = [table.df for table in tables]

            # Cache result
            self._table_cache[page_num] = dataframes

            return dataframes

        except Exception as e:
            logger.debug(f"Camelot failed for page {page_num}, trying tabula: {e}")

            # Fallback to tabula
            try:
                tables = tabula.read_pdf(
                    self.file_path,
                    pages=page_num + 1,
                    multiple_tables=True,
                    pandas_options={"header": None},
                )

                # Cache result
                self._table_cache[page_num] = tables

                return tables

            except Exception as e2:
                logger.error(f"Table extraction failed for page {page_num}: {e2}")
                return []

    def extract_text_chunks(self, chunk_size: int = 1000) -> List[str]:
        """Extract text in chunks for better memory usage.

        Args:
            chunk_size: Size of each chunk in characters

        Returns:
            List of text chunks
        """
        full_text = self.extract_text()

        # Split into chunks
        chunks = []
        for i in range(0, len(full_text), chunk_size):
            chunk = full_text[i : i + chunk_size]
            chunks.append(chunk)

        return chunks

    def search_text(self, query: str, case_sensitive: bool = False) -> List[Dict[str, Any]]:
        """Search for text in PDF with page references.

        Args:
            query: Search query
            case_sensitive: Case sensitive search

        Returns:
            List of matches with page numbers
        """
        matches = []
        metadata = self.get_metadata()

        # Search each page
        for page_num in range(metadata.get("pages", 0)):
            page_text = self._extract_page_text_lazy(page_num)

            # Search in page
            if not case_sensitive:
                search_text = page_text.lower()
                search_query = query.lower()
            else:
                search_text = page_text
                search_query = query

            if search_query in search_text:
                # Find all occurrences
                start = 0
                while True:
                    pos = search_text.find(search_query, start)
                    if pos == -1:
                        break

                    # Get context
                    context_start = max(0, pos - 50)
                    context_end = min(len(page_text), pos + len(query) + 50)
                    context = page_text[context_start:context_end]

                    matches.append(
                        {
                            "page": page_num + 1,  # 1-based for user display
                            "position": pos,
                            "context": context,
                            "query": query,
                        }
                    )

                    start = pos + 1

        return matches

    def clear_cache(self) -> None:
        """Clear all cached data for this PDF."""
        self._page_cache.clear()
        self._text_cache.clear()
        self._table_cache.clear()
        self._metadata = None

        # Clear from global cache
        if self.cache_enabled:
            file_hash = self._get_file_hash()
            # Clear known cache keys
            for prefix in ["pdf_meta", "pdf_text", "pdf_page", "pdf_tables"]:
                self.cache.delete(f"{prefix}:{file_hash}")


# Import required libraries with error handling
try:
    import PyPDF2
except ImportError:
    logger.warning("PyPDF2 not available")
    PyPDF2 = None

try:
    import camelot
except ImportError:
    logger.warning("camelot-py not available")
    camelot = None

try:
    import tabula
except ImportError:
    logger.warning("tabula-py not available")
    tabula = None
