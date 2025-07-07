"""McKinsey State of AI data loader with actual PDF extraction."""

import logging
import re
from pathlib import Path
from typing import Dict, List, Optional

import pandas as pd

from ..extractors.pdf_extractor import PDFExtractor
from ..models.economics import EconomicImpact, ROIMetrics
from .base import BaseDataLoader, DataSource

logger = logging.getLogger(__name__)


class McKinseyLoader(BaseDataLoader):
    """Loader for McKinsey State of AI report data with real PDF extraction."""

    def __init__(self, file_path: Optional[Path] = None):
        """Initialize with McKinsey report file path."""
        if file_path is None:
            # Default to McKinsey State of AI report
            file_path = Path(
                "C:/Users/rcasa/OneDrive/Documents/AI-Adoption-Dashboard/data/loaders/mckinsey.py"
                "the-state-of-ai-how-organizations-are-rewiring-to-capture-value_final.pdf"
            )

        source = DataSource(
            name="McKinsey State of AI",
            version="2024",
            url="https://www.mckinsey.com/capabilities/quantumblack/our-insights/the-state-of-ai",
            file_path=file_path,
            citation="McKinsey & Company. 'The State of AI in 2024.r' McKinsey Global Institute.",
        )
        super().__init__(source)

        # Initialize PDF extractor if file exists
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
        """Load all datasets from McKinsey report using actual PDF extraction."""
        logger.info(f"Loading data from {self.source.name} {self.source.version}")

        if not self.extractor:
            logger.warning("PDF extractor not available, returning empty datasets")
            return self._get_empty_datasets()

        datasets = {}

        try:
            # Extract different aspects of the report

            # 1. Value creation and financial impact
            financial_impact = self._extract_financial_impact()
            if financial_impact is not None and not financial_impact.empty:
                datasets["financial_impact"] = financial_impact

            # 2. Use case adoption by function
            use_case_adoption = self._extract_use_case_adoption()
            if use_case_adoption is not None and not use_case_adoption.empty:
                datasets["use_case_adoption"] = use_case_adoption

            # 3. Implementation challenges and barriers
            implementation_barriers = self._extract_implementation_barriers()
            if implementation_barriers is not None and not implementation_barriers.empty:
                datasets["implementation_barriers"] = implementation_barriers

            # 4. AI talent and skills
            talent_metrics = self._extract_talent_metrics()
            if talent_metrics is not None and not talent_metrics.empty:
                datasets["talent_metrics"] = talent_metrics

            # 5. Productivity gains
            productivity_gains = self._extract_productivity_gains()
            if productivity_gains is not None and not productivity_gains.empty:
                datasets["productivity_gains"] = productivity_gains

            # 6. Risk and governance
            risk_governance = self._extract_risk_governance()
            if risk_governance is not None and not risk_governance.empty:
                datasets["risk_governance"] = risk_governance

        except Exception as e:
            logger.error(f"Error during PDF extraction: {e}")
            # Return empty datasets on error
            return self._get_empty_datasets()

        # Validate datasets
        if datasets:
            self.validate(datasets)
        else:
            logger.warning("No data extracted from PDF, using empty datasets")
            datasets = self._get_empty_datasets()

        return datasets

    def _extract_financial_impact(self) -> Optional[pd.DataFrame]:
        """Extract financial impact and value creation data."""
        logger.info("Extracting financial impact data...")

        try:
            # Keywords for financial impact sections
            keywords = [
                "value creation",
                "financial impact",
                "cost reduction",
                "revenue increase",
                "EBITDA",
                "productivity",
                "savings",
            ]

            # Find relevant pages
            financial_pages = []
            for keyword in keywords:
                pages = self.extractor.find_pages_with_keyword(keyword)
                financial_pages.extend(pages)

            financial_pages = sorted(set(financial_pages))[:15]

            if not financial_pages:
                return None

            # Extract financial data from tables and text
            financial_data = []

            # First try tables
            for page in financial_pages[:10]:
                tables = self.extractor.extract_tables(page_range=(page, page))

                for table in tables:
                    if table.empty:
                        continue

                    table_str = table.to_string().lower()
                    # Check if table contains financial metrics
                    if any(
                        term in table_str
                        for term in ["cost", "revenue", "savings", "increase", "reduction", "%"]
                    ):
                        # Process financial table
                        processed_data = self._process_financial_table(table)
                        if processed_data:
                            financial_data.extend(processed_data)

            # Also extract from text using patterns
            for page in financial_pages[:5]:
                text = self.extractor.extract_text_from_page(page)

                # Patterns for financial metrics
                # Examples: "20% cost reduction", "15% revenue increase", "$2.5 million savings"
                patterns = [
                    r"(\d+(?:\.\d+)?)\s*%\s*(cost reduction|revenue increase|productivity gain|EBITDA improvement)",
                    r"(cost reduction|revenue increase|productivity gain|savings)\s*of\s*(\d+(?:\.\d+)?)\s*%",
                    r"\$(\d+(?:\.\d+)?)\s*(million|billion)\s*(savings|value|impact)",
                    r"(\d+(?:\.\d+)?)\s*%\s*(improvement|increase|decrease|reduction)\s*in\s*(\w+)",
                ]

                for pattern in patterns:
                    matches = re.findall(pattern, text, re.IGNORECASE)
                    for match in matches:
                        financial_data.append(self._parse_financial_match(match, pattern))

            if financial_data:
                # Convert to DataFrame and clean
                df = pd.DataFrame(financial_data)
                df = df.dropna(subset=["metric", "value"])
                df = df.drop_duplicates()

                logger.info(f"Extracted {len(df)} financial impact metrics")
                return df

        except Exception as e:
            logger.error(f"Error extracting financial impact: {e}")

        return None

    def _process_financial_table(self, table: pd.DataFrame) -> List[Dict]:
        """Process a table containing financial metrics."""
        results = []

        # Identify metric name column
        metric_col = None
        for col in table.columns:
            sample_vals = table[col].astype(str).str.lower()
            if any(
                val
                for val in sample_vals
                if any(
                    term in val
                    for term in ["cost", "revenue", "productivity", "savings", "function"]
                )
            ):
                metric_col = col
                break

        if not metric_col:
            return results

        # Find value columns
        value_cols = []
        for col in table.columns:
            if col == metric_col:
                continue

            # Check if column contains percentages or numbers
            col_str = table[col].astype(str)
            if col_str.str.contains("%").sum() > len(table) * 0.3:
                value_cols.append(col)
            elif col_str.str.match(r"^\d+(?:\.\d+)?$").sum() > len(table) * 0.3:
                value_cols.append(col)

        # Extract data
        for _, row in table.iterrows():
            metric_name = str(row[metric_col])

            for val_col in value_cols:
                try:
                    value_str = str(row[val_col])
                    if "%" in value_str:
                        value = float(value_str.replace("%", "").strip())
                        unit = "percentage"
                    else:
                        value = float(value_str.replace(",", "").strip())
                        unit = "absolute"

                    results.append(
                        {
                            "metric": metric_name,
                            "value": value,
                            "unit": unit,
                            "category": self._categorize_financial_metric(metric_name),
                        }
                    )
                except ValueError:
                    continue

        return results

    def _parse_financial_match(self, match: tuple, pattern: str) -> Dict:
        """Parse a regex match for financial data."""
        result = {"metric": "", "value": 0, "unit": "", "category": ""}

        try:
            if "%" in pattern and "cost reduction" in pattern:
                # Pattern like "20% cost reduction"
                if len(match) >= 2:
                    result["value"] = float(match[0])
                    result["metric"] = match[1]
                    result["unit"] = "percentage"
            elif "$" in pattern:
                # Pattern like "$2.5 million savings"
                if len(match) >= 3:
                    value = float(match[0])
                    multiplier = 1 if match[1].lower() == "million" else 1000
                    result["value"] = value * multiplier
                    result["metric"] = f"{match[2]} (millions)"
                    result["unit"] = "millions_usd"
            else:
                # Generic percentage pattern
                if len(match) >= 3:
                    result["value"] = float(match[0])
                    result["metric"] = f"{match[1]} in {match[2]}"
                    result["unit"] = "percentage"

            result["category"] = self._categorize_financial_metric(result["metric"])

        except (ValueError, IndexError):
            pass

        return result

    def _categorize_financial_metric(self, metric: str) -> str:
        """Categorize financial metric."""
        metric_lower = metric.lower()

        if any(term in metric_lower for term in ["cost", "expense", "reduction"]):
            return "cost_savings"
        elif any(term in metric_lower for term in ["revenue", "sales", "growth"]):
            return "revenue_gains"
        elif any(term in metric_lower for term in ["productivity", "efficiency"]):
            return "productivity"
        elif any(term in metric_lower for term in ["risk", "compliance"]):
            return "risk_reduction"
        else:
            return "other"

    def _extract_use_case_adoption(self) -> Optional[pd.DataFrame]:
        """Extract AI use case adoption by business function."""
        logger.info("Extracting use case adoption data...")

        try:
            # Keywords for use case sections
            keywords = [
                "use case",
                "application",
                "deployment",
                "function",
                "department",
                "marketing",
                "sales",
                "supply chain",
                "HR",
                "finance",
                "IT",
            ]

            # Find relevant pages
            use_case_pages = []
            for keyword in keywords:
                pages = self.extractor.find_pages_with_keyword(keyword)
                use_case_pages.extend(pages)

            use_case_pages = sorted(set(use_case_pages))[:10]

            if not use_case_pages:
                return None

            # Look for use case tables
            for page in use_case_pages:
                tables = self.extractor.extract_tables(page_range=(page, page))

                for table in tables:
                    if table.empty or len(table) < 3:
                        continue

                    # Check if table contains function names
                    table_str = table.to_string().lower()
                    function_keywords = [
                        "marketing",
                        "sales",
                        "supply",
                        "operations",
                        "finance",
                        "hr",
                        "it",
                    ]

                    if sum(1 for kw in function_keywords if kw in table_str) >= 3:
                        # Process use case table
                        use_case_df = self._process_use_case_table(table)
                        if use_case_df is not None and not use_case_df.empty:
                            logger.info(
                                f"Extracted use case data with {len(use_case_df)} functions"
                            )
                            return use_case_df

            # If no table found, extract from text
            use_case_data = self._extract_use_cases_from_text(use_case_pages)
            if use_case_data:
                return pd.DataFrame(use_case_data)

        except Exception as e:
            logger.error(f"Error extracting use case adoption: {e}")

        return None

    def _process_use_case_table(self, table: pd.DataFrame) -> Optional[pd.DataFrame]:
        """Process table containing use case data."""
        # Identify function column
        function_col = None
        for col in table.columns:
            sample_vals = table[col].astype(str).str.lower()
            if any(
                "marketing" in val or "sales" in val or "supply" in val or "finance" in val
                for val in sample_vals
            ):
                function_col = col
                break

        if not function_col:
            return None

        # Find adoption rate columns
        rate_cols = []
        for col in table.columns:
            if col == function_col:
                continue

            # Check for percentage values
            col_vals = table[col].astype(str)
            if col_vals.str.contains("%").sum() > len(table) * 0.3:
                rate_cols.append(col)

        if function_col and rate_cols:
            # Create clean dataframe
            result_data = []

            for _, row in table.iterrows():
                function = str(row[function_col]).strip()

                for rate_col in rate_cols:
                    try:
                        rate_str = str(row[rate_col])
                        rate = float(rate_str.replace("%", "").strip())

                        # Determine metric type from column name
                        col_lower = rate_col.lower()
                        if "genai" in col_lower or "generative" in col_lower:
                            metric_type = "genai_adoption"
                        elif "pilot" in col_lower:
                            metric_type = "pilot_rate"
                        elif "production" in col_lower:
                            metric_type = "production_rate"
                        else:
                            metric_type = "adoption_rate"

                        result_data.append({"function": function, metric_type: rate, "year": 2024})
                    except ValueError:
                        continue

            if result_data:
                # Consolidate by function
                df = pd.DataFrame(result_data)
                df = df.groupby("function").first().reset_index()
                return df

        return None

    def _extract_use_cases_from_text(self, pages: List[int]) -> List[Dict]:
        """Extract use case data from text."""
        use_case_data = []
        functions = [
            "Marketing",
            "Sales",
            "Supply Chain",
            "Operations",
            "Finance",
            "HR",
            "IT",
            "R&D",
        ]

        for page in pages[:5]:
            text = self.extractor.extract_text_from_page(page)

            for function in functions:
                # Look for function mentions with percentages
                patterns = [
                    rf"{function}.*?(\d+(?:\.\d+)?)\s*%",
                    rf"(\d+(?:\.\d+)?)\s*%.*?{function}",
                    rf"{function}.*?adoption.*?(\d+(?:\.\d+)?)\s*%",
                ]

                for pattern in patterns:
                    matches = re.findall(pattern, text, re.IGNORECASE)
                    if matches:
                        try:
                            rate = float(matches[0])
                            if 0 <= rate <= 100:
                                use_case_data.append(
                                    {"function": function, "adoption_rate": rate, "year": 2024}
                                )
                                break
                        except ValueError:
                            continue

        # Remove duplicates
        seen = set()
        unique_data = []
        for item in use_case_data:
            key = item["function"]
            if key not in seen:
                seen.add(key)
                unique_data.append(item)

        return unique_data

    def _extract_implementation_barriers(self) -> Optional[pd.DataFrame]:
        """Extract implementation challenges and barriers."""
        logger.info("Extracting implementation barriers...")

        try:
            # Keywords for barriers/challenges
            keywords = [
                "barrier",
                "challenge",
                "obstacle",
                "difficulty",
                "constraint",
                "limitation",
                "risk",
                "concern",
            ]

            # Find relevant pages
            barrier_pages = []
            for keyword in keywords:
                pages = self.extractor.find_pages_with_keyword(keyword)
                barrier_pages.extend(pages)

            barrier_pages = sorted(set(barrier_pages))[:10]

            if not barrier_pages:
                return None

            barriers_data = []

            # Extract from tables first
            for page in barrier_pages[:5]:
                tables = self.extractor.extract_tables(page_range=(page, page))

                for table in tables:
                    if table.empty:
                        continue

                    # Look for barrier-related content
                    table_str = table.to_string().lower()
                    if any(
                        term in table_str
                        for term in ["talent", "data", "integration", "cost", "security"]
                    ):
                        processed = self._process_barrier_table(table)
                        if processed:
                            barriers_data.extend(processed)

            # Also extract from text
            barrier_patterns = [
                r"(\d+(?:\.\d+)?)\s*%\s*(?:of\s+)?(?:companies|organizations|firms)\s+(?:cite|report|identify)\s+([^.]+)\s+as\s+(?:a\s+)?(?:barrier|challenge)",
                r"([^.]+)\s+(?:is|are)\s+(?:a\s+)?(?:barrier|challenge)\s+for\s+(\d+(?:\.\d+)?)\s*%",
                r"(?:barrier|challenge):\s*([^.]+)\s+\((\d+(?:\.\d+)?)\s*%\)",
            ]

            for page in barrier_pages[:5]:
                text = self.extractor.extract_text_from_page(page)

                for pattern in barrier_patterns:
                    matches = re.findall(pattern, text, re.IGNORECASE)
                    for match in matches:
                        barriers_data.append(self._parse_barrier_match(match, pattern))

            if barriers_data:
                # Convert to DataFrame and clean
                df = pd.DataFrame(barriers_data)
                df = df.dropna(subset=["barrier"])
                df = df[df["percentage"] > 0]
                df = df.drop_duplicates(subset=["barrier"])
                df = df.sort_values("percentage", ascending=False)

                logger.info(f"Extracted {len(df)} implementation barriers")
                return df.head(15)  # Top 15 barriers

        except Exception as e:
            logger.error(f"Error extracting implementation barriers: {e}")

        return None

    def _process_barrier_table(self, table: pd.DataFrame) -> List[Dict]:
        """Process table containing barrier data."""
        results = []

        # Find barrier description column
        barrier_col = None
        for col in table.columns:
            # Look for text-heavy columns
            non_numeric = table[col].astype(str).str.match(r"^\d+(?:\.\d+)?%?$").sum()
            if non_numeric < len(table) * 0.5:
                barrier_col = col
                break

        if not barrier_col:
            return results

        # Find percentage column
        pct_col = None
        for col in table.columns:
            if col == barrier_col:
                continue

            col_vals = table[col].astype(str)
            if col_vals.str.contains("%").sum() > len(table) * 0.3:
                pct_col = col
                break

        if barrier_col and pct_col:
            for _, row in table.iterrows():
                try:
                    barrier = str(row[barrier_col]).strip()
                    pct_str = str(row[pct_col])
                    percentage = float(pct_str.replace("%", "").strip())

                    if 0 < percentage <= 100:
                        results.append(
                            {
                                "barrier": barrier,
                                "percentage": percentage,
                                "category": self._categorize_barrier(barrier),
                            }
                        )
                except ValueError:
                    continue

        return results

    def _parse_barrier_match(self, match: tuple, pattern: str) -> Dict:
        """Parse regex match for barrier data."""
        result = {"barrier": "", "percentage": 0, "category": ""}

        try:
            if pattern.startswith(r"(\d+"):
                # Percentage first
                result["percentage"] = float(match[0])
                result["barrier"] = match[1].strip()
            else:
                # Barrier first
                result["barrier"] = match[0].strip()
                result["percentage"] = float(match[1])

            result["category"] = self._categorize_barrier(result["barrier"])

        except (ValueError, IndexError):
            pass

        return result

    def _categorize_barrier(self, barrier: str) -> str:
        """Categorize implementation barrier."""
        barrier_lower = barrier.lower()

        if any(term in barrier_lower for term in ["talent", "skill", "expertise", "training"]):
            return "talent"
        elif any(term in barrier_lower for term in ["data", "quality", "availability"]):
            return "data"
        elif any(term in barrier_lower for term in ["integration", "legacy", "system"]):
            return "technology"
        elif any(term in barrier_lower for term in ["cost", "budget", "investment", "roi"]):
            return "financial"
        elif any(
            term in barrier_lower for term in ["security", "privacy", "compliance", "regulation"]
        ):
            return "security_compliance"
        elif any(term in barrier_lower for term in ["culture", "resistance", "change"]):
            return "organizational"
        else:
            return "other"

    def _extract_talent_metrics(self) -> Optional[pd.DataFrame]:
        """Extract AI talent and skills data."""
        logger.info("Extracting talent metrics...")

        try:
            # Keywords for talent sections
            keywords = ["talent", "skills", "hiring", "workforce", "training", "expertise", "roles"]

            talent_pages = []
            for keyword in keywords:
                pages = self.extractor.find_pages_with_keyword(keyword)
                talent_pages.extend(pages)

            talent_pages = sorted(set(talent_pages))[:10]

            if not talent_pages:
                return None

            talent_data = []

            # Extract talent metrics
            for page in talent_pages[:5]:
                text = self.extractor.extract_text_from_page(page)

                # Patterns for talent metrics
                patterns = [
                    r"(\d+(?:\.\d+)?)\s*%\s*(?:of\s+)?(?:companies|organizations)\s+(?:report|face|have)\s+(?:talent|skill)\s+(?:gap|shortage)",
                    r"(\d+(?:\.\d+)?)\s*%\s*increase\s+in\s+(?:AI|ML|data)\s+(?:talent|hiring|roles)",
                    r"average\s+of\s+(\d+(?:\.\d+)?)\s+(?:AI|ML|data)\s+(?:professionals|engineers|scientists)\s+per\s+(?:company|organization)",
                    r"(\d+(?:\.\d+)?)\s*%\s*(?:of\s+)?employees\s+(?:trained|upskilled|reskilled)\s+(?:in|on)\s+AI",
                ]

                for pattern in patterns:
                    matches = re.findall(pattern, text, re.IGNORECASE)
                    for match in matches:
                        value = float(match if isinstance(match, str) else match[0])

                        if "gap" in pattern or "shortage" in pattern:
                            metric = "talent_gap_percentage"
                        elif "increase" in pattern and "hiring" in pattern:
                            metric = "hiring_increase_percentage"
                        elif "average" in pattern:
                            metric = "avg_ai_professionals"
                        elif "trained" in pattern or "upskilled" in pattern:
                            metric = "employees_trained_percentage"
                        else:
                            metric = "other_talent_metric"

                        talent_data.append({"metric": metric, "value": value, "year": 2024})

            if talent_data:
                df = pd.DataFrame(talent_data)
                df = df.drop_duplicates(subset=["metric"])
                logger.info(f"Extracted {len(df)} talent metrics")
                return df

        except Exception as e:
            logger.error(f"Error extracting talent metrics: {e}")

        return None

    def _extract_productivity_gains(self) -> Optional[pd.DataFrame]:
        """Extract productivity gains data."""
        logger.info("Extracting productivity gains...")

        try:
            # Keywords for productivity sections
            keywords = [
                "productivity",
                "efficiency",
                "performance",
                "output",
                "automation",
                "time savings",
            ]

            productivity_pages = []
            for keyword in keywords:
                pages = self.extractor.find_pages_with_keyword(keyword)
                productivity_pages.extend(pages)

            productivity_pages = sorted(set(productivity_pages))[:10]

            if not productivity_pages:
                return None

            productivity_data = []

            # Extract productivity metrics
            for page in productivity_pages[:5]:
                text = self.extractor.extract_text_from_page(page)

                # Extract numeric productivity data
                numeric_data = self.extractor.extract_numeric_data(
                    keywords=["productivity", "efficiency", "time", "output"],
                    value_pattern=r"(\d+(?:\.\d+)?)\s*(%|percent|hours|x)",
                )

                for keyword, values in numeric_data.items():
                    for value, unit in values:
                        if unit in ["%", "percent"]:
                            productivity_data.append(
                                {
                                    "metric": f"{keyword}_improvement",
                                    "value": value,
                                    "unit": "percentage",
                                    "category": self._categorize_productivity_metric(keyword),
                                }
                            )
                        elif unit == "hours":
                            productivity_data.append(
                                {
                                    "metric": f"{keyword}_saved",
                                    "value": value,
                                    "unit": "hours",
                                    "category": "time_savings",
                                }
                            )
                        elif unit == "x":
                            productivity_data.append(
                                {
                                    "metric": f"{keyword}_multiplier",
                                    "value": value,
                                    "unit": "multiplier",
                                    "category": "efficiency",
                                }
                            )

            if productivity_data:
                df = pd.DataFrame(productivity_data)
                df = df[df["value"] > 0]
                df = df.drop_duplicates(subset=["metric"])
                logger.info(f"Extracted {len(df)} productivity metrics")
                return df

        except Exception as e:
            logger.error(f"Error extracting productivity gains: {e}")

        return None

    def _categorize_productivity_metric(self, metric: str) -> str:
        """Categorize productivity metric."""
        metric_lower = metric.lower()

        if "time" in metric_lower:
            return "time_savings"
        elif "output" in metric_lower:
            return "output_increase"
        elif "efficiency" in metric_lower:
            return "efficiency"
        elif "automation" in metric_lower:
            return "automation"
        else:
            return "general_productivity"

    def _extract_risk_governance(self) -> Optional[pd.DataFrame]:
        """Extract risk and governance data."""
        logger.info("Extracting risk and governance data...")

        try:
            # Keywords for risk/governance sections
            keywords = [
                "risk",
                "governance",
                "compliance",
                "ethics",
                "responsible",
                "bias",
                "fairness",
                "transparency",
                "accountability",
            ]

            risk_pages = []
            for keyword in keywords:
                pages = self.extractor.find_pages_with_keyword(keyword)
                risk_pages.extend(pages)

            risk_pages = sorted(set(risk_pages))[:10]

            if not risk_pages:
                return None

            risk_data = []

            # Common risk and governance aspects
            aspects = [
                "AI ethics guidelines",
                "Risk assessment framework",
                "Bias detection and mitigation",
                "Data privacy controls",
                "Transparency requirements",
                "Model governance",
                "Compliance monitoring",
                "Responsible AI practices",
            ]

            # Extract adoption rates for each aspect
            for page in risk_pages[:5]:
                text = self.extractor.extract_text_from_page(page)

                for aspect in aspects:
                    # Look for mentions with percentages
                    patterns = [
                        rf"{aspect}.*?(\d+(?:\.\d+)?)\s*%",
                        rf"(\d+(?:\.\d+)?)\s*%.*?{aspect}",
                        rf"{aspect}.*?adopted by.*?(\d+(?:\.\d+)?)\s*%",
                    ]

                    for pattern in patterns:
                        matches = re.findall(pattern, text, re.IGNORECASE)
                        if matches:
                            try:
                                rate = float(matches[0])
                                if 0 <= rate <= 100:
                                    risk_data.append(
                                        {
                                            "governance_aspect": aspect,
                                            "adoption_rate": rate,
                                            "year": 2024,
                                        }
                                    )
                                    break
                            except ValueError:
                                continue

            if risk_data:
                df = pd.DataFrame(risk_data)
                df = df.drop_duplicates(subset=["governance_aspect"])
                df = df.sort_values("adoption_rate", ascending=False)
                logger.info(f"Extracted {len(df)} risk/governance metrics")
                return df

        except Exception as e:
            logger.error(f"Error extracting risk/governance data: {e}")

        return None

    def validate(self, data: Dict[str, pd.DataFrame]) -> bool:
        """Validate loaded data meets expected schema."""
        if not data:
            raise ValueError("No data extracted from PDF")

        logger.info(f"Extracted datasets: {list(data.keys())}")

        # Validate key datasets
        if "financial_impact" in data:
            df = data["financial_impact"]
            if not {"metric", "value"}.issubset(df.columns):
                raise ValueError("Financial impact missing required columns")

        if "use_case_adoption" in data:
            df = data["use_case_adoption"]
            if "function" not in df.columns:
                raise ValueError("Use case adoption missing 'function' column")

        logger.info("Data validation passed")
        return True

    def _get_empty_datasets(self) -> Dict[str, pd.DataFrame]:
        """Return empty datasets when extraction fails."""
        return {
            "financial_impact": pd.DataFrame(),
            "use_case_adoption": pd.DataFrame(),
            "implementation_barriers": pd.DataFrame(),
            "talent_metrics": pd.DataFrame(),
            "productivity_gains": pd.DataFrame(),
            "risk_governance": pd.DataFrame(),
        }
