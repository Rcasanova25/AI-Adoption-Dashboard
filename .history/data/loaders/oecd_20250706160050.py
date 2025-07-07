"""OECD AI Policy Observatory data loader with actual PDF extraction."""

import logging
import re
from pathlib import Path
from typing import Dict, List, Optional

import pandas as pd

from config.settings import settings

from ..extractors.pdf_extractor import PDFExtractor
from ..models.governance import GovernanceMetrics, PolicyFramework
from .base import BaseDataLoader, DataSource

logger = logging.getLogger(__name__)


class OECDLoader(BaseDataLoader):
    """Loader for OECD AI Policy Observatory data with real PDF extraction."""

    def __init__(self, policy_file: Optional[Path] = None, adoption_file: Optional[Path] = None):
        """Initialize with OECD report file paths."""
        if policy_file is None:
            policy_file = settings.get_resources_path() / "AI dashboard resources 1/be745f04-en.pdf"

        source = DataSource(
            name="OECD AI Policy Observatory",
            version="2025",
            url="https://oecd.ai",
            file_path=policy_file,
            citation="Organisation for Economic Co-operation and Development. 'OECD AI Policy Observatory.' 2025.",
        )
        super().__init__(source)

        self.adoption_file = adoption_file or (
            settings.get_resources_path() / "AI Adoption Resources 3/f9ef33c3-en.pdf"
        )

        # Initialize PDF extractors
        self.extractors = []

        # Primary policy file
        if self.source.file_path and self.source.file_path.exists():
            try:
                extractor = PDFExtractor(self.source.file_path)
                self.extractors.append(extractor)
                logger.info(f"Initialized PDF extractor for {self.source.file_path.name}")
            except Exception as e:
                logger.error(f"Failed to initialize PDF extractor: {e}")

        # Adoption file
        if self.adoption_file and self.adoption_file.exists():
            try:
                extractor = PDFExtractor(self.source.file_path)
                self.extractors.append(extractor)
                logger.info(f"Initialized PDF extractor for {self.adoption_file.name}")
            except Exception as e:
                logger.error(f"Failed to initialize PDF extractor for adoption file: {e}")

    def load(self) -> Dict[str, pd.DataFrame]:
        """Load all datasets from OECD reports using actual PDF extraction."""
        logger.info(f"Loading data from {self.source.name}")

        if not self.extractors:
            logger.error("No PDF extractors available; cannot load data.")
            raise RuntimeError("No PDF extractors available; cannot load data.")

        datasets = {}

        try:
            # Extract different policy and governance aspects

            # 1. National AI strategies
            national_strategies = self._extract_national_strategies()
            if national_strategies is not None and not national_strategies.empty:
                datasets["national_ai_strategies"] = national_strategies

            # 2. Policy instruments
            policy_instruments = self._extract_policy_instruments()
            if policy_instruments is not None and not policy_instruments.empty:
                datasets["policy_instruments"] = policy_instruments

            # 3. AI principles adoption
            principles_adoption = self._extract_principles_adoption()
            if principles_adoption is not None and not principles_adoption.empty:
                datasets["ai_principles_adoption"] = principles_adoption

            # 4. Regulatory approaches
            regulatory_approaches = self._extract_regulatory_approaches()
            if regulatory_approaches is not None and not regulatory_approaches.empty:
                datasets["regulatory_approaches"] = regulatory_approaches

            # 5. International cooperation
            international_cooperation = self._extract_international_cooperation()
            if international_cooperation is not None and not international_cooperation.empty:
                datasets["international_cooperation"] = international_cooperation

            # 6. Skills initiatives
            skills_initiatives = self._extract_skills_initiatives()
            if skills_initiatives is not None and not skills_initiatives.empty:
                datasets["skills_initiatives"] = skills_initiatives

            # 7. Public investment trends
            public_investment = self._extract_public_investment()
            if public_investment is not None and not public_investment.empty:
                datasets["public_investment"] = public_investment

        except Exception as e:
            logger.error(f"Error during PDF extraction: {e}")
            raise

        # Validate datasets
        if datasets:
            self.validate(datasets)
        else:
            logger.error("No data extracted from PDFs; cannot proceed.")
            raise RuntimeError("No data extracted from PDFs.")

        return datasets

    def _extract_national_strategies(self) -> Optional[pd.DataFrame]:
        """Extract national AI strategy data from PDFs."""
        logger.info("Extracting national AI strategies...")

        strategy_data = []

        try:
            for extractor in self.extractors:
                # Keywords for national strategy sections
                keywords = [
                    "national",
                    "strategy",
                    "country",
                    "government",
                    "policy",
                    "framework",
                    "initiative",
                    "plan",
                ]

                strategy_pages = []
                for keyword in keywords:
                    pages = extractor.find_pages_with_keyword(keyword)
                    strategy_pages.extend(pages)

                strategy_pages = sorted(set(strategy_pages))[:15]

                if not strategy_pages:
                    continue

                # Countries to look for
                countries = [
                    "United States",
                    "China",
                    "United Kingdom",
                    "Germany",
                    "France",
                    "Canada",
                    "Japan",
                    "South Korea",
                    "India",
                    "Australia",
                    "Singapore",
                    "Netherlands",
                    "Sweden",
                    "Israel",
                    "Finland",
                    "Denmark",
                    "Norway",
                    "Switzerland",
                    "Italy",
                    "Spain",
                ]

                for page in strategy_pages[:10]:
                    text = extractor.extract_text_from_page(page)

                    for country in countries:
                        if country.lower() in text.lower():
                            # Extract strategy information
                            strategy_info = self._extract_country_strategy(text, country)
                            if strategy_info:
                                strategy_data.append(strategy_info)

                # Look for strategy tables
                for page in strategy_pages[:5]:
                    tables = extractor.extract_tables(page_range=(page, page))
                    for table in tables:
                        if table.empty:
                            continue

                        # Check if table contains country data
                        table_str = table.to_string().lower()
                        if any(country.lower() in table_str for country in countries[:5]):
                            processed = self._process_strategy_table(table)
                            if processed:
                                strategy_data.extend(processed)

            if strategy_data:
                df = pd.DataFrame(strategy_data)
                df = df.drop_duplicates(subset=["country"])
                df = df.sort_values("strategy_maturity_score", ascending=False).head(15)

                logger.info(f"Extracted strategies for {len(df)} countries")
                return df

        except Exception as e:
            logger.error(f"Error extracting national strategies: {e}")

        return None

    def _extract_country_strategy(self, text: str, country: str) -> Optional[Dict]:
        """Extract strategy information for a specific country."""
        result = {"country": country}

        # Find context around country name
        country_pos = text.lower().find(country.lower())
        if country_pos == -1:
            return None

        context = text[max(0, country_pos - 500) : country_pos + 500]

        # Extract launch year
        year_match = re.search(
            r"(20[1-2]\d)\s*(?:launch|establish|introduce|adopt)", context, re.IGNORECASE
        )
        if year_match:
            result["strategy_launch_year"] = int(year_match.group(1))

        # Extract funding
        funding_patterns = [
            r"\$(\d+(?:\.\d+)?)\s*(billion|million)",
            r"(\d+(?:\.\d+)?)\s*(billion|million)\s*(?:USD|dollars?)",
            r"invest(?:ment|ing)?\s*(?:of\s*)?\$?(\d+(?:\.\d+)?)\s*(billion|million)",
        ]

        for pattern in funding_patterns:
            matches = re.findall(pattern, context, re.IGNORECASE)
            if matches:
                amount = float(matches[0][0])
                unit = matches[0][1].lower()
                if unit == "million":
                    amount = amount / 1000  # Convert to billions
                result["public_funding_billions"] = amount
                break

        # Extract maturity indicators
        maturity_keywords = {
            "comprehensive": 2,
            "advanced": 2,
            "leading": 2,
            "established": 1.5,
            "mature": 1.5,
            "robust": 1.5,
            "developing": 1,
            "emerging": 0.8,
            "initial": 0.5,
        }

        maturity_score = 7.0  # Base score
        for keyword, modifier in maturity_keywords.items():
            if keyword in context.lower():
                maturity_score += modifier
                break

        result["strategy_maturity_score"] = min(10.0, maturity_score)

        # Check for governance framework
        result["ai_governance_framework"] = any(
            term in context.lower() for term in ["governance", "regulatory", "oversight"]
        )

        # Check for ethics guidelines
        result["ethics_guidelines"] = any(
            term in context.lower() for term in ["ethics", "ethical", "principles", "responsible"]
        )

        return result if "strategy_launch_year" in result else None

    def _process_strategy_table(self, table: pd.DataFrame) -> List[Dict]:
        """Process table containing strategy information."""
        results = []

        # Identify country column
        country_col = None
        for col in table.columns:
            sample_vals = table[col].astype(str).str.lower()
            if any("united" in val or "china" in val or "germany" in val for val in sample_vals):
                country_col = col
                break

        if not country_col:
            return results

        # Extract data for each country
        for _, row in table.iterrows():
            country = str(row[country_col]).strip()
            if not country or country.lower() == "nan":
                continue

            result = {"country": country}

            for col in table.columns:
                if col == country_col:
                    continue

                col_lower = str(col).lower()
                value_str = str(row[col])

                try:
                    if "year" in col_lower:
                        result["strategy_launch_year"] = int(float(value_str))
                    elif "fund" in col_lower or "invest" in col_lower:
                        # Extract numeric value
                        numeric_match = re.search(r"(\d+(?:\.\d+)?)", value_str)
                        if numeric_match:
                            result["public_funding_billions"] = float(numeric_match.group(1))
                    elif "score" in col_lower or "maturity" in col_lower:
                        result["strategy_maturity_score"] = float(value_str)
                except ValueError:
                    continue

            if len(result) > 1:
                results.append(result)

        return results

    def _extract_policy_instruments(self) -> Optional[pd.DataFrame]:
        """Extract AI policy instruments data."""
        logger.info("Extracting policy instruments...")

        instrument_data = []

        try:
            for extractor in self.extractors:
                # Keywords for policy instruments
                keywords = [
                    "policy",
                    "instrument",
                    "measure",
                    "initiative",
                    "program",
                    "incentive",
                    "funding",
                    "regulatory",
                ]

                policy_pages = []
                for keyword in keywords:
                    pages = extractor.find_pages_with_keyword(keyword)
                    policy_pages.extend(pages)

                policy_pages = sorted(set(policy_pages))[:10]

                if not policy_pages:
                    continue

                # Policy instrument types to look for
                instruments = [
                    "R&D Funding",
                    "Tax Incentives",
                    "Regulatory Sandboxes",
                    "Public-Private Partnerships",
                    "Skills Programs",
                    "Data Governance",
                    "Ethics Boards",
                    "Standards Development",
                    "International Cooperation",
                    "Public Procurement",
                    "Innovation Hubs",
                    "Testbeds",
                    "Certification Schemes",
                ]

                for page in policy_pages[:5]:
                    text = extractor.extract_text_from_page(page)

                    for instrument in instruments:
                        if instrument.lower() in text.lower():
                            # Extract instrument metrics
                            metrics = self._extract_instrument_metrics(text, instrument)
                            if metrics:
                                instrument_data.append(metrics)

            if instrument_data:
                df = pd.DataFrame(instrument_data)
                df = df.drop_duplicates(subset=["instrument_type"])

                logger.info(f"Extracted {len(df)} policy instruments")
                return df

        except Exception as e:
            logger.error(f"Error extracting policy instruments: {e}")

        return None

    def _extract_instrument_metrics(self, text: str, instrument: str) -> Optional[Dict]:
        """Extract metrics for a specific policy instrument."""
        result = {"instrument_type": instrument}

        # Find context around instrument
        instrument_pos = text.lower().find(instrument.lower())
        if instrument_pos == -1:
            return None

        context = text[max(0, instrument_pos - 400) : instrument_pos + 400]

        # Extract number of countries implementing
        country_patterns = [
            r"(\d+)\s*countr(?:ies|y)\s*(?:implement|adopt|use)",
            r"implement(?:ed|ing)?\s*(?:in|by)\s*(\d+)\s*countr",
            r"(\d+)\s*(?:nations?|states?|governments?)\s*(?:have|has)",
        ]

        for pattern in country_patterns:
            matches = re.findall(pattern, context, re.IGNORECASE)
            if matches:
                result["countries_implementing"] = int(matches[0])
                break

        # Extract effectiveness or impact scores
        score_patterns = [
            r"effectiveness\s*(?:score|rating)?\s*(?:of\s*)?(\d+(?:\.\d+)?)",
            r"(\d+(?:\.\d+)?)\s*(?:out of 10|/10)\s*effectiveness",
            r"impact\s*(?:score|rating)?\s*(?:of\s*)?(\d+(?:\.\d+)?)",
        ]

        for pattern in score_patterns:
            matches = re.findall(pattern, context, re.IGNORECASE)
            if matches:
                result["effectiveness_score"] = float(matches[0])
                break

        # Assess implementation complexity
        if any(term in context.lower() for term in ["complex", "difficult", "challenging"]):
            result["implementation_complexity"] = "High"
        elif any(term in context.lower() for term in ["moderate", "manageable"]):
            result["implementation_complexity"] = "Medium"
        elif any(term in context.lower() for term in ["simple", "easy", "straightforward"]):
            result["implementation_complexity"] = "Low"

        # Extract budget if available
        budget_match = re.search(r"\$(\d+(?:\.\d+)?)\s*(million|billion)", context, re.IGNORECASE)
        if budget_match:
            amount = float(budget_match.group(1))
            if budget_match.group(2).lower() == "billion":
                amount = amount * 1000  # Convert to millions
            result["avg_budget_millions"] = amount

        return result if "countries_implementing" in result else None

    def _extract_principles_adoption(self) -> Optional[pd.DataFrame]:
        """Extract OECD AI Principles adoption data."""
        logger.info("Extracting AI principles adoption...")

        principles_data = []

        try:
            for extractor in self.extractors:
                # Keywords for principles sections
                keywords = [
                    "principle",
                    "ethics",
                    "responsible",
                    "trustworthy",
                    "transparent",
                    "accountable",
                    "fair",
                    "human",
                ]

                principles_pages = []
                for keyword in keywords:
                    pages = extractor.find_pages_with_keyword(keyword)
                    principles_pages.extend(pages)

                principles_pages = sorted(set(principles_pages))[:10]

                if not principles_pages:
                    continue

                # OECD AI Principles to look for
                principles = [
                    "Inclusive growth and well-being",
                    "Human-centered values",
                    "Transparency and explainability",
                    "Robustness and safety",
                    "Accountability",
                    "Privacy and data governance",
                    "Human oversight",
                    "Non-discrimination and fairness",
                ]

                for page in principles_pages[:5]:
                    text = extractor.extract_text_from_page(page)

                    for principle in principles:
                        # Look for principle mentions
                        principle_keywords = principle.lower().split()
                        if any(keyword in text.lower() for keyword in principle_keywords):
                            # Extract adoption metrics
                            adoption_info = self._extract_principle_adoption(text, principle)
                            if adoption_info:
                                principles_data.append(adoption_info)

            if principles_data:
                df = pd.DataFrame(principles_data)
                df = df.drop_duplicates(subset=["principle"])

                logger.info(f"Extracted adoption data for {len(df)} principles")
                return df

        except Exception as e:
            logger.error(f"Error extracting principles adoption: {e}")

        return None

    def _extract_principle_adoption(self, text: str, principle: str) -> Optional[Dict]:
        """Extract adoption information for a specific principle."""
        result = {"principle": principle}

        # Find relevant context
        # Use first keyword of principle for searching
        keyword = principle.split()[0].lower()
        keyword_pos = text.lower().find(keyword)
        if keyword_pos == -1:
            return None

        context = text[max(0, keyword_pos - 500) : keyword_pos + 500]

        # Extract adoption rate
        adoption_patterns = [
            r"(\d+(?:\.\d+)?)\s*%\s*(?:of\s*)?(?:countries|organizations|firms)\s*(?:adopt|implement)",
            r"adopt(?:ed|ion)\s*(?:rate|by)\s*(\d+(?:\.\d+)?)\s*%",
            r"(\d+(?:\.\d+)?)\s*%\s*implementation",
        ]

        for pattern in adoption_patterns:
            matches = re.findall(pattern, context, re.IGNORECASE)
            if matches:
                result["adoption_rate_percent"] = float(matches[0])
                break

        # Extract implementation score
        impl_patterns = [
            r"implementation\s*(?:score|rating)\s*(?:of\s*)?(\d+(?:\.\d+)?)",
            r"(\d+(?:\.\d+)?)\s*(?:out of 10|/10)\s*implementation",
        ]

        for pattern in impl_patterns:
            matches = re.findall(pattern, context, re.IGNORECASE)
            if matches:
                result["implementation_score"] = float(matches[0])
                break

        # Assess policy coverage
        if any(term in context.lower() for term in ["comprehensive", "extensive", "broad"]):
            result["policy_coverage"] = "High"
        elif any(term in context.lower() for term in ["moderate", "partial", "some"]):
            result["policy_coverage"] = "Medium"
        else:
            result["policy_coverage"] = "Low"

        # Assess enforcement level
        if any(term in context.lower() for term in ["mandatory", "required", "enforced"]):
            result["enforcement_level"] = "High"
        elif any(term in context.lower() for term in ["recommended", "suggested", "guidelines"]):
            result["enforcement_level"] = "Medium"
        else:
            result["enforcement_level"] = "Low"

        return result if "adoption_rate_percent" in result else None

    def _extract_regulatory_approaches(self) -> Optional[pd.DataFrame]:
        """Extract AI regulatory approaches by region."""
        logger.info("Extracting regulatory approaches...")

        regulatory_data = []

        try:
            for extractor in self.extractors:
                # Keywords for regulatory sections
                keywords = [
                    "regulatory",
                    "regulation",
                    "compliance",
                    "governance",
                    "framework",
                    "approach",
                    "act",
                    "law",
                ]

                regulatory_pages = []
                for keyword in keywords:
                    pages = extractor.find_pages_with_keyword(keyword)
                    regulatory_pages.extend(pages)

                regulatory_pages = sorted(set(regulatory_pages))[:10]

                if not regulatory_pages:
                    continue

                # Regions to analyze
                regions = {
                    "European Union": ["EU", "European", "AI Act"],
                    "United States": ["US", "United States", "America"],
                    "China": ["China", "Chinese", "PRC"],
                    "United Kingdom": ["UK", "United Kingdom", "Britain"],
                    "Canada": ["Canada", "Canadian"],
                    "Japan": ["Japan", "Japanese"],
                    "Singapore": ["Singapore"],
                    "Australia": ["Australia", "Australian"],
                }

                for page in regulatory_pages[:5]:
                    text = extractor.extract_text_from_page(page)

                    for region, keywords in regions.items():
                        if any(kw.lower() in text.lower() for kw in keywords):
                            # Extract regulatory approach info
                            approach_info = self._extract_regulatory_info(text, region)
                            if approach_info:
                                regulatory_data.append(approach_info)

            if regulatory_data:
                df = pd.DataFrame(regulatory_data)
                df = df.drop_duplicates(subset=["region"])

                logger.info(f"Extracted regulatory approaches for {len(df)} regions")
                return df

        except Exception as e:
            logger.error(f"Error extracting regulatory approaches: {e}")

        return None

    def _extract_regulatory_info(self, text: str, region: str) -> Optional[Dict]:
        """Extract regulatory information for a specific region."""
        result = {"region": region}

        # Identify regulatory approach type
        approaches = {
            "Comprehensive": ["comprehensive", "detailed", "prescriptive"],
            "Risk-based": ["risk-based", "proportionate", "tiered"],
            "Principles-based": ["principles", "outcomes", "flexible"],
            "Sectoral": ["sectoral", "industry-specific", "targeted"],
            "Voluntary": ["voluntary", "self-regulation", "guidelines"],
            "Co-regulatory": ["co-regulatory", "partnership", "collaborative"],
        }

        for approach, keywords in approaches.items():
            if any(kw in text.lower() for kw in keywords):
                result["regulatory_approach"] = approach
                break

        # Extract implementation stage
        stages = {
            "Adopted": ["adopted", "enacted", "in force"],
            "Developing": ["developing", "drafting", "considering"],
            "Consultation": ["consultation", "feedback", "comment period"],
            "Pilot": ["pilot", "trial", "testing"],
        }

        for stage, keywords in stages.items():
            if any(kw in text.lower() for kw in keywords):
                result["implementation_stage"] = stage
                break

        # Extract numeric metrics
        # Industry alignment score
        alignment_match = re.search(
            r"industry\s*alignment\s*(?:score|rating)?\s*(?:of\s*)?(\d+(?:\.\d+)?)",
            text,
            re.IGNORECASE,
        )
        if alignment_match:
            result["industry_alignment"] = float(alignment_match.group(1))

        # Innovation impact
        innovation_patterns = [
            r"(\d+(?:\.\d+)?)\s*%\s*(?:impact on|effect on)\s*innovation",
            r"innovation\s*(?:impact|effect)\s*(?:of\s*)?([+-]?\d+(?:\.\d+)?)\s*%",
        ]

        for pattern in innovation_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                result["innovation_impact"] = float(matches[0])
                break

        # Compliance cost
        cost_match = re.search(
            r"compliance\s*cost\s*(?:index|score)?\s*(?:of\s*)?(\d+(?:\.\d+)?)", text, re.IGNORECASE
        )
        if cost_match:
            result["compliance_cost_index"] = float(cost_match.group(1))

        return result if "regulatory_approach" in result else None

    def _extract_international_cooperation(self) -> Optional[pd.DataFrame]:
        """Extract international AI cooperation initiatives."""
        logger.info("Extracting international cooperation data...")

        cooperation_data = []

        try:
            for extractor in self.extractors:
                # Keywords for international cooperation
                keywords = [
                    "international",
                    "cooperation",
                    "partnership",
                    "alliance",
                    "multilateral",
                    "bilateral",
                    "global",
                    "initiative",
                ]

                cooperation_pages = []
                for keyword in keywords:
                    pages = extractor.find_pages_with_keyword(keyword)
                    cooperation_pages.extend(pages)

                cooperation_pages = sorted(set(cooperation_pages))[:10]

                if not cooperation_pages:
                    continue

                # Known initiatives to look for
                initiatives = [
                    "GPAI",
                    "Global Partnership on AI",
                    "OECD AI",
                    "OECD AI Principles",
                    "UNESCO AI Ethics",
                    "EU-US TTC",
                    "Trade and Technology Council",
                    "Quad AI",
                    "Council of Europe AI",
                    "ISO/IEC AI Standards",
                    "UN AI Advisory",
                ]

                for page in cooperation_pages[:5]:
                    text = extractor.extract_text_from_page(page)

                    # Extract tables with cooperation data
                    tables = extractor.extract_tables(page_range=(page, page))
                    for table in tables:
                        if table.empty:
                            continue

                        processed = self._process_cooperation_table(table)
                        if processed:
                            cooperation_data.extend(processed)

                    # Also extract from text
                    for initiative in initiatives:
                        if initiative.lower() in text.lower():
                            info = self._extract_initiative_info(text, initiative)
                            if info:
                                cooperation_data.append(info)

            if cooperation_data:
                df = pd.DataFrame(cooperation_data)
                # Clean up initiative names
                df = df.drop_duplicates(subset=["initiative"])

                logger.info(f"Extracted {len(df)} cooperation initiatives")
                return df

        except Exception as e:
            logger.error(f"Error extracting international cooperation: {e}")

        return None

    def _extract_initiative_info(self, text: str, initiative: str) -> Optional[Dict]:
        """Extract information about a specific cooperation initiative."""
        result = {"initiative": initiative.split(",")[0]}  # Use short name

        # Find context
        init_pos = text.lower().find(initiative.lower())
        if init_pos == -1:
            return None

        context = text[max(0, init_pos - 400) : init_pos + 400]

        # Extract member countries
        member_patterns = [
            r"(\d+)\s*(?:member|participating)\s*countr",
            r"(\d+)\s*countr(?:ies|y)\s*(?:participate|involved)",
            r"membership\s*of\s*(\d+)",
        ]

        for pattern in member_patterns:
            matches = re.findall(pattern, context, re.IGNORECASE)
            if matches:
                result["member_countries"] = int(matches[0])
                break

        # Identify focus area
        focus_areas = {
            "Responsible AI": ["responsible", "ethical", "trustworthy"],
            "Policy coordination": ["policy", "coordination", "harmonization"],
            "Technical standards": ["standards", "technical", "interoperability"],
            "Security": ["security", "safety", "defense"],
            "Human rights": ["rights", "fundamental", "protection"],
            "Global governance": ["governance", "oversight", "regulation"],
        }

        for area, keywords in focus_areas.items():
            if any(kw in context.lower() for kw in keywords):
                result["focus_area"] = area
                break

        # Extract effectiveness score if available
        eff_match = re.search(
            r"effectiveness\s*(?:score|rating)?\s*(?:of\s*)?(\d+(?:\.\d+)?)", context, re.IGNORECASE
        )
        if eff_match:
            result["effectiveness_score"] = float(eff_match.group(1))

        # Extract budget
        budget_match = re.search(r"\$(\d+(?:\.\d+)?)\s*(million|billion)", context, re.IGNORECASE)
        if budget_match:
            amount = float(budget_match.group(1))
            if budget_match.group(2).lower() == "billion":
                amount = amount * 1000
            result["budget_millions"] = amount

        return result if "member_countries" in result else None

    def _process_cooperation_table(self, table: pd.DataFrame) -> List[Dict]:
        """Process table containing cooperation initiative data."""
        results = []

        # Identify initiative column
        init_col = None
        for col in table.columns:
            sample_vals = table[col].astype(str).str.lower()
            if any("gpai" in val or "oecd" in val or "unesco" in val for val in sample_vals):
                init_col = col
                break

        if not init_col:
            return results

        # Extract data
        for _, row in table.iterrows():
            initiative = str(row[init_col]).strip()
            if not initiative or initiative.lower() == "nan":
                continue

            result = {"initiative": initiative}

            for col in table.columns:
                if col == init_col:
                    continue

                col_lower = str(col).lower()
                value_str = str(row[col])

                try:
                    if "member" in col_lower or "countr" in col_lower:
                        result["member_countries"] = int(float(value_str))
                    elif "budget" in col_lower or "fund" in col_lower:
                        result["budget_millions"] = float(value_str)
                    elif "score" in col_lower or "effectiveness" in col_lower:
                        result["effectiveness_score"] = float(value_str)
                    elif "focus" in col_lower or "area" in col_lower:
                        result["focus_area"] = value_str
                except ValueError:
                    continue

            if len(result) > 1:
                results.append(result)

        return results

    def _extract_skills_initiatives(self) -> Optional[pd.DataFrame]:
        """Extract AI skills and education initiatives."""
        logger.info("Extracting skills initiatives...")

        skills_data = []

        try:
            for extractor in self.extractors:
                # Keywords for skills sections
                keywords = [
                    "skills",
                    "education",
                    "training",
                    "workforce",
                    "talent",
                    "reskilling",
                    "upskilling",
                    "curriculum",
                ]

                skills_pages = []
                for keyword in keywords:
                    pages = extractor.find_pages_with_keyword(keyword)
                    skills_pages.extend(pages)

                skills_pages = sorted(set(skills_pages))[:10]

                if not skills_pages:
                    continue

                # Countries to analyze
                countries = [
                    "Singapore",
                    "Finland",
                    "Canada",
                    "South Korea",
                    "Germany",
                    "United Kingdom",
                    "France",
                    "Japan",
                    "Australia",
                    "Netherlands",
                    "Denmark",
                    "Sweden",
                    "United States",
                    "China",
                    "India",
                ]

                for page in skills_pages[:5]:
                    text = extractor.extract_text_from_page(page)

                    for country in countries:
                        if country.lower() in text.lower():
                            # Extract skills initiative data
                            skills_info = self._extract_country_skills(text, country)
                            if skills_info:
                                skills_data.append(skills_info)

            if skills_data:
                df = pd.DataFrame(skills_data)
                df = df.drop_duplicates(subset=["country"])
                df = df.head(10)  # Top 10 countries

                logger.info(f"Extracted skills initiatives for {len(df)} countries")
                return df

        except Exception as e:
            logger.error(f"Error extracting skills initiatives: {e}")

        return None

    def _extract_country_skills(self, text: str, country: str) -> Optional[Dict]:
        """Extract skills initiative data for a specific country."""
        result = {"country": country}

        # Find context around country
        country_pos = text.lower().find(country.lower())
        if country_pos == -1:
            return None

        context = text[max(0, country_pos - 500) : country_pos + 500]

        # Check for AI in curriculum
        result["ai_in_curriculum"] = any(
            term in context.lower() for term in ["curriculum", "education system", "schools"]
        )

        # Extract number of reskilling programs
        program_patterns = [
            r"(\d+)\s*(?:reskilling|upskilling|training)\s*programs?",
            r"(\d+)\s*programs?\s*(?:for|to)\s*(?:reskill|upskill|train)",
        ]

        for pattern in program_patterns:
            matches = re.findall(pattern, context, re.IGNORECASE)
            if matches:
                result["reskilling_programs"] = int(matches[0])
                break

        # Extract training budget
        budget_match = re.search(
            r"\$(\d+(?:\.\d+)?)\s*(million|billion)\s*(?:for\s*)?training", context, re.IGNORECASE
        )
        if budget_match:
            amount = float(budget_match.group(1))
            if budget_match.group(2).lower() == "billion":
                amount = amount * 1000
            result["public_training_budget_millions"] = amount

        # Extract citizens trained
        trained_patterns = [
            r"(\d+(?:,\d+)?)\s*(?:thousand|K)\s*(?:citizens?|people|workers?)\s*trained",
            r"trained\s*(\d+(?:,\d+)?)\s*(?:thousand|K)\s*(?:citizens?|people|workers?)",
        ]

        for pattern in trained_patterns:
            matches = re.findall(pattern, context, re.IGNORECASE)
            if matches:
                # Convert to number
                value = matches[0].replace(",", "")
                result["citizens_trained_thousands"] = int(value)
                break

        # Extract partnership score
        if any(term in context.lower() for term in ["partnership", "collaboration", "industry"]):
            # Simple heuristic based on keywords
            score = 7.0
            if "strong" in context.lower() or "extensive" in context.lower():
                score += 1.5
            if "leading" in context.lower() or "exemplary" in context.lower():
                score += 0.7
            result["industry_partnership_score"] = min(10.0, score)

        return result if "reskilling_programs" in result else None

    def _extract_public_investment(self) -> Optional[pd.DataFrame]:
        """Extract public AI investment trends."""
        logger.info("Extracting public investment data...")

        investment_data = []

        try:
            for extractor in self.extractors:
                # Keywords for investment sections
                keywords = [
                    "investment",
                    "funding",
                    "budget",
                    "spending",
                    "expenditure",
                    "billion",
                    "million",
                    "public",
                ]

                investment_pages = []
                for keyword in keywords:
                    pages = extractor.find_pages_with_keyword(keyword)
                    investment_pages.extend(pages)

                investment_pages = sorted(set(investment_pages))[:10]

                if not investment_pages:
                    continue

                # Look for investment tables
                for page in investment_pages[:5]:
                    tables = extractor.extract_tables(page_range=(page, page))

                    for table in tables:
                        if table.empty:
                            continue

                        # Check if table contains year and investment data
                        table_str = table.to_string().lower()
                        if "20" in table_str and any(
                            term in table_str for term in ["billion", "investment", "funding"]
                        ):
                            processed = self._process_investment_table(table)
                            if processed:
                                investment_data.extend(processed)

                # Also extract from text
                for page in investment_pages[:5]:
                    text = extractor.extract_text_from_page(page)

                    # Extract year-wise investment data
                    year_patterns = [
                        r"(20[1-3]\d)\s*[:]\s*\$?(\d+(?:\.\d+)?)\s*(billion|million)",
                        r"in\s*(20[1-3]\d)\s*.*?\$?(\d+(?:\.\d+)?)\s*(billion|million)\s*(?:in\s*)?(?:AI\s*)?investment",
                    ]

                    for pattern in year_patterns:
                        matches = re.findall(pattern, text, re.IGNORECASE)
                        for match in matches:
                            year = int(match[0])
                            amount = float(match[1])
                            unit = match[2].lower()

                            if unit == "million":
                                amount = amount / 1000  # Convert to billions

                            # Look for regional breakdown
                            investment_info = {
                                "year": year,
                                "global_public_investment_billions": amount,
                            }

                            # Extract regional shares if available
                            regional_info = self._extract_regional_shares(text, year)
                            if regional_info:
                                investment_info.update(regional_info)

                            investment_data.append(investment_info)

            if investment_data:
                # Consolidate by year
                df = pd.DataFrame(investment_data)
                df = df.groupby("year").first().reset_index()
                df = df.sort_values("year")

                logger.info(f"Extracted public investment data for {len(df)} years")
                return df

        except Exception as e:
            logger.error(f"Error extracting public investment: {e}")

        return None

    def _process_investment_table(self, table: pd.DataFrame) -> List[Dict]:
        """Process table containing investment data."""
        results = []

        # Identify year column
        year_col = None
        for col in table.columns:
            sample_vals = table[col].astype(str)
            if sample_vals.str.contains("20[1-3]\\d").sum() > 0:
                year_col = col
                break

        if not year_col:
            return results

        # Extract investment data
        for _, row in table.iterrows():
            try:
                year = int(float(str(row[year_col])))
                if year < 2015 or year > 2030:
                    continue

                result = {"year": year}

                for col in table.columns:
                    if col == year_col:
                        continue

                    col_lower = str(col).lower()
                    value_str = str(row[col])

                    try:
                        if "global" in col_lower or "total" in col_lower:
                            result["global_public_investment_billions"] = float(value_str)
                        elif "us" in col_lower or "united states" in col_lower:
                            result["us_share_percent"] = float(value_str)
                        elif "china" in col_lower:
                            result["china_share_percent"] = float(value_str)
                        elif "eu" in col_lower or "europe" in col_lower:
                            result["eu_share_percent"] = float(value_str)
                        elif "safety" in col_lower or "security" in col_lower:
                            result["focus_on_safety_percent"] = float(value_str)
                    except ValueError:
                        continue

                if len(result) > 1:
                    results.append(result)

            except ValueError:
                continue

        return results

    def _extract_regional_shares(self, text: str, year: int) -> Optional[Dict]:
        """Extract regional investment shares for a given year."""
        result = {}

        # Look for regional breakdown near year mention
        year_pos = text.find(str(year))
        if year_pos == -1:
            return None

        context = text[max(0, year_pos - 500) : year_pos + 500]

        # Regional patterns
        regions = {
            "us_share_percent": ["US", "United States", "America"],
            "china_share_percent": ["China", "Chinese"],
            "eu_share_percent": ["EU", "Europe", "European Union"],
        }

        for key, keywords in regions.items():
            for keyword in keywords:
                pattern = f"{keyword}.*?(\d+(?:\.\d+)?)\s*%"
                match = re.search(pattern, context, re.IGNORECASE)
                if match:
                    result[key] = float(match.group(1))
                    break

        # Calculate other share if main regions found
        if len(result) >= 3:
            total = sum(result.values())
            if total < 100:
                result["other_share_percent"] = 100 - total

        return result if result else None

    def validate(self, data: Dict[str, pd.DataFrame]) -> bool:
        """Validate loaded data meets expected schema."""
        if not data:
            raise ValueError("No data extracted from PDFs")

        logger.info(f"Extracted datasets: {list(data.keys())}")

        # Validate key datasets if present
        required_datasets = [
            "national_ai_strategies",
            "policy_instruments",
            "ai_principles_adoption",
            "regulatory_approaches",
        ]

        present_required = [ds for ds in required_datasets if ds in data]
        if len(present_required) < 2:
            logger.warning(f"Only {len(present_required)} of 4 required datasets present")

        # Validate national strategies if present
        if "national_ai_strategies" in data:
            df = data["national_ai_strategies"]
            if "country" not in df.columns:
                raise ValueError("National strategies missing 'country' column")

        # Validate policy instruments if present
        if "policy_instruments" in data:
            df = data["policy_instruments"]
            if "instrument_type" not in df.columns:
                raise ValueError("Policy instruments missing 'instrument_type' column")

        logger.info("Data validation passed")
        return True


__all__ = ["OECDLoader"]
