"""Federal Reserve Banks data loaders for AI economic impact studies."""

import logging
import re
from pathlib import Path
from typing import Dict, List, Optional

import pandas as pd

from ..extractors.pdf_extractor_impl import EnhancedPDFExtractor
from ..models.economics import EconomicImpact
from ..models.workforce import ProductivityMetrics
from ..models.workforce import WorkforceImpact
from .base import BaseDataLoader, DataSource

logger = logging.getLogger(__name__)


class RichmondFedLoader(BaseDataLoader):
    """Loader for Richmond Fed productivity and workforce transformation data with real PDF extraction."""

    def __init__(self, file_path: Optional[Path] = None):
        if file_path is None:
            file_path = Path(
                "/mnt/c/Users/rcasa/OneDrive/Documents/AI-Adoption-Dashboard/"
                "AI adoption resources/AI dashboard resources 1/"
                "The Productivity Puzzle_ AI, Technology Adoption and the Workforce _ Richmond Fed.pdf"
            )
        source = DataSource(
            name="Richmond Fed Productivity Analysis",
            version="2024",
            url="https://www.richmondfed.org/publications/research/econ_focus",
            file_path=file_path,
            citation="Federal Reserve Bank of Richmond. 'The Productivity Puzzle: AI, Technology Adoption and the Workforce.' Economic Focus, 2024.",
        )
        super().__init__(source)
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
        logger.info(f"Loading data from {self.source.name}")
        if not self.extractor:
            logger.warning("PDF extractor not available, returning fallback datasets")
            raise RuntimeError("PDF extractor not available; cannot load data.")
        datasets = {}
        try:
            productivity_trends = self._extract_productivity_trends()
            if productivity_trends is not None and not productivity_trends.empty:
                datasets["productivity_trends"] = productivity_trends
            tech_adoption = self._extract_technology_adoption()
            if tech_adoption is not None and not tech_adoption.empty:
                datasets["technology_adoption"] = tech_adoption
            workforce_impact = self._extract_workforce_transformation()
            if workforce_impact is not None and not workforce_impact.empty:
                datasets["workforce_transformation"] = workforce_impact
            skill_requirements = self._extract_skill_requirements()
            if skill_requirements is not None and not skill_requirements.empty:
                datasets["skill_requirements"] = skill_requirements
            regional_data = self._extract_regional_variations()
            if regional_data is not None and not regional_data.empty:
                datasets["regional_variations"] = regional_data
            policy_implications = self._extract_policy_implications()
            if policy_implications is not None and not policy_implications.empty:
                datasets["policy_implications"] = policy_implications
        except Exception as e:
            logger.error(f"Error during PDF extraction: {e}")
            raise
        if datasets:
            self.validate(datasets)
        else:
            logger.error("No data extracted from PDF; cannot proceed.")
            raise RuntimeError("No data extracted from PDF.")
        return datasets

    def _extract_productivity_trends(self) -> Optional[pd.DataFrame]:
        """Extract productivity trends and paradox data."""
        logger.info("Extracting productivity trends...")

        try:
            # Keywords for productivity sections
            keywords = ["productivity", "growth", "paradox", "slowdown", "puzzle", "output"]

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

                # Patterns for productivity data
                patterns = [
                    r"productivity\s+growth\s+(?:of\s+)?(\d+(?:\.\d+)?)\s*%",
                    r"(\d+(?:\.\d+)?)\s*%\s*(?:annual\s+)?productivity",
                    r"productivity\s+(?:increased|decreased|grew)\s+(?:by\s+)?(\d+(?:\.\d+)?)\s*%",
                    r"(\d+(?:\.\d+)?)\s*%\s*(?:decline|increase)\s+in\s+productivity",
                ]

                for pattern in patterns:
                    matches = re.findall(pattern, text, re.IGNORECASE)
                    for match in matches:
                        value = float(match[0] if isinstance(match, str) else match[0])

                        # Try to extract time period from context
                        period = self._extract_time_period(text, pattern)

                        productivity_data.append(
                            {
                                "metric": "productivity_growth_rate",
                                "value": value,
                                "period": period,
                                "unit": "percentage",
                            }
                        )

            # Look for productivity tables
            for page in productivity_pages[:5]:
                tables = self.extractor.extract_tables(page_range=(page, page))
                for table in tables:
                    if table.empty:
                        continue

                    # Process productivity tables
                    processed = self._process_productivity_table(table)
                    if processed:
                        productivity_data.extend(processed)

            if productivity_data:
                df = pd.DataFrame(productivity_data)
                df = df[df["value"].notna()]
                df = df.drop_duplicates(subset=["metric", "period"])

                logger.info(f"Extracted {len(df)} productivity trend metrics")
                return df

        except Exception as e:
            logger.error(f"Error extracting productivity trends: {e}")

        return None

    def _extract_time_period(self, text: str, pattern: str) -> str:
        """Extract time period from context."""
        # Look for year ranges or decades near the match
        year_patterns = [
            r"(\d{4})-(\d{4})",
            r"(\d{4})s",
            r"since\s+(\d{4})",
            r"between\s+(\d{4})\s+and\s+(\d{4})",
        ]

        for year_pattern in year_patterns:
            matches = re.findall(year_pattern, text[:200])  # Check nearby text
            if matches:
                if isinstance(matches[0], tuple):
                    return f"{matches[0][0]}-{matches[0][1]}"
                else:
                    return str(matches[0])

        # Default periods based on keywords
        if "recent" in text.lower():
            return "2020-2024"
        elif "historical" in text.lower():
            return "1990-2020"
        else:
            return "unspecified"

    def _process_productivity_table(self, table: pd.DataFrame) -> List[Dict]:
        """Process table containing productivity data."""
        results = []

        # Look for time period column (year, decade, period)
        time_col = None
        for col in table.columns:
            col_str = str(col).lower()
            if any(term in col_str for term in ["year", "period", "decade", "time"]):
                time_col = col
                break

        # Find productivity value columns
        value_cols = []
        for col in table.columns:
            if col == time_col:
                continue

            col_vals = table[col].astype(str)
            # Check for percentage or numeric values
            if (
                col_vals.str.contains("%").sum() > 0
                or col_vals.str.match(r"^-?\d+(?:\.\d+)?$").sum() > len(table) * 0.3
            ):
                value_cols.append(col)

        if time_col and value_cols:
            for _, row in table.iterrows():
                period = str(row[time_col]) if time_col else "unspecified"

                for val_col in value_cols:
                    try:
                        value_str = str(row[val_col])
                        value = float(value_str.replace("%", "").replace(",", "").strip())

                        # Determine metric type from column name
                        col_lower = val_col.lower()
                        if "growth" in col_lower:
                            metric = "productivity_growth_rate"
                        elif "level" in col_lower:
                            metric = "productivity_level"
                        elif "tfp" in col_lower:
                            metric = "total_factor_productivity"
                        else:
                            metric = "productivity_metric"

                        results.append(
                            {
                                "metric": metric,
                                "value": value,
                                "period": period,
                                "unit": "percentage" if "%" in value_str else "index",
                            }
                        )
                    except ValueError:
                        continue

        return results

    def _extract_technology_adoption(self) -> Optional[pd.DataFrame]:
        """Extract technology adoption patterns."""
        logger.info("Extracting technology adoption data...")

        try:
            # Keywords for technology adoption
            keywords = [
                "adoption",
                "implementation",
                "diffusion",
                "technology",
                "digital",
                "automation",
            ]

            tech_pages = []
            for keyword in keywords:
                pages = self.extractor.find_pages_with_keyword(keyword)
                tech_pages.extend(pages)

            tech_pages = sorted(set(tech_pages))[:10]

            if not tech_pages:
                return None

            tech_data = []

            # Technology categories to look for
            technologies = [
                "AI",
                "Machine Learning",
                "Automation",
                "Robotics",
                "Cloud Computing",
                "IoT",
                "Digital Tools",
                "Analytics",
            ]

            for page in tech_pages[:5]:
                text = self.extractor.extract_text_from_page(page)

                for tech in technologies:
                    # Patterns for adoption rates
                    patterns = [
                        rf"{tech}.*?adoption.*?(\d+(?:\.\d+)?)\s*%",
                        rf"(\d+(?:\.\d+)?)\s*%.*?(?:firms|companies).*?{tech}",
                        rf"{tech}.*?implemented.*?(\d+(?:\.\d+)?)\s*%",
                    ]

                    for pattern in patterns:
                        matches = re.findall(pattern, text, re.IGNORECASE)
                        if matches:
                            try:
                                rate = float(matches[0])
                                if 0 <= rate <= 100:
                                    tech_data.append(
                                        {
                                            "technology": tech,
                                            "adoption_rate": rate,
                                            "year": self._extract_year_from_context(text),
                                            "adoption_stage": self._categorize_adoption_stage(rate),
                                        }
                                    )
                                    break
                            except ValueError:
                                continue

            if tech_data:
                df = pd.DataFrame(tech_data)
                df = df.drop_duplicates(subset=["technology"])
                df = df.sort_values("adoption_rate", ascending=False)

                logger.info(f"Extracted technology adoption for {len(df)} technologies")
                return df

        except Exception as e:
            logger.error(f"Error extracting technology adoption: {e}")

        return None

    def _extract_year_from_context(self, text: str) -> int:
        """Extract year from text context."""
        # Look for recent years
        year_matches = re.findall(r"20[1-2]\d", text)
        if year_matches:
            # Return most recent year found
            return max(int(year) for year in year_matches)
        return 2024  # Default to current year

    def _categorize_adoption_stage(self, rate: float) -> str:
        """Categorize adoption stage based on rate."""
        if rate < 20:
            return "Early Adoption"
        elif rate < 50:
            return "Growing Adoption"
        elif rate < 80:
            return "Mainstream"
        else:
            return "Mature"

    def _extract_workforce_transformation(self) -> Optional[pd.DataFrame]:
        """Extract workforce transformation data."""
        logger.info("Extracting workforce transformation data...")

        try:
            # Keywords for workforce sections
            keywords = [
                "workforce",
                "employment",
                "jobs",
                "skills",
                "workers",
                "labor",
                "occupations",
            ]

            workforce_pages = []
            for keyword in keywords:
                pages = self.extractor.find_pages_with_keyword(keyword)
                workforce_pages.extend(pages)

            workforce_pages = sorted(set(workforce_pages))[:10]

            if not workforce_pages:
                return None

            workforce_data = []

            # Extract workforce metrics
            for page in workforce_pages[:5]:
                text = self.extractor.extract_text_from_page(page)

                # Patterns for workforce impact
                patterns = [
                    r"(\d+(?:\.\d+)?)\s*%\s*of\s*(?:workers|jobs|employment)\s*(?:affected|impacted|transformed)",
                    r"(\d+(?:\.\d+)?)\s*%\s*(?:job|employment)\s*(?:growth|decline|change)",
                    r"workforce.*?(\d+(?:\.\d+)?)\s*%\s*(?:increase|decrease|change)",
                    r"(\d+(?:\.\d+)?)\s*million\s*(?:jobs|workers)\s*(?:created|displaced|affected)",
                ]

                for pattern in patterns:
                    matches = re.findall(pattern, text, re.IGNORECASE)
                    for match in matches:
                        value = float(match[0] if isinstance(match, str) else match[0])

                        # Determine metric type
                        if "million" in pattern:
                            metric = "jobs_affected_millions"
                            unit = "millions"
                        else:
                            metric = "workforce_change_percentage"
                            unit = "percentage"

                        # Determine impact type
                        if any(
                            term in pattern.lower() for term in ["displaced", "decline", "decrease"]
                        ):
                            impact_type = "negative"
                        elif any(
                            term in pattern.lower() for term in ["created", "growth", "increase"]
                        ):
                            impact_type = "positive"
                        else:
                            impact_type = "transformation"

                        workforce_data.append(
                            {
                                "metric": metric,
                                "value": value,
                                "unit": unit,
                                "impact_type": impact_type,
                                "timeframe": self._extract_timeframe_from_context(text),
                            }
                        )

            if workforce_data:
                df = pd.DataFrame(workforce_data)
                df = df[df["value"] > 0]
                df = df.drop_duplicates()

                logger.info(f"Extracted {len(df)} workforce transformation metrics")
                return df

        except Exception as e:
            logger.error(f"Error extracting workforce transformation: {e}")

        return None

    def _extract_timeframe_from_context(self, text: str) -> str:
        """Extract timeframe from text context."""
        if "next decade" in text.lower():
            return "Next 10 years"
        elif "by 2030" in text.lower():
            return "By 2030"
        elif "next 5 years" in text.lower():
            return "Next 5 years"
        else:
            return "Projected"

    def _extract_skill_requirements(self) -> Optional[pd.DataFrame]:
        """Extract skill requirements and gaps data."""
        logger.info("Extracting skill requirements...")

        try:
            # Keywords for skills sections
            keywords = ["skills", "training", "education", "competencies", "capabilities", "talent"]

            skill_pages = []
            for keyword in keywords:
                pages = self.extractor.find_pages_with_keyword(keyword)
                skill_pages.extend(pages)

            skill_pages = sorted(set(skill_pages))[:10]

            if not skill_pages:
                return None

            skill_data = []

            # Common skill categories
            skill_categories = [
                "Technical Skills",
                "Digital Skills",
                "AI/ML Skills",
                "Data Analysis",
                "Programming",
                "Critical Thinking",
                "Communication",
                "Problem Solving",
                "Creativity",
                "Leadership",
                "Adaptability",
            ]

            for page in skill_pages[:5]:
                text = self.extractor.extract_text_from_page(page)

                for skill in skill_categories:
                    # Look for skill mentions with percentages or importance
                    patterns = [
                        f"{skill}.*?(\d+(?:\.\d+)?)\s*%\s*(?:of\s+)?(?:workers|employees|firms)\s*(?:need|require|lack)",
                        f"(\d+(?:\.\d+)?)\s*%.*?{skill}",
                        f"{skill}.*?(?:critical|essential|important).*?(\d+(?:\.\d+)?)\s*%",
                    ]

                    for pattern in patterns:
                        matches = re.findall(pattern, text, re.IGNORECASE)
                        if matches:
                            try:
                                value = float(matches[0])
                                if 0 <= value <= 100:
                                    skill_data.append(
                                        {
                                            "skill_category": skill,
                                            "importance_score": value,
                                            "skill_type": self._categorize_skill_type(skill),
                                            "demand_level": self._categorize_demand_level(value),
                                        }
                                    )
                                    break
                            except ValueError:
                                continue

            if skill_data:
                df = pd.DataFrame(skill_data)
                df = df.drop_duplicates(subset=["skill_category"])
                df = df.sort_values("importance_score", ascending=False)

                logger.info(f"Extracted {len(df)} skill requirements")
                return df

        except Exception as e:
            logger.error(f"Error extracting skill requirements: {e}")

        return None

    def _categorize_skill_type(self, skill: str) -> str:
        """Categorize skill type."""
        skill_lower = skill.lower()

        if any(term in skill_lower for term in ["technical", "programming", "ai", "ml", "data"]):
            return "Technical"
        elif any(term in skill_lower for term in ["communication", "leadership", "creativity"]):
            return "Soft Skills"
        elif "digital" in skill_lower:
            return "Digital Literacy"
        else:
            return "General"

    def _categorize_demand_level(self, score: float) -> str:
        """Categorize demand level based on importance score."""
        if score >= 70:
            return "Critical"
        elif score >= 50:
            return "High"
        elif score >= 30:
            return "Medium"
        else:
            return "Low"

    def _extract_regional_variations(self) -> Optional[pd.DataFrame]:
        """Extract regional variation data."""
        logger.info("Extracting regional variations...")

        try:
            # Keywords for regional data
            keywords = ["regional", "geographic", "state", "metropolitan", "urban", "rural"]

            regional_pages = []
            for keyword in keywords:
                pages = self.extractor.find_pages_with_keyword(keyword)
                regional_pages.extend(pages)

            regional_pages = sorted(set(regional_pages))[:10]

            if not regional_pages:
                return None

            regional_data = []

            # Common regions/areas
            regions = [
                "Northeast",
                "Southeast",
                "Midwest",
                "Southwest",
                "West Coast",
                "Urban",
                "Suburban",
                "Rural",
                "Metropolitan",
                "Non-metropolitan",
            ]

            for page in regional_pages[:5]:
                text = self.extractor.extract_text_from_page(page)

                # Extract numeric data by region
                numeric_data = self.extractor.extract_numeric_data(
                    keywords=regions,
                    value_pattern=r"(\d+(?:\.\d+)?)\s*(%|percent|percentage points)",
                )

                for region, values in numeric_data.items():
                    for value, unit in values:
                        if 0 <= value <= 100:
                            regional_data.append(
                                {
                                    "region": region,
                                    "metric_value": value,
                                    "metric_type": self._infer_regional_metric(text, region),
                                    "unit": "percentage",
                                }
                            )

            if regional_data:
                df = pd.DataFrame(regional_data)
                df = df.drop_duplicates()

                logger.info(f"Extracted {len(df)} regional variation metrics")
                return df

        except Exception as e:
            logger.error(f"Error extracting regional variations: {e}")

        return None

    def _infer_regional_metric(self, text: str, region: str) -> str:
        """Infer what metric is being measured for the region."""
        context = text.lower()

        if "adoption" in context:
            return "technology_adoption_rate"
        elif "productivity" in context:
            return "productivity_growth"
        elif "employment" in context or "jobs" in context:
            return "employment_impact"
        elif "investment" in context:
            return "investment_level"
        else:
            return "economic_metric"

    def _extract_policy_implications(self) -> Optional[pd.DataFrame]:
        """Extract policy implications and recommendations."""
        logger.info("Extracting policy implications...")

        try:
            # Keywords for policy sections
            keywords = [
                "policy",
                "recommendation",
                "government",
                "regulation",
                "intervention",
                "support",
            ]

            policy_pages = []
            for keyword in keywords:
                pages = self.extractor.find_pages_with_keyword(keyword)
                policy_pages.extend(pages)

            policy_pages = sorted(set(policy_pages))[:10]

            if not policy_pages:
                return None

            policy_data = []

            # Policy areas
            policy_areas = [
                "Education and Training",
                "Research and Development",
                "Infrastructure Investment",
                "Regulatory Framework",
                "Worker Protection",
                "Innovation Support",
                "Tax Incentives",
                "Public-Private Partnerships",
            ]

            for page in policy_pages[:5]:
                text = self.extractor.extract_text_from_page(page)

                for policy in policy_areas:
                    if policy.lower() in text.lower():
                        # Extract any associated metrics
                        patterns = [
                            r"(\d+(?:\.\d+)?)\s*%\s*(?:increase|improvement|reduction)",
                            r"\$(\d+(?:\.\d+)?)\s*(billion|million)\s*(?:investment|funding)",
                            r"(\d+(?:\.\d+)?)\s*(?:fold|x)\s*(?:increase|improvement)",
                        ]

                        impact_value = None
                        impact_unit = None

                        for pattern in patterns:
                            matches = re.findall(
                                pattern,
                                text[
                                    max(
                                        0, text.lower().find(policy.lower()) - 200
                                    ) : text.lower().find(policy.lower())
                                    + 200
                                ],
                                re.IGNORECASE,
                            )
                            if matches:
                                if "%" in pattern:
                                    impact_value = float(matches[0])
                                    impact_unit = "percentage"
                                elif "billion" in pattern or "million" in pattern:
                                    impact_value = float(matches[0][0])
                                    impact_unit = matches[0][1].lower()
                                else:
                                    impact_value = float(matches[0])
                                    impact_unit = "multiplier"
                                break

                        policy_data.append(
                            {
                                "policy_area": policy,
                                "priority_level": self._assess_policy_priority(text, policy),
                                "impact_value": impact_value,
                                "impact_unit": impact_unit,
                                "implementation_timeframe": self._extract_policy_timeframe(
                                    text, policy
                                ),
                            }
                        )

            if policy_data:
                df = pd.DataFrame(policy_data)
                # Sort by priority
                priority_order = {"Critical": 0, "High": 1, "Medium": 2, "Low": 3}
                df["priority_rank"] = df["priority_level"].map(priority_order)
                df = df.sort_values("priority_rank").drop("priority_rank", axis=1)

                logger.info(f"Extracted {len(df)} policy implications")
                return df

        except Exception as e:
            logger.error(f"Error extracting policy implications: {e}")

        return None

    def _assess_policy_priority(self, text: str, policy: str) -> str:
        """Assess priority level of policy recommendation."""
        # Look for priority indicators near the policy mention
        context = text[
            max(0, text.lower().find(policy.lower()) - 100) : text.lower().find(policy.lower())
            + 100
        ].lower()

        if any(term in context for term in ["critical", "urgent", "immediate", "essential"]):
            return "Critical"
        elif any(term in context for term in ["important", "significant", "priority"]):
            return "High"
        elif any(term in context for term in ["consider", "explore", "potential"]):
            return "Medium"
        else:
            return "Low"

    def _extract_policy_timeframe(self, text: str, policy: str) -> str:
        """Extract implementation timeframe for policy."""
        context = text[
            max(0, text.lower().find(policy.lower()) - 200) : text.lower().find(policy.lower())
            + 200
        ].lower()

        if "immediate" in context or "now" in context:
            return "Immediate"
        elif "short term" in context or "near term" in context:
            return "Short-term (1-2 years)"
        elif "medium term" in context:
            return "Medium-term (3-5 years)"
        elif "long term" in context:
            return "Long-term (5+ years)"
        else:
            return "Unspecified"

    def validate(self, data: Dict[str, pd.DataFrame]) -> bool:
        if not data:
            raise ValueError("No data extracted from PDF")
        logger.info(f"Extracted datasets: {list(data.keys())}")
        if "productivity_trends" in data:
            df = data["productivity_trends"]
            if "metric" not in df.columns or "value" not in df.columns:
                raise ValueError("Productivity trends missing required columns")
        if "workforce_transformation" in data:
            df = data["workforce_transformation"]
            if "metric" not in df.columns:
                raise ValueError("Workforce transformation missing 'metric' column")
        logger.info("Data validation passed")
        return True


class StLouisFedLoader(BaseDataLoader):
    """Loader for St. Louis Fed GenAI rapid adoption reports with real PDF extraction."""

    def __init__(self, file_paths: Optional[List[Path]] = None):
        if file_paths and not isinstance(file_paths, list):
            file_paths = [file_paths]
        primary_file = file_paths[0] if file_paths else None
        source = DataSource(
            name="St. Louis Fed GenAI Analysis",
            version="2024-2025",
            url="https://www.stlouisfed.org/on-the-economy",
            file_path=primary_file,
            citation="Federal Reserve Bank of St. Louis. 'Rapid Adoption of Generative AI' and 'Impact of Generative AI on Work Productivity.' On the Economy Blog, 2024-2025.",
        )
        super().__init__(source)
        self.file_paths = file_paths
        self.extractors = []
        for file_path in self.file_paths:
            if file_path and file_path.exists():
                try:
                    extractor = EnhancedPDFExtractor(file_path)
                    self.extractors.append(extractor)
                    logger.info(f"Initialized PDF extractor for {file_path.name}")
                except Exception as e:
                    logger.error(f"Failed to initialize PDF extractor for {file_path}: {e}")
            else:
                logger.warning(f"PDF file not found: {file_path}")

    def load(self) -> Dict[str, pd.DataFrame]:
        logger.info(f"Loading data from {self.source.name}")
        if not self.extractors:
            logger.error("No PDF extractors available; cannot load data.")
            raise RuntimeError("No PDF extractors available; cannot load data.")
        datasets = {}
        try:
            genai_adoption = self._extract_genai_adoption()
            if genai_adoption is not None and not genai_adoption.empty:
                datasets["genai_adoption_speed"] = genai_adoption
            productivity_impact = self._extract_productivity_impact()
            if productivity_impact is not None and not productivity_impact.empty:
                datasets["productivity_impact"] = productivity_impact
            task_automation = self._extract_task_automation()
            if task_automation is not None and not task_automation.empty:
                datasets["task_automation"] = task_automation
            worker_impacts = self._extract_worker_category_impacts()
            if worker_impacts is not None and not worker_impacts.empty:
                datasets["worker_category_impacts"] = worker_impacts
            implementation_timeline = self._extract_implementation_timeline()
            if implementation_timeline is not None and not implementation_timeline.empty:
                datasets["implementation_timeline"] = implementation_timeline
            economic_implications = self._extract_economic_implications()
            if economic_implications is not None and not economic_implications.empty:
                datasets["economic_implications"] = economic_implications
        except Exception as e:
            logger.error(f"Error during PDF extraction: {e}")
            raise
        if datasets:
            self.validate(datasets)
        else:
            logger.error("No data extracted from PDFs; cannot proceed.")
            raise RuntimeError("No data extracted from PDFs.")
        return datasets

    def _extract_genai_adoption(self) -> Optional[pd.DataFrame]:
        """Extract GenAI adoption rates and speed."""
        logger.info("Extracting GenAI adoption data...")

        adoption_data = []

        try:
            for extractor in self.extractors:
                # Keywords for adoption sections
                keywords = [
                    "adoption",
                    "generative AI",
                    "GenAI",
                    "uptake",
                    "implementation",
                    "deployment",
                ]

                adoption_pages = []
                for keyword in keywords:
                    pages = extractor.find_pages_with_keyword(keyword)
                    adoption_pages.extend(pages)

                adoption_pages = sorted(set(adoption_pages))[:10]

                if not adoption_pages:
                    continue

                # Extract adoption metrics
                for page in adoption_pages[:5]:
                    text = extractor.extract_text_from_page(page)

                    # Patterns for adoption data
                    patterns = [
                        r"(\d+(?:\.\d+)?)\s*%\s*of\s*(?:firms|companies|organizations)\s*(?:using|adopted|implementing)\s*(?:generative\s*)?AI",
                        r"(?:generative\s*)?AI\s*adoption\s*(?:rate\s*)?(?:reached|at|is)\s*(\d+(?:\.\d+)?)\s*%",
                        r"(\d+(?:\.\d+)?)\s*%\s*(?:increase|growth)\s*in\s*(?:generative\s*)?AI\s*adoption",
                        r"adoption\s*(?:rate\s*)?(?:increased|grew)\s*(?:by\s*)?(\d+(?:\.\d+)?)\s*%",
                    ]

                    for pattern in patterns:
                        matches = re.findall(pattern, text, re.IGNORECASE)
                        for match in matches:
                            value = float(match[0] if isinstance(match, str) else match[0])

                            # Determine metric type
                            if "increase" in pattern or "growth" in pattern or "grew" in pattern:
                                metric_type = "adoption_growth_rate"
                            else:
                                metric_type = "adoption_rate"

                            adoption_data.append(
                                {
                                    "metric": metric_type,
                                    "value": value,
                                    "technology": "Generative AI",
                                    "time_period": self._extract_time_period_from_text(text),
                                    "unit": "percentage",
                                }
                            )

            if adoption_data:
                df = pd.DataFrame(adoption_data)
                df = df[df["value"] > 0]
                df = df.drop_duplicates(subset=["metric", "time_period"])

                logger.info(f"Extracted {len(df)} GenAI adoption metrics")
                return df

        except Exception as e:
            logger.error(f"Error extracting GenAI adoption: {e}")

        return None

    def _extract_time_period_from_text(self, text: str) -> str:
        """Extract time period from text context."""
        # Look for specific time references
        if "2024" in text:
            if "2023" in text:
                return "2023-2024"
            return "2024"
        elif "2025" in text:
            return "2025"
        elif "past year" in text.lower():
            return "Past 12 months"
        elif "last 6 months" in text.lower():
            return "Past 6 months"
        else:
            return "Recent"

    def _extract_productivity_impact(self) -> Optional[pd.DataFrame]:
        """Extract productivity impact metrics."""
        logger.info("Extracting productivity impact data...")

        productivity_data = []

        try:
            for extractor in self.extractors:
                # Keywords for productivity sections
                keywords = ["productivity", "efficiency", "output", "performance", "time savings"]

                productivity_pages = []
                for keyword in keywords:
                    pages = extractor.find_pages_with_keyword(keyword)
                    productivity_pages.extend(pages)

                productivity_pages = sorted(set(productivity_pages))[:10]

                if not productivity_pages:
                    continue

                # Extract productivity metrics
                for page in productivity_pages[:5]:
                    text = extractor.extract_text_from_page(page)

                    # Extract numeric productivity data
                    numeric_data = extractor.extract_numeric_data(
                        keywords=["productivity", "efficiency", "output", "time"],
                        value_pattern=r"(\d+(?:\.\d+)?)\s*(%|percent|x|times|hours)",
                    )

                    for keyword, values in numeric_data.items():
                        for value, unit in values:
                            if unit in ["%", "percent"]:
                                metric = f"{keyword}_improvement_percentage"
                                unit_clean = "percentage"
                            elif unit in ["x", "times"]:
                                metric = f"{keyword}_multiplier"
                                unit_clean = "multiplier"
                            elif unit == "hours":
                                metric = f"{keyword}_saved"
                                unit_clean = "hours"
                            else:
                                continue

                            productivity_data.append(
                                {
                                    "metric": metric,
                                    "value": value,
                                    "unit": unit_clean,
                                    "context": self._extract_productivity_context(text, keyword),
                                }
                            )

            if productivity_data:
                df = pd.DataFrame(productivity_data)
                df = df[df["value"] > 0]
                df = df.drop_duplicates(subset=["metric"])

                logger.info(f"Extracted {len(df)} productivity impact metrics")
                return df

        except Exception as e:
            logger.error(f"Error extracting productivity impact: {e}")

        return None

    def _extract_productivity_context(self, text: str, keyword: str) -> str:
        """Extract context for productivity metric."""
        # Find context around the keyword
        keyword_pos = text.lower().find(keyword.lower())
        if keyword_pos == -1:
            return "general"

        context = text[max(0, keyword_pos - 100) : keyword_pos + 100].lower()

        if "writing" in context or "content" in context:
            return "content_creation"
        elif "code" in context or "programming" in context:
            return "software_development"
        elif "analysis" in context or "data" in context:
            return "data_analysis"
        elif "customer" in context or "service" in context:
            return "customer_service"
        else:
            return "general_tasks"

    def _extract_task_automation(self) -> Optional[pd.DataFrame]:
        """Extract task automation potential data."""
        logger.info("Extracting task automation data...")

        task_data = []

        try:
            for extractor in self.extractors:
                # Keywords for task automation
                keywords = ["task", "automate", "automation", "activities", "work activities"]

                task_pages = []
                for keyword in keywords:
                    pages = extractor.find_pages_with_keyword(keyword)
                    task_pages.extend(pages)

                task_pages = sorted(set(task_pages))[:10]

                if not task_pages:
                    continue

                # Extract task automation data
                for page in task_pages[:5]:
                    text = extractor.extract_text_from_page(page)

                    # Patterns for task automation
                    patterns = [
                        r"(\d+(?:\.\d+)?)\s*%\s*of\s*(?:tasks|activities|work)\s*(?:can be|could be|are)\s*automated",
                        r"automate\s*(\d+(?:\.\d+)?)\s*%\s*of\s*(?:tasks|activities)",
                        r"(\d+(?:\.\d+)?)\s*%\s*(?:task|activity)\s*automation\s*potential",
                    ]

                    for pattern in patterns:
                        matches = re.findall(pattern, text, re.IGNORECASE)
                        for match in matches:
                            value = float(match[0] if isinstance(match, str) else match[0])

                            # Try to identify task category
                            task_category = self._identify_task_category(text)

                            task_data.append(
                                {
                                    "task_category": task_category,
                                    "automation_potential": value,
                                    "feasibility": self._assess_automation_feasibility(value),
                                    "timeframe": self._extract_automation_timeframe(text),
                                }
                            )

            if task_data:
                df = pd.DataFrame(task_data)
                df = df[df["automation_potential"] > 0]
                df = df.drop_duplicates(subset=["task_category"])
                df = df.sort_values("automation_potential", ascending=False)

                logger.info(f"Extracted task automation data for {len(df)} categories")
                return df

        except Exception as e:
            logger.error(f"Error extracting task automation: {e}")

        return None

    def _identify_task_category(self, text: str) -> str:
        """Identify task category from context."""
        text_lower = text.lower()

        task_categories = {
            "Administrative": ["administrative", "clerical", "filing", "scheduling"],
            "Analytical": ["analysis", "research", "data", "insights"],
            "Creative": ["creative", "design", "content", "writing"],
            "Technical": ["technical", "engineering", "programming", "development"],
            "Communication": ["communication", "email", "correspondence", "messaging"],
            "Decision Making": ["decision", "strategic", "planning", "management"],
        }

        for category, keywords in task_categories.items():
            if any(keyword in text_lower for keyword in keywords):
                return category

        return "General Tasks"

    def _assess_automation_feasibility(self, potential: float) -> str:
        """Assess feasibility based on automation potential."""
        if potential >= 70:
            return "High"
        elif potential >= 40:
            return "Medium"
        else:
            return "Low"

    def _extract_automation_timeframe(self, text: str) -> str:
        """Extract timeframe for automation."""
        text_lower = text.lower()

        if "immediate" in text_lower or "today" in text_lower:
            return "Immediate"
        elif "near term" in text_lower or "soon" in text_lower:
            return "1-2 years"
        elif "medium term" in text_lower:
            return "3-5 years"
        elif "long term" in text_lower:
            return "5+ years"
        else:
            return "Ongoing"

    def _extract_worker_category_impacts(self) -> Optional[pd.DataFrame]:
        """Extract impacts by worker category."""
        logger.info("Extracting worker category impacts...")

        worker_data = []

        try:
            for extractor in self.extractors:
                # Keywords for worker categories
                keywords = ["worker", "employee", "skill level", "occupation", "job category"]

                worker_pages = []
                for keyword in keywords:
                    pages = extractor.find_pages_with_keyword(keyword)
                    worker_pages.extend(pages)

                worker_pages = sorted(set(worker_pages))[:10]

                if not worker_pages:
                    continue

                # Worker categories to look for
                categories = [
                    "High-skilled",
                    "Medium-skilled",
                    "Low-skilled",
                    "Knowledge workers",
                    "Service workers",
                    "Manual workers",
                    "Creative professionals",
                    "Technical workers",
                    "Administrative staff",
                ]

                for page in worker_pages[:5]:
                    text = extractor.extract_text_from_page(page)

                    for category in categories:
                        # Look for impact metrics for each category
                        patterns = [
                            f"{category}.*?(\d+(?:\.\d+)?)\s*%\s*(?:productivity|efficiency|impact)",
                            f"(\d+(?:\.\d+)?)\s*%.*?{category}",
                            f"{category}.*?(?:gain|improvement|benefit).*?(\d+(?:\.\d+)?)\s*%",
                        ]

                        for pattern in patterns:
                            matches = re.findall(pattern, text, re.IGNORECASE)
                            if matches:
                                try:
                                    impact_value = float(matches[0])
                                    if 0 <= impact_value <= 100:
                                        worker_data.append(
                                            {
                                                "worker_category": category,
                                                "impact_value": impact_value,
                                                "impact_type": self._determine_impact_type(
                                                    text, category
                                                ),
                                                "skill_level": self._categorize_skill_level(
                                                    category
                                                ),
                                            }
                                        )
                                        break
                                except ValueError:
                                    continue

            if worker_data:
                df = pd.DataFrame(worker_data)
                df = df.drop_duplicates(subset=["worker_category"])
                df = df.sort_values("impact_value", ascending=False)

                logger.info(f"Extracted impacts for {len(df)} worker categories")
                return df

        except Exception as e:
            logger.error(f"Error extracting worker category impacts: {e}")

        return None

    def _determine_impact_type(self, text: str, category: str) -> str:
        """Determine type of impact on worker category."""
        context = text.lower()

        if any(term in context for term in ["productivity", "efficiency", "output"]):
            return "productivity_gain"
        elif any(term in context for term in ["displacement", "replace", "substitute"]):
            return "displacement_risk"
        elif any(term in context for term in ["augment", "enhance", "assist"]):
            return "augmentation"
        elif any(term in context for term in ["skill", "upskill", "reskill"]):
            return "skill_change"
        else:
            return "general_impact"

    def _categorize_skill_level(self, category: str) -> str:
        """Categorize skill level of worker category."""
        category_lower = category.lower()

        if (
            "high" in category_lower
            or "knowledge" in category_lower
            or "professional" in category_lower
        ):
            return "High"
        elif "medium" in category_lower or "technical" in category_lower:
            return "Medium"
        elif "low" in category_lower or "manual" in category_lower:
            return "Low"
        else:
            return "Mixed"

    def _extract_implementation_timeline(self) -> Optional[pd.DataFrame]:
        """Extract GenAI implementation timeline data."""
        logger.info("Extracting implementation timeline...")

        timeline_data = []

        try:
            for extractor in self.extractors:
                # Keywords for timeline/phases
                keywords = ["timeline", "phase", "stage", "implementation", "roadmap", "milestone"]

                timeline_pages = []
                for keyword in keywords:
                    pages = extractor.find_pages_with_keyword(keyword)
                    timeline_pages.extend(pages)

                timeline_pages = sorted(set(timeline_pages))[:10]

                if not timeline_pages:
                    continue

                # Implementation phases
                phases = ["Pilot", "Early Adoption", "Scaling", "Full Deployment", "Optimization"]

                for page in timeline_pages[:5]:
                    text = extractor.extract_text_from_page(page)

                    for phase in phases:
                        if phase.lower() in text.lower():
                            # Extract timing and metrics
                            patterns = [
                                f"{phase}.*?(\d+(?:\.\d+)?)\s*(?:months|quarters|years)",
                                f"{phase}.*?(\d{{4}})",  # Year
                                f"{phase}.*?Q(\d)\s*(\d{{4}})",  # Quarter and year
                            ]

                            duration = None
                            target_date = None

                            for pattern in patterns:
                                matches = re.findall(pattern, text, re.IGNORECASE)
                                if matches:
                                    if (
                                        "months" in pattern
                                        or "quarters" in pattern
                                        or "years" in pattern
                                    ):
                                        duration = f"{matches[0]} {pattern.split()[-1]}"
                                    elif "Q" in pattern:
                                        target_date = f"Q{matches[0][0]} {matches[0][1]}"
                                    else:
                                        target_date = matches[0]
                                    break

                            timeline_data.append(
                                {
                                    "phase": phase,
                                    "duration": duration,
                                    "target_date": target_date,
                                    "status": self._determine_phase_status(phase, text),
                                }
                            )

            if timeline_data:
                df = pd.DataFrame(timeline_data)
                # Order phases logically
                phase_order = {
                    "Pilot": 0,
                    "Early Adoption": 1,
                    "Scaling": 2,
                    "Full Deployment": 3,
                    "Optimization": 4,
                }
                df["order"] = df["phase"].map(phase_order)
                df = df.sort_values("order").drop("order", axis=1)

                logger.info(f"Extracted {len(df)} implementation phases")
                return df

        except Exception as e:
            logger.error(f"Error extracting implementation timeline: {e}")

        return None

    def _determine_phase_status(self, phase: str, text: str) -> str:
        """Determine status of implementation phase."""
        context = text[
            max(0, text.lower().find(phase.lower()) - 100) : text.lower().find(phase.lower()) + 100
        ].lower()

        if any(term in context for term in ["completed", "achieved", "finished"]):
            return "Completed"
        elif any(term in context for term in ["current", "ongoing", "in progress"]):
            return "In Progress"
        elif any(term in context for term in ["planned", "upcoming", "future"]):
            return "Planned"
        else:
            return "Identified"

    def _extract_economic_implications(self) -> Optional[pd.DataFrame]:
        """Extract economic implications data."""
        logger.info("Extracting economic implications...")

        economic_data = []

        try:
            for extractor in self.extractors:
                # Keywords for economic implications
                keywords = ["economic", "GDP", "growth", "impact", "trillion", "billion"]

                economic_pages = []
                for keyword in keywords:
                    pages = extractor.find_pages_with_keyword(keyword)
                    economic_pages.extend(pages)

                economic_pages = sorted(set(economic_pages))[:10]

                if not economic_pages:
                    continue

                # Extract economic metrics
                for page in economic_pages[:5]:
                    text = extractor.extract_text_from_page(page)

                    # Patterns for economic data
                    patterns = [
                        r"\$(\d+(?:\.\d+)?)\s*(trillion|billion)\s*(?:in\s+)?(?:economic\s+)?(?:value|impact|benefit)",
                        r"(\d+(?:\.\d+)?)\s*%\s*GDP\s*(?:growth|increase|impact)",
                        r"economic\s*(?:impact|benefit|value)\s*of\s*\$(\d+(?:\.\d+)?)\s*(trillion|billion)",
                        r"add\s*(\d+(?:\.\d+)?)\s*%\s*to\s*(?:economic\s+)?growth",
                    ]

                    for pattern in patterns:
                        matches = re.findall(pattern, text, re.IGNORECASE)
                        for match in matches:
                            economic_data.append(self._parse_economic_match(match, pattern))

            if economic_data:
                df = pd.DataFrame(economic_data)
                df = df.dropna(subset=["metric"])
                df = df[df["value"] > 0]
                df = df.drop_duplicates()

                logger.info(f"Extracted {len(df)} economic implication metrics")
                return df

        except Exception as e:
            logger.error(f"Error extracting economic implications: {e}")

        return None

    def _parse_economic_match(self, match: tuple, pattern: str) -> Dict:
        """Parse economic data match."""
        result = {"metric": "", "value": 0, "unit": "", "scope": ""}

        try:
            if "$" in pattern and ("trillion" in pattern or "billion" in pattern):
                # Dollar amount pattern
                value = float(match[0])
                unit = match[1].lower()

                # Convert to billions for consistency
                if unit == "trillion":
                    value = value * 1000

                result["metric"] = "Economic value"
                result["value"] = value
                result["unit"] = "billions_usd"
                result["scope"] = "Total impact"

            elif "GDP" in pattern:
                # GDP impact pattern
                result["metric"] = "GDP impact"
                result["value"] = float(match[0] if isinstance(match, str) else match[0])
                result["unit"] = "percentage"
                result["scope"] = "Annual growth"

            else:
                # Generic economic growth
                result["metric"] = "Economic growth"
                result["value"] = float(match[0] if isinstance(match, str) else match[0])
                result["unit"] = "percentage"
                result["scope"] = "General"

        except (ValueError, IndexError):
            pass

        return result

    def validate(self, data: Dict[str, pd.DataFrame]) -> bool:
        if not data:
            raise ValueError("No data extracted from PDFs")
        logger.info(f"Extracted datasets: {list(data.keys())}")
        if "genai_adoption_speed" in data:
            df = data["genai_adoption_speed"]
            if "metric" not in df.columns or "value" not in df.columns:
                raise ValueError("GenAI adoption missing required columns")
        if "productivity_impact" in data:
            df = data["productivity_impact"]
            if "metric" not in df.columns:
                raise ValueError("Productivity impact missing 'metric' column")
        logger.info("Data validation passed")
        return True


__all__ = ["RichmondFedLoader", "StLouisFedLoader"]
