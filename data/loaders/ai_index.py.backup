"""Stanford HAI AI Index Report data loader with actual PDF extraction."""

import logging
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

import pandas as pd

from config.settings import settings

from ..extractors.pdf_extractor import PDFExtractor
from ..models.adoption import AdoptionMetrics, GeographicAdoption, SectorAdoption
from .base import BaseDataLoader, DataSource

logger = logging.getLogger(__name__)


class AIIndexLoader(BaseDataLoader):
    """Loader for Stanford HAI AI Index Report data with real PDF extraction."""

    def __init__(self, file_path: Optional[Path] = None):
        if file_path is None:
            file_path = (
                settings.get_resources_path()
                / "AI dashboard resources 1/hai_ai_index_report_2025.pdf"
            )
        source = DataSource(
            name="Stanford HAI AI Index Report",
            version="2025",
            url="https://aiindex.stanford.edu/ai-index-report-2025/",
            file_path=file_path,
            citation="Stanford Human-Centered AI Institute. 'AI Index Report 2025.' Stanford University.",
        )
        super().__init__(source)
        if self.source.file_path and self.source.file_path.exists():
            try:
                self.extractor = PDFExtractor(self.source.file_path)
                logger.info(f"Initialized PDF extractor for {self.source.file_path.name}")
            except Exception as e:
                logger.error(f"Failed to initialize PDF extractor: {e}")
                self.extractor = None
        else:
            logger.warning(f"PDF file not found: {self.source.file_path}")
            self.extractor = None

    def load(self) -> Dict[str, pd.DataFrame]:
        logger.info(f"Loading data from {self.source.name} {self.source.version}")
        if not self.extractor:
            logger.warning("PDF extractor not available, returning empty datasets")
            return self._get_empty_datasets()
        datasets = {}
        try:
            datasets["adoption_trends"] = self._extract_adoption_trends() or pd.DataFrame()
            datasets["sector_adoption"] = self._extract_sector_adoption() or pd.DataFrame()
            datasets["geographic_adoption"] = self._extract_geographic_adoption() or pd.DataFrame()
            datasets["firm_size_adoption"] = self._extract_firm_size_adoption() or pd.DataFrame()
            datasets["ai_maturity"] = self._extract_ai_maturity() or pd.DataFrame()
            datasets["investment_trends"] = self._extract_investment_trends() or pd.DataFrame()
        except Exception as e:
            logger.error(f"Error during PDF extraction: {e}")
            return self._get_empty_datasets()
        if datasets:
            self.validate(datasets)
        else:
            logger.warning("No data extracted from PDF, using empty datasets")
            datasets = self._get_empty_datasets()
        return datasets

    def _extract_adoption_trends(self) -> Optional[pd.DataFrame]:
        logger.info("Extracting adoption trends data...")
        try:
            keywords = ["adoption rate", "deployment", "implementation", "year-over-year", "growth"]
            adoption_pages = []
            for keyword in keywords:
                adoption_pages.extend(self.extractor.find_pages_with_keyword(keyword))
            adoption_pages = sorted(set(adoption_pages))[:10]
            if not adoption_pages:
                logger.warning("No adoption trend pages found")
                return None
            tables = []
            for page in adoption_pages:
                tables.extend(self.extractor.extract_tables(page_range=(page, page)))
            adoption_df = None
            for table in tables:
                if table.empty:
                    continue
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
                adoption_data = self._extract_adoption_from_text(adoption_pages)
                if adoption_data:
                    adoption_df = pd.DataFrame(adoption_data)
            if adoption_df is not None and not adoption_df.empty:
                adoption_df = self._clean_adoption_dataframe(adoption_df)
                logger.info(f"Extracted adoption trends with {len(adoption_df)} records")
                return adoption_df
        except Exception as e:
            logger.error(f"Error extracting adoption trends: {e}")
        return None

    def _extract_adoption_from_text(self, pages: List[int]) -> List[Dict]:
        adoption_data = []
        for page in pages[:5]:
            text = self.extractor.extract_text_from_page(page)
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
                            percentage, year = match
                        else:
                            year, percentage = match
                        year = int(year)
                        percentage = float(percentage)
                        if 2010 <= year <= 2030 and 0 <= percentage <= 100:
                            adoption_data.append({"year": year, "adoption_rate": percentage})
                    except ValueError:
                        continue
        seen = set()
        unique_data = []
        for item in sorted(adoption_data, key=lambda x: x["year"]):
            key = (item["year"], item["adoption_rate"])
            if key not in seen:
                seen.add(key)
                unique_data.append(item)
        return unique_data

    def _clean_adoption_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        df.columns = [col.lower().strip() for col in df.columns]
        year_col = None
        for col in df.columns:
            if "year" in col or bool(re.search(r"20\d{2}", str(df[col].iloc[0]))):
                year_col = col
                break
        rate_col = None
        for col in df.columns:
            if any(keyword in col for keyword in ["adoption", "rate", "deployment", "%"]):
                rate_col = col
                break
        if year_col and rate_col:
            clean_df = pd.DataFrame(
                {
                    "year": pd.to_numeric(df[year_col], errors="coerce"),
                    "overall_adoption": pd.to_numeric(
                        df[rate_col].astype(str).str.replace("%", ""), errors="coerce"
                    ),
                }
            )
            clean_df = clean_df.dropna()
            clean_df = clean_df[
                (clean_df["year"] >= 2010)
                & (clean_df["year"] <= 2030)
                & (clean_df["overall_adoption"] >= 0)
                & (clean_df["overall_adoption"] <= 100)
            ]
            clean_df = clean_df.sort_values("year").reset_index(drop=True)
            if "genai" in str(df).lower() or "generative" in str(df).lower():
                for col in df.columns:
                    if "genai" in col.lower() or "generative" in col.lower():
                        clean_df["genai_adoption"] = pd.to_numeric(
                            df[col].astype(str).str.replace("%", ""), errors="coerce"
                        )
                        break
            return clean_df
        return df

    def _extract_sector_adoption(self) -> Optional[pd.DataFrame]:
        logger.info("Extracting sector adoption data...")
        try:
            keywords = ["industry", "sector", "vertical", "by industry", "industry adoption"]
            sector_pages = []
            for keyword in keywords:
                sector_pages.extend(self.extractor.find_pages_with_keyword(keyword))
            sector_pages = sorted(set(sector_pages))[:10]
            if not sector_pages:
                return None
            sector_df = None
            for page in sector_pages:
                tables = self.extractor.extract_tables(page_range=(page, page))
                for table in tables:
                    if table.empty or len(table) < 3:
                        continue
                    table_str = table.to_string().lower()
                    sector_keywords = [
                        "technology", "financial", "healthcare", "manufacturing", "retail"
                    ]
                    if sum(1 for kw in sector_keywords if kw in table_str) >= 3:
                        sector_df = table
                        break
                if sector_df is not None:
                    break
            if sector_df is not None:
                sector_df = self._clean_sector_dataframe(sector_df)
                logger.info(f"Extracted sector adoption data with {len(sector_df)} sectors")
                return sector_df
        except Exception as e:
            logger.error(f"Error extracting sector adoption: {e}")
        return None

    def _clean_sector_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
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
        rate_cols = []
        for col in df.columns:
            if col == sector_col:
                continue
            try:
                numeric_vals = pd.to_numeric(
                    df[col].astype(str).str.replace("%", "").str.replace(",", ""), errors="coerce"
                )
                if numeric_vals.notna().sum() > len(df) * 0.5:
                    rate_cols.append(col)
            except:
                continue
        if sector_col and rate_cols:
            clean_df = pd.DataFrame(
                {
                    "sector": df[sector_col],
                    "adoption_rate": pd.to_numeric(
                        df[rate_cols[0]].astype(str).str.replace("%", "").str.replace(",", ""),
                        errors="coerce",
                    ),
                }
            )
            if len(rate_cols) > 1:
                clean_df["genai_adoption"] = pd.to_numeric(
                    df[rate_cols[1]].astype(str).str.replace("%", "").str.replace(",", ""),
                    errors="coerce",
                )
            clean_df["sector"] = clean_df["sector"].str.strip().str.title()
            clean_df = clean_df.dropna(subset=["sector", "adoption_rate"])
            clean_df = clean_df[
                (clean_df["adoption_rate"] >= 0) & (clean_df["adoption_rate"] <= 100)
            ]
            clean_df["year"] = 2025
            return clean_df.reset_index(drop=True)
        return df

    def _extract_geographic_adoption(self) -> Optional[pd.DataFrame]:
        logger.info("Extracting geographic adoption data...")
        try:
            keywords = ["geographic", "regional", "country", "state", "city", "location"]
            geo_pages = []
            for keyword in keywords:
                geo_pages.extend(self.extractor.find_pages_with_keyword(keyword))
            geo_pages = sorted(set(geo_pages))[:10]
            if not geo_pages:
                return None
            for page in geo_pages:
                tables = self.extractor.extract_tables(page_range=(page, page))
                for table in tables:
                    if table.empty:
                        continue
                    table_str = table.to_string().lower()
                    if any(
                        loc in table_str
                        for loc in ["united states", "china", "europe", "california", "new york"]
                    ):
                        geo_df = self._clean_geographic_dataframe(table)
                        if geo_df is not None and not geo_df.empty:
                            logger.info(f"Extracted geographic data with {len(geo_df)} locations")
                            return geo_df
        except Exception as e:
            logger.error(f"Error extracting geographic adoption: {e}")
        return None

    def _clean_geographic_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
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
            clean_df = clean_df.dropna()
            clean_df = clean_df[
                (clean_df["adoption_rate"] >= 0) & (clean_df["adoption_rate"] <= 100)
            ]
            return clean_df.reset_index(drop=True)
        return None

    def _extract_firm_size_adoption(self) -> Optional[pd.DataFrame]:
        logger.info("Extracting firm size adoption data...")
        try:
            keywords = [
                "firm size", "company size", "employee", "small business", "enterprise", "SMB"
            ]
            size_pages = []
            for keyword in keywords:
                size_pages.extend(self.extractor.find_pages_with_keyword(keyword))
            size_pages = sorted(set(size_pages))[:10]
            if not size_pages:
                return None
            for page in size_pages:
                tables = self.extractor.extract_tables(page_range=(page, page))
                for table in tables:
                    if table.empty:
                        continue
                    table_str = table.to_string().lower()
                    size_indicators = [
                        "employee", "<50", "50-", "250-", "1000", "5000", "small", "medium", "large"
                    ]
                    if sum(1 for ind in size_indicators if ind in table_str) >= 2:
                        size_df = self._clean_firm_size_dataframe(table)
                        if size_df is not None and not size_df.empty:
                            logger.info(f"Extracted firm size data with {len(size_df)} categories")
                            return size_df
        except Exception as e:
            logger.error(f"Error extracting firm size adoption: {e}")
        return None

    def _clean_firm_size_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
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
            clean_df = clean_df.dropna()
            clean_df = clean_df[
                (clean_df["adoption_rate"] >= 0) & (clean_df["adoption_rate"] <= 100)
            ]
            return clean_df.reset_index(drop=True)
        return None

    def _extract_ai_maturity(self) -> Optional[pd.DataFrame]:
        logger.info("Extracting AI maturity data...")
        try:
            keywords = [
                "maturity", "stage", "phase", "journey", "adoption stage", "implementation phase"
            ]
            maturity_pages = []
            for keyword in keywords:
                maturity_pages.extend(self.extractor.find_pages_with_keyword(keyword))
            maturity_pages = sorted(set(maturity_pages))[:10]
            if not maturity_pages:
                return None
            for page in maturity_pages:
                tables = self.extractor.extract_tables(page_range=(page, page))
                for table in tables:
                    if table.empty:
                        continue
                    table_str = table.to_string().lower()
                    maturity_keywords = [
                        "exploring", "experimenting", "pilot", "scaling", "transform", "mature"
                    ]
                    if sum(1 for kw in maturity_keywords if kw in table_str) >= 2:
                        maturity_df = self._clean_maturity_dataframe(table)
                        if maturity_df is not None and not maturity_df.empty:
                            logger.info(f"Extracted maturity data with {len(maturity_df)} stages")
                            return maturity_df
        except Exception as e:
            logger.error(f"Error extracting AI maturity: {e}")
        return None

    def _clean_maturity_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
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
            clean_df = clean_df.dropna()
            clean_df = clean_df[
                (clean_df["percentage_of_firms"] >= 0) & (clean_df["percentage_of_firms"] <= 100)
            ]
            return clean_df.reset_index(drop=True)
        return None

    def _extract_investment_trends(self) -> Optional[pd.DataFrame]:
        logger.info("Extracting investment trends data...")
        try:
            keywords = ["investment", "funding", "venture capital", "billion", "million", "capital"]
            investment_pages = []
            for keyword in keywords:
                investment_pages.extend(self.extractor.find_pages_with_keyword(keyword))
            investment_pages = sorted(set(investment_pages))[:10]
            if not investment_pages:
                return None
            investment_data = []
            for page in investment_pages[:5]:
                text = self.extractor.extract_text_from_page(page)
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
                                amount, unit, year = match
                            else:
                                year, amount, unit = match
                            year = int(year)
                            amount = float(amount)
                            if unit.lower() in ["million", "m"]:
                                amount = amount / 1000
                            if 2010 <= year <= 2030 and amount > 0:
                                investment_data.append(
                                    {"year": year, "global_investment_billions": amount}
                                )
                        except ValueError:
                            continue
            if investment_data:
                investment_df = pd.DataFrame(investment_data)
                investment_df = (
                    investment_df.groupby("year")
                    .agg({"global_investment_billions": "max"})
                    .reset_index()
                )
                investment_df = investment_df.sort_values("year")
                logger.info(f"Extracted investment trends with {len(investment_df)} years")
                return investment_df
        except Exception as e:
            logger.error(f"Error extracting investment trends: {e}")
        return None

    def validate(self, data: Dict[str, pd.DataFrame]) -> bool:
        if not data:
            raise ValueError("No data extracted from PDF")
        logger.info(f"Extracted datasets: {list(data.keys())}")
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
        return {
            "adoption_trends": pd.DataFrame(columns=["year", "overall_adoption", "genai_adoption"]),
            "sector_adoption": pd.DataFrame(columns=["sector", "year", "adoption_rate"]),
            "geographic_adoption": pd.DataFrame(columns=["location", "year", "adoption_rate"]),
            "firm_size_adoption": pd.DataFrame(columns=["firm_size", "adoption_rate"]),
            "ai_maturity": pd.DataFrame(columns=["maturity_level", "percentage_of_firms"]),
            "investment_trends": pd.DataFrame(columns=["year", "global_investment_billions"]),
        }
