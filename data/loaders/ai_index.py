"""Stanford HAI AI Index Report data loader with actual PDF extraction."""

import logging
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import pandas as pd

from config.settings import settings
from ..extractors.pdf_extractor_impl import EnhancedPDFExtractor
from ..models.adoption import AdoptionMetrics, GeographicAdoption, SectorAdoption
from .base import BaseDataLoader, DataSource

logger = logging.getLogger(__name__)


class AIIndexLoader(BaseDataLoader):
    """Loader for Stanford HAI AI Index Report data with real PDF extraction."""

    def __init__(self, file_path: Optional[Path] = None):
        """Initialize with AI Index report file path."""
        if file_path is None:
            # Default to AI Index 2025 report
            file_path = settings.get_resources_path() / "AI dashboard resources 1/hai_ai_index_report_2025.pdf"

        source = DataSource(
            name="Stanford HAI AI Index Report",
            version="2025",
            url="https://aiindex.stanford.edu/ai-index-report-2025/",
            file_path=file_path,
            citation="Stanford Human-Centered AI Institute. 'AI Index Report 2025.' Stanford University.",
        )
        super().__init__(source)

        # Initialize PDF extractor if file exists
        if self.source.file_path and self.source.file_path.exists():
            try:
                self.extractor = EnhancedPDFExtractor(self.source.file_path)
                logger.info(f"Initialized PDF extractor for {self.source.file_path.name}")
            except Exception as e:
                logger.error(f"Failed to initialize PDF extractor: {e}")
                self.extractor = None
        else:
            logger.warning(f"PDF file not found: {self.source.file_path}")
            self.extractor = None

    def load(self) -> Dict[str, pd.DataFrame]:
        """Load all datasets from AI Index report using actual PDF extraction."""
        logger.info(f"Loading data from {self.source.name} {self.source.version}")

        if not self.extractor:
            logger.warning("PDF extractor not available, returning empty datasets")
            return self._get_empty_datasets()

        datasets = {}

        # Extract different sections from the PDF
        try:
            # 1. Extract adoption trends data
            adoption_trends = self._extract_adoption_trends()
            if adoption_trends is not None and not adoption_trends.empty:
                datasets["adoption_trends"] = adoption_trends

            # 2. Extract sector adoption data
            sector_adoption = self._extract_sector_adoption()
            if sector_adoption is not None and not sector_adoption.empty:
                datasets["sector_adoption"] = sector_adoption

            # 3. Extract geographic adoption data
            geographic_adoption = self._extract_geographic_adoption()
            if geographic_adoption is not None and not geographic_adoption.empty:
                datasets["geographic_adoption"] = geographic_adoption

            # 4. Extract firm size adoption data
            firm_size_adoption = self._extract_firm_size_adoption()
            if firm_size_adoption is not None and not firm_size_adoption.empty:
                datasets["firm_size_adoption"] = firm_size_adoption

            # 5. Extract AI maturity data
            ai_maturity = self._extract_ai_maturity()
            if ai_maturity is not None and not ai_maturity.empty:
                datasets["ai_maturity"] = ai_maturity

            # 6. Extract investment trends
            investment_trends = self._extract_investment_trends()
            if investment_trends is not None and not investment_trends.empty:
                datasets["investment_trends"] = investment_trends

        except Exception as e:
            logger.error(f"Error during PDF extraction: {e}")
            # Return empty datasets on error
            return self._get_empty_datasets()

        # Validate all datasets
        if datasets:
            self.validate(datasets)
        else:
            logger.warning("No data extracted from PDF, using empty datasets")
            datasets = self._get_empty_datasets()

        return datasets

    def _extract_adoption_trends(self) -> Optional[pd.DataFrame]:
        """Extract AI adoption trends over time."""
        logger.info("Extracting adoption trends data...")

        try:
            # Look for adoption trends section
            # Common keywords in AI Index for adoption data
            keywords = ["adoption rate", "deployment", "implementation", "year-over-year", "growth"]

            # Find pages with adoption data
            adoption_pages = []
            for keyword in keywords:
                pages = self.extractor.find_pages_with_keyword(keyword)
                adoption_pages.extend(pages)

            adoption_pages = sorted(set(adoption_pages))[:10]  # Focus on first 10 relevant pages

            if not adoption_pages:
                logger.warning("No adoption trend pages found")
                return None

            # Extract tables from these pages
            tables = []
            for page in adoption_pages:
                page_tables = self.extractor.extract_tables(page_range=(page, page))
                tables.extend(page_tables)

            # Look for table with year and percentage columns
            adoption_df = None
            for table in tables:
                if table.empty:
                    continue

                # Check if table has year-like and percentage-like columns
                has_year = any(
                    "year" in str(col).lower() or bool(re.search(r"20\d{2}", str(col)))
                    for col in table.columns
                )

                has_percentage = any(
                    "%" in str(col) or "rate" in str(col).lower() or "adoption" in str(col).lower()
                    for col in table.columns
                )

                if has_year and has_percentage:
                    adoption_df = table
                    break

            if adoption_df is None:
                # Try extracting from text using patterns
                adoption_data = self._extract_adoption_from_text(adoption_pages)
                if adoption_data:
                    adoption_df = pd.DataFrame(adoption_data)

            if adoption_df is not None and not adoption_df.empty:
                # Clean and standardize column names
                adoption_df = self._clean_adoption_dataframe(adoption_df)
                logger.info(f"Extracted adoption trends with {len(adoption_df)} records")
                return adoption_df

        except Exception as e:
            logger.error(f"Error extracting adoption trends: {e}")

        return None

    def _extract_adoption_from_text(self, pages: List[int]) -> List[Dict]:
        """Extract adoption data from text using patterns."""
        adoption_data = []

        for page in pages[:5]:  # Check first 5 relevant pages
            text = self.extractor.extract_text_from_page(page)

            # Pattern for year and percentage pairs
            # Examples: "2024: 78%", "78% in 2024", "2024 (78%)"
            patterns = [
                r"(\d{4}):\s*(\d+(?:\.\d+)?)\s*%",
                r"(\d+(?:\.\d+)?)\s*%\s*in\s*(\d{4})",
                r"(\d{4})\s*\((\d+(?:\.\d+)?)\s*%\)",
                r"(\d{4})\s*-\s*(\d+(?:\.\d+)?)\s*%",
            ]

            for pattern in patterns:
                matches = re.findall(pattern, text)
                for match in matches:
                    try:
                        if pattern.startswith(r"(\d+(?:\.\d+)?)\s*%"):
                            # Percentage comes first
                            percentage, year = match
                        else:
                            # Year comes first
                            year, percentage = match

                        year = int(year)
                        percentage = float(percentage)

                        # Validate reasonable ranges
                        if 2010 <= year <= 2030 and 0 <= percentage <= 100:
                            adoption_data.append({"year": year, "adoption_rate": percentage})
                    except ValueError:
                        continue

        # Remove duplicates and sort by year
        seen = set()
        unique_data = []
        for item in sorted(adoption_data, key=lambda x: x["year"]):
            key = (item["year"], item["adoption_rate"])
            if key not in seen:
                seen.add(key)
                unique_data.append(item)

        return unique_data

    def _clean_adoption_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean and standardize adoption dataframe."""
        # Standardize column names
        df.columns = [col.lower().strip() for col in df.columns]

        # Identify year column
        year_col = None
        for col in df.columns:
            if "year" in col or bool(re.search(r"20\d{2}", str(df[col].iloc[0]))):
                year_col = col
                break

        # Identify adoption rate column
        rate_col = None
        for col in df.columns:
            if any(keyword in col for keyword in ["adoption", "rate", "deployment", "%"]):
                rate_col = col
                break

        if year_col and rate_col:
            # Create clean dataframe
            clean_df = pd.DataFrame(
                {
                    "year": pd.to_numeric(df[year_col], errors="coerce"),
                    "overall_adoption": pd.to_numeric(
                        df[rate_col].astype(str).str.replace("%", ""), errors="coerce"
                    ),
                }
            )

            # Remove invalid rows
            clean_df = clean_df.dropna()
            clean_df = clean_df[
                (clean_df["year"] >= 2010)
                & (clean_df["year"] <= 2030)
                & (clean_df["overall_adoption"] >= 0)
                & (clean_df["overall_adoption"] <= 100)
            ]

            # Sort by year
            clean_df = clean_df.sort_values("year").reset_index(drop=True)

            # Add additional columns if GenAI data is mentioned
            if "genai" in str(df).lower() or "generative" in str(df).lower():
                # Look for GenAI specific columns
                for col in df.columns:
                    if "genai" in col.lower() or "generative" in col.lower():
                        clean_df["genai_adoption"] = pd.to_numeric(
                            df[col].astype(str).str.replace("%", ""), errors="coerce"
                        )
                        break

            return clean_df

        return df

    def _extract_sector_adoption(self) -> Optional[pd.DataFrame]:
        """Extract sector/industry adoption data."""
        logger.info("Extracting sector adoption data...")

        try:
            # Keywords for finding sector data
            keywords = ["industry", "sector", "vertical", "by industry", "industry adoption"]

            # Find relevant pages
            sector_pages = []
            for keyword in keywords:
                pages = self.extractor.find_pages_with_keyword(keyword)
                sector_pages.extend(pages)

            sector_pages = sorted(set(sector_pages))[:10]

            if not sector_pages:
                return None

            # Look for sector tables
            sector_df = None
            for page in sector_pages:
                tables = self.extractor.extract_tables(page_range=(page, page))

                for table in tables:
                    if table.empty or len(table) < 3:
                        continue

                    # Check if table contains industry/sector names
                    table_str = table.to_string().lower()
                    sector_keywords = [
                        "technology",
                        "financial",
                        "healthcare",
                        "manufacturing",
                        "retail",
                    ]

                    if sum(1 for kw in sector_keywords if kw in table_str) >= 3:
                        sector_df = table
                        break

                if sector_df is not None:
                    break

            if sector_df is not None:
                # Clean and process sector data
                sector_df = self._clean_sector_dataframe(sector_df)
                logger.info(f"Extracted sector adoption data with {len(sector_df)} sectors")
                return sector_df

        except Exception as e:
            logger.error(f"Error extracting sector adoption: {e}")

        return None

    def _clean_sector_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean and standardize sector dataframe."""
        # Identify sector name column
        sector_col = None
        for col in df.columns:
            sample_values = df[col].astype(str).str.lower()
            if any(
                "technology" in val or "financial" in val or "healthcare" in val
                for val in sample_values
            ):
                sector_col = col
                break

        if not sector_col:
            return df

        # Identify adoption rate column
        rate_cols = []
        for col in df.columns:
            if col == sector_col:
                continue
            # Check if column contains numeric values (likely percentages)
            try:
                numeric_vals = pd.to_numeric(
                    df[col].astype(str).str.replace("%", "").str.replace(",", ""), errors="coerce"
                )
                if numeric_vals.notna().sum() > len(df) * 0.5:
                    rate_cols.append(col)
            except:
                continue

        if sector_col and rate_cols:
            # Create clean dataframe
            clean_df = pd.DataFrame(
                {
                    "sector": df[sector_col],
                    "adoption_rate": pd.to_numeric(
                        df[rate_cols[0]].astype(str).str.replace("%", "").str.replace(",", ""),
                        errors="coerce",
                    ),
                }
            )

            # Add additional rate columns if available
            if len(rate_cols) > 1:
                clean_df["genai_adoption"] = pd.to_numeric(
                    df[rate_cols[1]].astype(str).str.replace("%", "").str.replace(",", ""),
                    errors="coerce",
                )

            # Clean sector names
            clean_df["sector"] = clean_df["sector"].str.strip().str.title()

            # Remove invalid rows
            clean_df = clean_df.dropna(subset=["sector", "adoption_rate"])
            clean_df = clean_df[
                (clean_df["adoption_rate"] >= 0) & (clean_df["adoption_rate"] <= 100)
            ]

            # Add year
            clean_df["year"] = 2025

            return clean_df.reset_index(drop=True)

        return df

    def _extract_geographic_adoption(self) -> Optional[pd.DataFrame]:
        """Extract geographic adoption data."""
        logger.info("Extracting geographic adoption data...")

        try:
            # Keywords for geographic data
            keywords = ["geographic", "regional", "country", "state", "city", "location"]

            # Find relevant pages
            geo_pages = []
            for keyword in keywords:
                pages = self.extractor.find_pages_with_keyword(keyword)
                geo_pages.extend(pages)

            geo_pages = sorted(set(geo_pages))[:10]

            if not geo_pages:
                return None

            # Extract tables from geographic pages
            for page in geo_pages:
                tables = self.extractor.extract_tables(page_range=(page, page))

                for table in tables:
                    if table.empty:
                        continue

                    # Check if table contains location data
                    table_str = table.to_string().lower()
                    if any(
                        loc in table_str
                        for loc in ["united states", "china", "europe", "california", "new york"]
                    ):
                        # Process geographic table
                        geo_df = self._clean_geographic_dataframe(table)
                        if geo_df is not None and not geo_df.empty:
                            logger.info(f"Extracted geographic data with {len(geo_df)} locations")
                            return geo_df

        except Exception as e:
            logger.error(f"Error extracting geographic adoption: {e}")

        return None

    def _clean_geographic_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean and standardize geographic dataframe."""
        # Similar cleaning logic as sector dataframe
        # but looking for location names and adoption rates

        location_col = None
        for col in df.columns:
            sample_values = df[col].astype(str).str.lower()
            if any(
                loc in " ".join(sample_values)
                for loc in ["state", "country", "city", "united", "china"]
            ):
                location_col = col
                break

        if not location_col:
            return None

        # Find numeric columns
        rate_col = None
        for col in df.columns:
            if col == location_col:
                continue
            try:
                numeric_vals = pd.to_numeric(
                    df[col].astype(str).str.replace("%", "").str.replace(",", ""), errors="coerce"
                )
                if numeric_vals.notna().sum() > len(df) * 0.5:
                    rate_col = col
                    break
            except:
                continue

        if location_col and rate_col:
            clean_df = pd.DataFrame(
                {
                    "location": df[location_col].str.strip(),
                    "adoption_rate": pd.to_numeric(
                        df[rate_col].astype(str).str.replace("%", "").str.replace(",", ""),
                        errors="coerce",
                    ),
                    "year": 2025,
                }
            )

            # Remove invalid rows
            clean_df = clean_df.dropna()
            clean_df = clean_df[
                (clean_df["adoption_rate"] >= 0) & (clean_df["adoption_rate"] <= 100)
            ]

            return clean_df.reset_index(drop=True)

        return None

    def _extract_firm_size_adoption(self) -> Optional[pd.DataFrame]:
        """Extract firm size adoption data."""
        logger.info("Extracting firm size adoption data...")

        try:
            # Keywords for firm size data
            keywords = [
                "firm size",
                "company size",
                "employee",
                "small business",
                "enterprise",
                "SMB",
            ]

            # Find relevant pages
            size_pages = []
            for keyword in keywords:
                pages = self.extractor.find_pages_with_keyword(keyword)
                size_pages.extend(pages)

            size_pages = sorted(set(size_pages))[:10]

            if not size_pages:
                return None

            # Look for firm size tables
            for page in size_pages:
                tables = self.extractor.extract_tables(page_range=(page, page))

                for table in tables:
                    if table.empty:
                        continue

                    # Check if table contains size categories
                    table_str = table.to_string().lower()
                    size_indicators = [
                        "employee",
                        "<50",
                        "50-",
                        "250-",
                        "1000",
                        "5000",
                        "small",
                        "medium",
                        "large",
                    ]

                    if sum(1 for ind in size_indicators if ind in table_str) >= 2:
                        # Process firm size table
                        size_df = self._clean_firm_size_dataframe(table)
                        if size_df is not None and not size_df.empty:
                            logger.info(f"Extracted firm size data with {len(size_df)} categories")
                            return size_df

        except Exception as e:
            logger.error(f"Error extracting firm size adoption: {e}")

        return None

    def _clean_firm_size_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean and standardize firm size dataframe."""
        # Look for size category column
        size_col = None
        for col in df.columns:
            col_values = df[col].astype(str)
            if any(
                val
                for val in col_values
                if any(
                    size in val for size in ["<", ">", "-", "employee", "small", "medium", "large"]
                )
            ):
                size_col = col
                break

        if not size_col:
            return None

        # Find adoption rate column
        rate_col = None
        for col in df.columns:
            if col == size_col:
                continue
            try:
                numeric_vals = pd.to_numeric(
                    df[col].astype(str).str.replace("%", "").str.replace(",", ""), errors="coerce"
                )
                if numeric_vals.notna().sum() > len(df) * 0.5:
                    rate_col = col
                    break
            except:
                continue

        if size_col and rate_col:
            clean_df = pd.DataFrame(
                {
                    "firm_size": df[size_col].str.strip(),
                    "adoption_rate": pd.to_numeric(
                        df[rate_col].astype(str).str.replace("%", "").str.replace(",", ""),
                        errors="coerce",
                    ),
                }
            )

            # Remove invalid rows
            clean_df = clean_df.dropna()
            clean_df = clean_df[
                (clean_df["adoption_rate"] >= 0) & (clean_df["adoption_rate"] <= 100)
            ]

            return clean_df.reset_index(drop=True)

        return None

    def _extract_ai_maturity(self) -> Optional[pd.DataFrame]:
        """Extract AI maturity data."""
        logger.info("Extracting AI maturity data...")

        try:
            # Keywords for maturity data
            keywords = [
                "maturity",
                "stage",
                "phase",
                "journey",
                "adoption stage",
                "implementation phase",
            ]

            # Find relevant pages
            maturity_pages = []
            for keyword in keywords:
                pages = self.extractor.find_pages_with_keyword(keyword)
                maturity_pages.extend(pages)

            maturity_pages = sorted(set(maturity_pages))[:10]

            if not maturity_pages:
                return None

            # Extract maturity data from tables or text
            for page in maturity_pages:
                tables = self.extractor.extract_tables(page_range=(page, page))

                for table in tables:
                    if table.empty:
                        continue

                    # Check for maturity stages
                    table_str = table.to_string().lower()
                    maturity_keywords = [
                        "exploring",
                        "experimenting",
                        "pilot",
                        "scaling",
                        "transform",
                        "mature",
                    ]

                    if sum(1 for kw in maturity_keywords if kw in table_str) >= 2:
                        # Process maturity table
                        maturity_df = self._clean_maturity_dataframe(table)
                        if maturity_df is not None and not maturity_df.empty:
                            logger.info(f"Extracted maturity data with {len(maturity_df)} stages")
                            return maturity_df

        except Exception as e:
            logger.error(f"Error extracting AI maturity: {e}")

        return None

    def _clean_maturity_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean and standardize maturity dataframe."""
        # Similar approach - identify maturity level column and percentage column
        maturity_col = None
        for col in df.columns:
            col_values = df[col].astype(str).str.lower()
            if any(
                val
                for val in col_values
                if any(
                    stage in val for stage in ["explor", "experiment", "pilot", "scal", "transform"]
                )
            ):
                maturity_col = col
                break

        if not maturity_col:
            return None

        # Find percentage column
        pct_col = None
        for col in df.columns:
            if col == maturity_col:
                continue
            try:
                numeric_vals = pd.to_numeric(
                    df[col].astype(str).str.replace("%", "").str.replace(",", ""), errors="coerce"
                )
                if numeric_vals.notna().sum() > len(df) * 0.5:
                    pct_col = col
                    break
            except:
                continue

        if maturity_col and pct_col:
            clean_df = pd.DataFrame(
                {
                    "maturity_level": df[maturity_col].str.strip().str.title(),
                    "percentage_of_firms": pd.to_numeric(
                        df[pct_col].astype(str).str.replace("%", "").str.replace(",", ""),
                        errors="coerce",
                    ),
                }
            )

            # Remove invalid rows
            clean_df = clean_df.dropna()
            clean_df = clean_df[
                (clean_df["percentage_of_firms"] >= 0) & (clean_df["percentage_of_firms"] <= 100)
            ]

            return clean_df.reset_index(drop=True)

        return None

    def _extract_investment_trends(self) -> Optional[pd.DataFrame]:
        """Extract AI investment trends data."""
        logger.info("Extracting investment trends data...")

        try:
            # Keywords for investment data
            keywords = ["investment", "funding", "venture capital", "billion", "million", "capital"]

            # Find relevant pages
            investment_pages = []
            for keyword in keywords:
                pages = self.extractor.find_pages_with_keyword(keyword)
                investment_pages.extend(pages)

            investment_pages = sorted(set(investment_pages))[:10]

            if not investment_pages:
                return None

            # Extract investment data
            investment_data = []
            for page in investment_pages[:5]:
                text = self.extractor.extract_text_from_page(page)

                # Pattern for investment amounts with years
                # Examples: "$252.3 billion in 2024", "2024: $252.3B"
                patterns = [
                    r"(\d{4}):\s*\$(\d+(?:\.\d+)?)\s*(billion|million|B|M)",
                    r"\$(\d+(?:\.\d+)?)\s*(billion|million|B|M)\s*in\s*(\d{4})",
                    r"(\d{4})\s*.*?\$(\d+(?:\.\d+)?)\s*(billion|million|B|M)",
                ]

                for pattern in patterns:
                    matches = re.findall(pattern, text, re.IGNORECASE)
                    for match in matches:
                        try:
                            if pattern.startswith(r"\$"):
                                # Amount comes first
                                amount, unit, year = match
                            else:
                                # Year comes first
                                year, amount, unit = match

                            year = int(year)
                            amount = float(amount)

                            # Convert to billions
                            if unit.lower() in ["million", "m"]:
                                amount = amount / 1000

                            if 2010 <= year <= 2030 and amount > 0:
                                investment_data.append(
                                    {"year": year, "global_investment_billions": amount}
                                )
                        except ValueError:
                            continue

            if investment_data:
                # Create dataframe and remove duplicates
                investment_df = pd.DataFrame(investment_data)
                investment_df = (
                    investment_df.groupby("year")
                    .agg({"global_investment_billions": "max"})  # Take max value for each year
                    .reset_index()
                )
                investment_df = investment_df.sort_values("year")

                logger.info(f"Extracted investment trends with {len(investment_df)} years")
                return investment_df

        except Exception as e:
            logger.error(f"Error extracting investment trends: {e}")

        return None

    def validate(self, data: Dict[str, pd.DataFrame]) -> bool:
        """Validate loaded data meets expected schema."""
        # At minimum, we need some data
        if not data:
            raise ValueError("No data extracted from PDF")

        # Log what we have
        logger.info(f"Extracted datasets: {list(data.keys())}")

        # Validate individual datasets if present
        if "adoption_trends" in data:
            trends = data["adoption_trends"]
            if "year" not in trends.columns:
                raise ValueError("Adoption trends missing 'year' column")
            if not any(
                col for col in trends.columns if "adoption" in col.lower() or "rate" in col.lower()
            ):
                raise ValueError("Adoption trends missing adoption rate column")

        if "sector_adoption" in data:
            sectors = data["sector_adoption"]
            if "sector" not in sectors.columns:
                raise ValueError("Sector adoption missing 'sector' column")

        logger.info("Data validation passed")
        return True

    def _get_empty_datasets(self) -> Dict[str, pd.DataFrame]:
        """Return empty datasets with correct schema."""
        return {
            "adoption_trends": pd.DataFrame(columns=["year", "overall_adoption", "genai_adoption"]),
            "sector_adoption": pd.DataFrame(columns=["sector", "year", "adoption_rate"]),
            "geographic_adoption": pd.DataFrame(columns=["location", "year", "adoption_rate"]),
            "firm_size_adoption": pd.DataFrame(columns=["firm_size", "adoption_rate"]),
            "ai_maturity": pd.DataFrame(columns=["maturity_level", "percentage_of_firms"]),
            "investment_trends": pd.DataFrame(columns=["year", "global_investment_billions"]),
        }
