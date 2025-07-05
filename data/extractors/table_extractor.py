"""Table extraction from PDF documents."""

import logging
from typing import Any, Dict, List, Optional

import pandas as pd

from .base import PDFExtractor

logger = logging.getLogger(__name__)


class TableExtractor:
    """Extract tables from PDF documents."""

    def __init__(self, pdf_extractor: Optional[PDFExtractor] = None):
        """Initialize table extractor.

        Args:
            pdf_extractor: Optional PDF extractor instance
        """
        self.pdf_extractor = pdf_extractor

    def extract_tables(self, page_num: Optional[int] = None) -> List[pd.DataFrame]:
        """Extract tables from PDF pages.

        Args:
            page_num: Optional specific page number

        Returns:
            List of pandas DataFrames containing table data
        """
        tables = []

        # This is a basic implementation that relies on the PDF extractor
        if self.pdf_extractor:
            try:
                # Try using the PDF extractor's table extraction if available
                if hasattr(self.pdf_extractor, "extract_tables"):
                    tables = self.pdf_extractor.extract_tables(page_num)
            except Exception as e:
                logger.warning(f"Error extracting tables: {e}")

        logger.info(f"Extracted {len(tables)} tables from page: {page_num if page_num else 'all'}")
        return tables

    def extract_table_with_headers(self, page_num: int) -> Optional[pd.DataFrame]:
        """Extract a table and attempt to identify headers.

        Args:
            page_num: Page number to extract from

        Returns:
            DataFrame with headers if found, None otherwise
        """
        tables = self.extract_tables(page_num)

        if tables:
            # Return the first table found
            # In a full implementation, this would include
            # logic to identify and set proper headers
            return tables[0]

        return None

    def merge_split_tables(self, tables: List[pd.DataFrame]) -> pd.DataFrame:
        """Merge tables that were split across pages.

        Args:
            tables: List of DataFrames to merge

        Returns:
            Merged DataFrame
        """
        if not tables:
            return pd.DataFrame()

        if len(tables) == 1:
            return tables[0]

        # Simple concatenation - a full implementation would
        # handle column alignment and deduplication
        try:
            return pd.concat(tables, ignore_index=True)
        except Exception as e:
            logger.error(f"Error merging tables: {e}")
            return tables[0]  # Return first table as fallback
