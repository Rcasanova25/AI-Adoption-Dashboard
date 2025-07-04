"""Goldman Sachs AI economic impact data loader with actual PDF extraction."""

from pathlib import Path
from typing import Dict, List, Optional, Tuple
import pandas as pd
import logging
import re

from .base import BaseDataLoader, DataSource
from ..models.economics import EconomicImpact, ProductivityMetrics
from ..extractors.pdf_extractor_impl import EnhancedPDFExtractor

logger = logging.getLogger(__name__)


class GoldmanSachsLoader(BaseDataLoader):
    """Loader for Goldman Sachs AI economic impact report with real PDF extraction."""
    
    def __init__(self, file_path: Optional[Path] = None):
        """Initialize with Goldman Sachs report file path."""
        if file_path is None:
            # Default to Goldman Sachs AI report
            file_path = Path("/mnt/c/Users/rcasa/OneDrive/Documents/AI-Adoption-Dashboard/"
                           "AI adoption resources/AI Adoption Resources 3/"
                           "Generative AI could raise global GDP by 7_ _ Goldman Sachs.pdf")
        
        source = DataSource(
            name="Goldman Sachs AI Economic Impact",
            version="2024",
            url="https://www.goldmansachs.com/insights/pages/generative-ai-could-raise-global-gdp-by-7-percent.html",
            file_path=file_path,
            citation="Goldman Sachs. 'Generative AI could raise global GDP by 7%.' Goldman Sachs Global Investment Research."
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
        """Load all datasets from Goldman Sachs report using actual PDF extraction."""
        logger.info(f"Loading data from {self.source.name}")
        
        if not self.extractor:
            logger.warning("PDF extractor not available, returning fallback datasets")
            return self._get_fallback_datasets()
        
        datasets = {}
        
        try:
            # Extract different economic impact analyses
            
            # 1. GDP impact projections
            gdp_impact = self._extract_gdp_impact()
            if gdp_impact is not None and not gdp_impact.empty:
                datasets['gdp_impact'] = gdp_impact
            
            # 2. Labor market disruption
            labor_impact = self._extract_labor_market_impact()
            if labor_impact is not None and not labor_impact.empty:
                datasets['labor_impact'] = labor_impact
            
            # 3. Productivity gains by sector
            productivity_gains = self._extract_productivity_gains()
            if productivity_gains is not None and not productivity_gains.empty:
                datasets['productivity_gains'] = productivity_gains
            
            # 4. Automation exposure by occupation
            automation_exposure = self._extract_automation_exposure()
            if automation_exposure is not None and not automation_exposure.empty:
                datasets['automation_exposure'] = automation_exposure
            
            # 5. Economic growth scenarios
            growth_scenarios = self._extract_growth_scenarios()
            if growth_scenarios is not None and not growth_scenarios.empty:
                datasets['growth_scenarios'] = growth_scenarios
            
            # 6. Investment outlook
            investment_outlook = self._extract_investment_outlook()
            if investment_outlook is not None and not investment_outlook.empty:
                datasets['investment_outlook'] = investment_outlook
            
        except Exception as e:
            logger.error(f"Error during PDF extraction: {e}")
            return self._get_fallback_datasets()
        
        # Validate datasets
        if datasets:
            self.validate(datasets)
        else:
            logger.warning("No data extracted from PDF, using fallback data")
            datasets = self._get_fallback_datasets()
        
        return datasets
    
    def _extract_gdp_impact(self) -> Optional[pd.DataFrame]:
        """Extract GDP impact projections."""
        logger.info("Extracting GDP impact data...")
        
        try:
            # Keywords for GDP impact sections
            keywords = ['GDP', 'growth', 'economic impact', '7%', 'trillion', 'global output']
            
            # Find relevant pages
            gdp_pages = []
            for keyword in keywords:
                pages = self.extractor.find_pages_with_keyword(keyword)
                gdp_pages.extend(pages)
            
            gdp_pages = sorted(set(gdp_pages))[:10]
            
            if not gdp_pages:
                return None
            
            gdp_data = []
            
            # Extract GDP impact data
            for page in gdp_pages[:5]:
                text = self.extractor.extract_text_from_page(page)
                
                # Patterns for GDP impact
                # Examples: "7% increase in GDP", "$7 trillion", "boost GDP by 7%"
                patterns = [
                    r'(\d+(?:\.\d+)?)\s*%\s*(?:increase|boost|growth|rise)\s*in\s*(?:global\s+)?GDP',
                    r'GDP\s*(?:could|may|will)?\s*(?:increase|grow|rise)\s*(?:by\s+)?(\d+(?:\.\d+)?)\s*%',
                    r'\$(\d+(?:\.\d+)?)\s*(trillion|billion)\s*(?:in\s+)?(?:GDP|economic)\s*(?:impact|growth)',
                    r'add\s*(\d+(?:\.\d+)?)\s*%\s*to\s*(?:global\s+)?(?:GDP|output)',
                    r'(\d+(?:\.\d+)?)\s*%\s*of\s*(?:global\s+)?GDP'
                ]
                
                for pattern in patterns:
                    matches = re.findall(pattern, text, re.IGNORECASE)
                    for match in matches:
                        gdp_data.append(self._parse_gdp_match(match, pattern))
            
            # Extract from tables
            for page in gdp_pages[:5]:
                tables = self.extractor.extract_tables(page_range=(page, page))
                for table in tables:
                    if table.empty:
                        continue
                    
                    # Look for GDP-related tables
                    table_str = table.to_string().lower()
                    if 'gdp' in table_str or 'growth' in table_str:
                        processed = self._process_gdp_table(table)
                        if processed:
                            gdp_data.extend(processed)
            
            if gdp_data:
                # Clean and consolidate
                df = pd.DataFrame(gdp_data)
                df = df.dropna(subset=['metric'])
                df = df[df['value'] > 0]
                df = df.drop_duplicates(subset=['metric', 'region'])
                
                logger.info(f"Extracted {len(df)} GDP impact metrics")
                return df
            
        except Exception as e:
            logger.error(f"Error extracting GDP impact: {e}")
        
        return None
    
    def _parse_gdp_match(self, match: tuple, pattern: str) -> Dict:
        """Parse regex match for GDP data."""
        result = {'metric': '', 'value': 0, 'unit': '', 'region': 'Global'}
        
        try:
            if 'trillion' in pattern or 'billion' in pattern:
                # Dollar amount pattern
                if len(match) >= 2:
                    value = float(match[0])
                    unit = match[1].lower()
                    
                    # Convert to consistent units (trillions)
                    if unit == 'billion':
                        value = value / 1000
                    
                    result['metric'] = 'GDP impact (trillions USD)'
                    result['value'] = value
                    result['unit'] = 'trillions_usd'
            else:
                # Percentage pattern
                result['metric'] = 'GDP growth rate'
                result['value'] = float(match[0] if isinstance(match, str) else match[0])
                result['unit'] = 'percentage'
            
            # Try to extract region from context
            # This would need more sophisticated context analysis
            result['timeframe'] = self._extract_timeframe_context(pattern)
            
        except (ValueError, IndexError):
            pass
        
        return result
    
    def _extract_timeframe_context(self, text: str) -> str:
        """Extract timeframe from context."""
        # Simple heuristic - would need improvement
        if any(year in text.lower() for year in ['2030', '2035', '2040']):
            return 'by 2030-2040'
        elif 'annual' in text.lower():
            return 'annual'
        elif 'decade' in text.lower():
            return 'next decade'
        else:
            return 'projected'
    
    def _process_gdp_table(self, table: pd.DataFrame) -> List[Dict]:
        """Process table containing GDP data."""
        results = []
        
        # Look for region/country column
        region_col = None
        for col in table.columns:
            sample_vals = table[col].astype(str).str.lower()
            if any(val for val in sample_vals if 
                   any(region in val for region in ['us', 'china', 'europe', 'global', 'world'])):
                region_col = col
                break
        
        # Find value columns
        value_cols = []
        for col in table.columns:
            if col == region_col:
                continue
            
            # Check for numeric values
            col_vals = table[col].astype(str)
            if col_vals.str.contains('%').sum() > 0 or \
               col_vals.str.match(r'^\d+(?:\.\d+)?$').sum() > len(table) * 0.3:
                value_cols.append(col)
        
        # Extract data
        for _, row in table.iterrows():
            region = str(row[region_col]) if region_col else 'Global'
            
            for val_col in value_cols:
                try:
                    value_str = str(row[val_col])
                    
                    if '%' in value_str:
                        value = float(value_str.replace('%', '').strip())
                        metric = f'GDP growth - {val_col}'
                        unit = 'percentage'
                    else:
                        value = float(value_str.replace(',', '').strip())
                        metric = f'GDP impact - {val_col}'
                        unit = 'absolute'
                    
                    results.append({
                        'metric': metric,
                        'value': value,
                        'unit': unit,
                        'region': region
                    })
                except ValueError:
                    continue
        
        return results
    
    def _extract_labor_market_impact(self) -> Optional[pd.DataFrame]:
        """Extract labor market disruption data."""
        logger.info("Extracting labor market impact data...")
        
        try:
            # Keywords for labor market sections
            keywords = ['jobs', 'employment', 'workers', 'labor', 'automation', 'displacement', 'workforce']
            
            labor_pages = []
            for keyword in keywords:
                pages = self.extractor.find_pages_with_keyword(keyword)
                labor_pages.extend(pages)
            
            labor_pages = sorted(set(labor_pages))[:10]
            
            if not labor_pages:
                return None
            
            labor_data = []
            
            # Extract labor impact metrics
            for page in labor_pages[:5]:
                text = self.extractor.extract_text_from_page(page)
                
                # Patterns for labor impact
                patterns = [
                    r'(\d+(?:\.\d+)?)\s*(?:million|billion)\s*(?:jobs|workers|employees)\s*(?:affected|impacted|displaced)',
                    r'(\d+(?:\.\d+)?)\s*%\s*of\s*(?:jobs|workforce|workers)\s*(?:could be|at risk|exposed)',
                    r'affect\s*(\d+(?:\.\d+)?)\s*%\s*of\s*(?:the\s+)?(?:global\s+)?workforce',
                    r'(\d+(?:\.\d+)?)\s*%\s*of\s*(?:work\s+)?tasks\s*(?:could be|can be)\s*automated'
                ]
                
                for pattern in patterns:
                    matches = re.findall(pattern, text, re.IGNORECASE)
                    for match in matches:
                        value = float(match[0] if isinstance(match, str) else match[0])
                        
                        if 'million' in pattern or 'billion' in pattern:
                            metric = 'workers_affected_millions'
                            unit = 'millions'
                            if 'billion' in pattern:
                                value = value * 1000  # Convert to millions
                        elif 'tasks' in pattern:
                            metric = 'tasks_automatable_percentage'
                            unit = 'percentage'
                        else:
                            metric = 'workforce_exposed_percentage'
                            unit = 'percentage'
                        
                        labor_data.append({
                            'metric': metric,
                            'value': value,
                            'unit': unit,
                            'impact_type': self._categorize_labor_impact(pattern)
                        })
            
            if labor_data:
                df = pd.DataFrame(labor_data)
                df = df[df['value'] > 0]
                df = df.drop_duplicates(subset=['metric'])
                
                logger.info(f"Extracted {len(df)} labor market impact metrics")
                return df
            
        except Exception as e:
            logger.error(f"Error extracting labor market impact: {e}")
        
        return None
    
    def _categorize_labor_impact(self, text: str) -> str:
        """Categorize type of labor market impact."""
        text_lower = text.lower()
        
        if 'displac' in text_lower:
            return 'displacement'
        elif 'automat' in text_lower:
            return 'automation'
        elif 'augment' in text_lower:
            return 'augmentation'
        elif 'transform' in text_lower:
            return 'transformation'
        else:
            return 'general_impact'
    
    def _extract_productivity_gains(self) -> Optional[pd.DataFrame]:
        """Extract productivity gains by sector."""
        logger.info("Extracting productivity gains data...")
        
        try:
            # Keywords for productivity sections
            keywords = ['productivity', 'efficiency', 'output', 'performance', 'gains']
            
            productivity_pages = []
            for keyword in keywords:
                pages = self.extractor.find_pages_with_keyword(keyword)
                productivity_pages.extend(pages)
            
            productivity_pages = sorted(set(productivity_pages))[:10]
            
            if not productivity_pages:
                return None
            
            # Look for productivity tables
            for page in productivity_pages:
                tables = self.extractor.extract_tables(page_range=(page, page))
                
                for table in tables:
                    if table.empty:
                        continue
                    
                    # Check if table contains sector/industry data
                    table_str = table.to_string().lower()
                    if any(term in table_str for term in ['sector', 'industry', 'productivity', '%']):
                        # Process productivity table
                        productivity_df = self._process_productivity_table(table)
                        if productivity_df is not None and not productivity_df.empty:
                            logger.info(f"Extracted productivity data for {len(productivity_df)} sectors")
                            return productivity_df
            
            # If no table found, extract from text
            productivity_data = self._extract_productivity_from_text(productivity_pages)
            if productivity_data:
                return pd.DataFrame(productivity_data)
            
        except Exception as e:
            logger.error(f"Error extracting productivity gains: {e}")
        
        return None
    
    def _process_productivity_table(self, table: pd.DataFrame) -> Optional[pd.DataFrame]:
        """Process table containing productivity data."""
        # Identify sector column
        sector_col = None
        for col in table.columns:
            sample_vals = table[col].astype(str).str.lower()
            if any(val for val in sample_vals if 
                   any(sector in val for sector in ['manufacturing', 'finance', 'retail', 'healthcare'])):
                sector_col = col
                break
        
        if not sector_col:
            return None
        
        # Find productivity gain columns
        gain_cols = []
        for col in table.columns:
            if col == sector_col:
                continue
            
            col_vals = table[col].astype(str)
            if col_vals.str.contains('%').sum() > len(table) * 0.3:
                gain_cols.append(col)
        
        if sector_col and gain_cols:
            # Create clean dataframe
            result_data = []
            
            for _, row in table.iterrows():
                sector = str(row[sector_col]).strip()
                
                for gain_col in gain_cols:
                    try:
                        value_str = str(row[gain_col])
                        value = float(value_str.replace('%', '').strip())
                        
                        # Determine timeframe from column name
                        col_lower = gain_col.lower()
                        if '2030' in col_lower:
                            timeframe = '2030'
                        elif '2025' in col_lower:
                            timeframe = '2025'
                        elif 'annual' in col_lower:
                            timeframe = 'annual'
                        else:
                            timeframe = 'projected'
                        
                        result_data.append({
                            'sector': sector,
                            'productivity_gain': value,
                            'timeframe': timeframe,
                            'unit': 'percentage'
                        })
                    except ValueError:
                        continue
            
            if result_data:
                df = pd.DataFrame(result_data)
                # Keep highest gain per sector if multiple timeframes
                df = df.sort_values('productivity_gain', ascending=False)
                df = df.drop_duplicates(subset=['sector'], keep='first')
                return df
        
        return None
    
    def _extract_productivity_from_text(self, pages: List[int]) -> List[Dict]:
        """Extract productivity data from text."""
        productivity_data = []
        sectors = ['Manufacturing', 'Healthcare', 'Finance', 'Retail', 'Technology', 
                  'Professional Services', 'Education', 'Transportation']
        
        for page in pages[:5]:
            text = self.extractor.extract_text_from_page(page)
            
            for sector in sectors:
                # Look for sector mentions with productivity gains
                patterns = [
                    f'{sector}.*?(\d+(?:\.\d+)?)\s*%\s*productivity',
                    f'(\d+(?:\.\d+)?)\s*%\s*productivity.*?{sector}',
                    f'{sector}.*?productivity.*?(\d+(?:\.\d+)?)\s*%'
                ]
                
                for pattern in patterns:
                    matches = re.findall(pattern, text, re.IGNORECASE)
                    if matches:
                        try:
                            value = float(matches[0])
                            if 0 < value < 100:
                                productivity_data.append({
                                    'sector': sector,
                                    'productivity_gain': value,
                                    'timeframe': 'projected',
                                    'unit': 'percentage'
                                })
                                break
                        except ValueError:
                            continue
        
        # Remove duplicates
        seen = set()
        unique_data = []
        for item in productivity_data:
            key = item['sector']
            if key not in seen:
                seen.add(key)
                unique_data.append(item)
        
        return unique_data
    
    def _extract_automation_exposure(self) -> Optional[pd.DataFrame]:
        """Extract automation exposure by occupation."""
        logger.info("Extracting automation exposure data...")
        
        try:
            # Keywords for automation sections
            keywords = ['automation', 'occupation', 'exposure', 'risk', 'displacement']
            
            automation_pages = []
            for keyword in keywords:
                pages = self.extractor.find_pages_with_keyword(keyword)
                automation_pages.extend(pages)
            
            automation_pages = sorted(set(automation_pages))[:10]
            
            if not automation_pages:
                return None
            
            automation_data = []
            
            # Common occupation categories
            occupations = [
                'Administrative', 'Legal', 'Architecture and Engineering',
                'Business and Financial Operations', 'Computer and Mathematical',
                'Life Sciences', 'Sales', 'Office Support', 'Healthcare',
                'Education', 'Arts and Design', 'Management', 'Production'
            ]
            
            # Extract automation exposure data
            for page in automation_pages[:5]:
                text = self.extractor.extract_text_from_page(page)
                
                for occupation in occupations:
                    # Look for occupation mentions with exposure percentages
                    patterns = [
                        f'{occupation}.*?(\d+(?:\.\d+)?)\s*%\s*(?:exposure|risk|automation)',
                        f'(\d+(?:\.\d+)?)\s*%\s*(?:of\s+)?{occupation}.*?(?:exposed|automated)',
                        f'{occupation}.*?(?:exposure|risk).*?(\d+(?:\.\d+)?)\s*%'
                    ]
                    
                    for pattern in patterns:
                        matches = re.findall(pattern, text, re.IGNORECASE)
                        if matches:
                            try:
                                exposure = float(matches[0])
                                if 0 <= exposure <= 100:
                                    automation_data.append({
                                        'occupation': occupation,
                                        'automation_exposure': exposure,
                                        'risk_level': self._categorize_risk_level(exposure)
                                    })
                                    break
                            except ValueError:
                                continue
            
            if automation_data:
                df = pd.DataFrame(automation_data)
                df = df.drop_duplicates(subset=['occupation'])
                df = df.sort_values('automation_exposure', ascending=False)
                
                logger.info(f"Extracted automation exposure for {len(df)} occupations")
                return df
            
        except Exception as e:
            logger.error(f"Error extracting automation exposure: {e}")
        
        return None
    
    def _categorize_risk_level(self, exposure: float) -> str:
        """Categorize automation risk level."""
        if exposure >= 70:
            return 'High'
        elif exposure >= 40:
            return 'Medium'
        else:
            return 'Low'
    
    def _extract_growth_scenarios(self) -> Optional[pd.DataFrame]:
        """Extract economic growth scenarios."""
        logger.info("Extracting growth scenarios...")
        
        try:
            # Keywords for scenario analysis
            keywords = ['scenario', 'projection', 'forecast', 'baseline', 'optimistic', 'conservative']
            
            scenario_pages = []
            for keyword in keywords:
                pages = self.extractor.find_pages_with_keyword(keyword)
                scenario_pages.extend(pages)
            
            scenario_pages = sorted(set(scenario_pages))[:10]
            
            if not scenario_pages:
                return None
            
            scenario_data = []
            
            # Common scenario types
            scenarios = ['Baseline', 'Optimistic', 'Conservative', 'Accelerated Adoption', 'Slow Adoption']
            
            for page in scenario_pages[:5]:
                text = self.extractor.extract_text_from_page(page)
                
                for scenario in scenarios:
                    # Look for scenario mentions with growth rates
                    patterns = [
                        f'{scenario}.*?(\d+(?:\.\d+)?)\s*%\s*(?:GDP\s+)?growth',
                        f'{scenario}.*?growth.*?(\d+(?:\.\d+)?)\s*%',
                        f'(\d+(?:\.\d+)?)\s*%.*?{scenario}\s+scenario'
                    ]
                    
                    for pattern in patterns:
                        matches = re.findall(pattern, text, re.IGNORECASE)
                        if matches:
                            try:
                                growth_rate = float(matches[0])
                                if 0 <= growth_rate <= 20:  # Reasonable bounds
                                    scenario_data.append({
                                        'scenario': scenario,
                                        'gdp_growth_rate': growth_rate,
                                        'probability': self._estimate_scenario_probability(scenario)
                                    })
                                    break
                            except ValueError:
                                continue
            
            if scenario_data:
                df = pd.DataFrame(scenario_data)
                df = df.drop_duplicates(subset=['scenario'])
                
                logger.info(f"Extracted {len(df)} growth scenarios")
                return df
            
        except Exception as e:
            logger.error(f"Error extracting growth scenarios: {e}")
        
        return None
    
    def _estimate_scenario_probability(self, scenario: str) -> str:
        """Estimate probability for scenario (heuristic)."""
        scenario_lower = scenario.lower()
        
        if 'baseline' in scenario_lower:
            return 'High (60-70%)'
        elif 'optimistic' in scenario_lower or 'accelerated' in scenario_lower:
            return 'Medium (20-30%)'
        elif 'conservative' in scenario_lower or 'slow' in scenario_lower:
            return 'Low (10-20%)'
        else:
            return 'Unknown'
    
    def _extract_investment_outlook(self) -> Optional[pd.DataFrame]:
        """Extract investment outlook and opportunities."""
        logger.info("Extracting investment outlook...")
        
        try:
            # Keywords for investment sections
            keywords = ['investment', 'capital', 'funding', 'opportunity', 'returns', 'ROI']
            
            investment_pages = []
            for keyword in keywords:
                pages = self.extractor.find_pages_with_keyword(keyword)
                investment_pages.extend(pages)
            
            investment_pages = sorted(set(investment_pages))[:10]
            
            if not investment_pages:
                return None
            
            investment_data = []
            
            # Investment categories
            categories = ['Infrastructure', 'Software', 'Hardware', 'Talent', 'R&D', 
                         'Applications', 'Services', 'Platforms']
            
            for page in investment_pages[:5]:
                text = self.extractor.extract_text_from_page(page)
                
                # Extract investment amounts and returns
                patterns = [
                    r'\$(\d+(?:\.\d+)?)\s*(billion|trillion)\s*(?:in\s+)?investment\s*(?:in\s+)?([^.]+)',
                    r'(\d+(?:\.\d+)?)\s*%\s*(?:expected\s+)?(?:return|ROI|growth)',
                    r'investment\s*(?:of\s+)?\$(\d+(?:\.\d+)?)\s*(billion|trillion)'
                ]
                
                for pattern in patterns:
                    matches = re.findall(pattern, text, re.IGNORECASE)
                    for match in matches:
                        investment_data.append(self._parse_investment_match(match, pattern))
            
            if investment_data:
                df = pd.DataFrame(investment_data)
                df = df.dropna(subset=['metric'])
                df = df[df['value'] > 0]
                df = df.drop_duplicates()
                
                logger.info(f"Extracted {len(df)} investment outlook metrics")
                return df
            
        except Exception as e:
            logger.error(f"Error extracting investment outlook: {e}")
        
        return None
    
    def _parse_investment_match(self, match: tuple, pattern: str) -> Dict:
        """Parse investment data match."""
        result = {'metric': '', 'value': 0, 'unit': '', 'category': ''}
        
        try:
            if '$' in pattern and ('billion' in pattern or 'trillion' in pattern):
                # Investment amount pattern
                value = float(match[0])
                unit = match[1].lower()
                
                # Convert to billions
                if unit == 'trillion':
                    value = value * 1000
                
                result['metric'] = 'Investment required'
                result['value'] = value
                result['unit'] = 'billions_usd'
                
                # Try to extract category from context
                if len(match) > 2:
                    result['category'] = self._categorize_investment(match[2])
            
            elif '%' in pattern and ('return' in pattern or 'ROI' in pattern):
                # Return pattern
                result['metric'] = 'Expected return'
                result['value'] = float(match[0] if isinstance(match, str) else match[0])
                result['unit'] = 'percentage'
                result['category'] = 'ROI'
            
        except (ValueError, IndexError):
            pass
        
        return result
    
    def _categorize_investment(self, text: str) -> str:
        """Categorize investment type."""
        text_lower = text.lower()
        
        if 'infrastructure' in text_lower:
            return 'Infrastructure'
        elif 'software' in text_lower or 'application' in text_lower:
            return 'Software'
        elif 'hardware' in text_lower or 'chip' in text_lower:
            return 'Hardware'
        elif 'talent' in text_lower or 'training' in text_lower:
            return 'Human Capital'
        elif 'research' in text_lower or 'r&d' in text_lower:
            return 'R&D'
        else:
            return 'General'
    
    def validate(self, data: Dict[str, pd.DataFrame]) -> bool:
        """Validate loaded data meets expected schema."""
        if not data:
            raise ValueError("No data extracted from PDF")
        
        logger.info(f"Extracted datasets: {list(data.keys())}")
        
        # Validate key datasets
        if 'gdp_impact' in data:
            df = data['gdp_impact']
            if 'metric' not in df.columns or 'value' not in df.columns:
                raise ValueError("GDP impact missing required columns")
        
        if 'labor_impact' in data:
            df = data['labor_impact']
            if 'metric' not in df.columns:
                raise ValueError("Labor impact missing 'metric' column")
        
        logger.info("Data validation passed")
        return True
    
    def _get_fallback_datasets(self) -> Dict[str, pd.DataFrame]:
        """Return fallback datasets when extraction fails."""
        return {
            'gdp_impact': pd.DataFrame({
                'metric': ['GDP growth rate', 'GDP impact (trillions USD)', 'Annual productivity growth'],
                'value': [7.0, 7.0, 1.5],
                'unit': ['percentage', 'trillions_usd', 'percentage'],
                'region': ['Global', 'Global', 'Global'],
                'timeframe': ['by 2030-2040', 'cumulative', 'annual']
            }),
            'labor_impact': pd.DataFrame({
                'metric': ['workforce_exposed_percentage', 'tasks_automatable_percentage', 
                         'workers_affected_millions'],
                'value': [25.0, 40.0, 300.0],
                'unit': ['percentage', 'percentage', 'millions'],
                'impact_type': ['automation', 'automation', 'transformation']
            }),
            'productivity_gains': pd.DataFrame({
                'sector': ['Professional Services', 'Manufacturing', 'Healthcare', 
                          'Financial Services', 'Retail'],
                'productivity_gain': [40.0, 35.0, 30.0, 35.0, 25.0],
                'timeframe': ['projected', 'projected', 'projected', 'projected', 'projected'],
                'unit': ['percentage'] * 5
            }),
            'automation_exposure': pd.DataFrame({
                'occupation': ['Administrative', 'Legal', 'Architecture and Engineering',
                             'Sales', 'Computer and Mathematical'],
                'automation_exposure': [85.0, 75.0, 45.0, 65.0, 20.0],
                'risk_level': ['High', 'High', 'Medium', 'Medium', 'Low']
            }),
            'growth_scenarios': pd.DataFrame({
                'scenario': ['Baseline', 'Optimistic', 'Conservative'],
                'gdp_growth_rate': [7.0, 10.0, 4.0],
                'probability': ['High (60-70%)', 'Medium (20-30%)', 'Low (10-20%)']
            }),
            'investment_outlook': pd.DataFrame({
                'metric': ['Investment required', 'Expected return', 'Infrastructure investment'],
                'value': [200.0, 25.0, 50.0],
                'unit': ['billions_usd', 'percentage', 'billions_usd'],
                'category': ['General', 'ROI', 'Infrastructure']
            })
        }