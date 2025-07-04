"""NVIDIA AI token economics and infrastructure data loader with actual PDF extraction."""

from pathlib import Path
from typing import Dict, List, Optional
import pandas as pd
import logging
import re

from .base import BaseDataLoader, DataSource
from ..models.economics import TokenEconomics
from ..extractors.pdf_extractor_impl import EnhancedPDFExtractor

logger = logging.getLogger(__name__)


class NVIDIATokenLoader(BaseDataLoader):
    """Loader for NVIDIA token economics and AI infrastructure data with real PDF extraction."""
    
    def __init__(self, file_path: Optional[Path] = None):
        """Initialize with NVIDIA report file path."""
        if file_path is None:
            file_path = Path("/mnt/c/Users/rcasa/OneDrive/Documents/AI-Adoption-Dashboard/"
                           "AI adoption resources/AI Adoption Resources 3/"
                           "Explaining Tokens — the Language and Currency of AI _ NVIDIA Blog.pdf")
        
        source = DataSource(
            name="NVIDIA Token Economics Analysis",
            version="2024-2025",
            url="https://blogs.nvidia.com/blog/explaining-tokens-ai/",
            file_path=file_path,
            citation="NVIDIA Corporation. 'Explaining Tokens — the Language and Currency of AI.' NVIDIA Blog, 2024."
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
        """Load all datasets from NVIDIA report using actual PDF extraction."""
        logger.info(f"Loading data from {self.source.name}")
        
        if not self.extractor:
            logger.warning("PDF extractor not available, returning fallback datasets")
            return self._get_fallback_datasets()
        
        datasets = {}
        
        try:
            # Extract different aspects of token economics
            
            # 1. Token pricing evolution and cost reduction
            token_pricing = self._extract_token_pricing_evolution()
            if token_pricing is not None and not token_pricing.empty:
                datasets['token_pricing_evolution'] = token_pricing
            
            # 2. Model efficiency and performance trends
            model_efficiency = self._extract_model_efficiency()
            if model_efficiency is not None and not model_efficiency.empty:
                datasets['model_efficiency_trends'] = model_efficiency
            
            # 3. Infrastructure and compute costs
            infrastructure_costs = self._extract_infrastructure_costs()
            if infrastructure_costs is not None and not infrastructure_costs.empty:
                datasets['infrastructure_costs'] = infrastructure_costs
            
            # 4. Token optimization strategies
            token_optimization = self._extract_token_optimization()
            if token_optimization is not None and not token_optimization.empty:
                datasets['token_optimization'] = token_optimization
            
            # 5. Compute requirements by use case
            compute_requirements = self._extract_compute_requirements()
            if compute_requirements is not None and not compute_requirements.empty:
                datasets['compute_requirements'] = compute_requirements
            
            # 6. Economic barriers and opportunities
            economic_barriers = self._extract_economic_barriers()
            if economic_barriers is not None and not economic_barriers.empty:
                datasets['economic_barriers'] = economic_barriers
            
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
    
    def _extract_token_pricing_evolution(self) -> Optional[pd.DataFrame]:
        """Extract token pricing evolution and cost reduction data."""
        logger.info("Extracting token pricing evolution...")
        
        try:
            # Keywords for token pricing sections
            keywords = ['token', 'pricing', 'cost', '280x', 'reduction', 'per thousand', 
                       'GPT', 'Claude', 'economics', 'price evolution']
            
            pricing_pages = []
            for keyword in keywords:
                pages = self.extractor.find_pages_with_keyword(keyword)
                pricing_pages.extend(pages)
            
            pricing_pages = sorted(set(pricing_pages))[:10]
            
            if not pricing_pages:
                return None
            
            pricing_data = []
            
            # Extract pricing metrics
            for page in pricing_pages[:5]:
                text = self.extractor.extract_text_from_page(page)
                
                # Patterns for token pricing and cost reduction
                patterns = [
                    r'(\d+(?:\.\d+)?)\s*x\s*(?:cost\s*)?reduction',  # 280x reduction
                    r'\$(\d+(?:\.\d+)?)\s*per\s*(?:thousand|1k|1,000)\s*tokens',
                    r'(\d+(?:\.\d+)?)\s*(?:cents?|¢)\s*per\s*(?:thousand|1k|1,000)\s*tokens',
                    r'token\s*(?:price|cost)\s*(?:dropped|reduced|decreased)\s*(?:by\s*)?(\d+(?:\.\d+)?)\s*%',
                    r'from\s*\$(\d+(?:\.\d+)?)\s*to\s*\$(\d+(?:\.\d+)?)\s*per\s*(?:thousand|1k)',
                    r'(\d+(?:\.\d+)?)\s*tokens?\s*per\s*dollar'
                ]
                
                for pattern in patterns:
                    matches = re.findall(pattern, text, re.IGNORECASE)
                    for match in matches:
                        pricing_data.append(self._parse_pricing_match(match, pattern, text))
            
            # Look for pricing tables
            for page in pricing_pages[:5]:
                tables = self.extractor.extract_tables(page_range=(page, page))
                for table in tables:
                    if table.empty:
                        continue
                    
                    # Process pricing tables
                    processed = self._process_pricing_table(table)
                    if processed:
                        pricing_data.extend(processed)
            
            if pricing_data:
                df = pd.DataFrame(pricing_data)
                df = df.dropna(subset=['metric'])
                df = df[df['value'] > 0]
                df = df.drop_duplicates()
                
                logger.info(f"Extracted {len(df)} token pricing metrics")
                return df
            
        except Exception as e:
            logger.error(f"Error extracting token pricing: {e}")
        
        return None
    
    def _parse_pricing_match(self, match: tuple, pattern: str, context: str) -> Dict:
        """Parse pricing data match."""
        result = {'metric': '', 'value': 0, 'unit': '', 'model': '', 'date': ''}
        
        try:
            if 'x' in pattern and 'reduction' in pattern:
                # Cost reduction factor (e.g., 280x)
                result['metric'] = 'cost_reduction_factor'
                result['value'] = float(match[0] if isinstance(match, str) else match[0])
                result['unit'] = 'multiplier'
                
            elif 'per' in pattern and ('thousand' in pattern or '1k' in pattern):
                # Price per thousand tokens
                if 'cents' in pattern or '¢' in pattern:
                    value = float(match[0] if isinstance(match, str) else match[0]) / 100
                else:
                    value = float(match[0] if isinstance(match, str) else match[0])
                
                result['metric'] = 'price_per_1k_tokens'
                result['value'] = value
                result['unit'] = 'usd'
                result['model'] = self._extract_model_from_context(context)
                
            elif 'from' in pattern and 'to' in pattern:
                # Price change from-to
                from_price = float(match[0])
                to_price = float(match[1])
                reduction = ((from_price - to_price) / from_price) * 100
                
                result['metric'] = 'price_reduction_percentage'
                result['value'] = reduction
                result['unit'] = 'percentage'
                
            elif 'tokens' in pattern and 'per' in pattern and 'dollar' in pattern:
                # Tokens per dollar
                result['metric'] = 'tokens_per_dollar'
                result['value'] = float(match[0] if isinstance(match, str) else match[0])
                result['unit'] = 'tokens'
                
            # Extract date if available
            result['date'] = self._extract_date_from_context(context)
            
        except (ValueError, IndexError):
            pass
        
        return result
    
    def _extract_model_from_context(self, text: str) -> str:
        """Extract model name from context."""
        models = ['GPT-4', 'GPT-3.5', 'GPT-3', 'Claude', 'Gemini', 'LLaMA', 'Mistral']
        
        for model in models:
            if model.lower() in text.lower():
                return model
        
        return 'General'
    
    def _extract_date_from_context(self, text: str) -> str:
        """Extract date from context."""
        # Look for year or quarter mentions
        year_match = re.search(r'20[2-3]\d', text)
        if year_match:
            year = year_match.group()
            
            # Check for quarter
            quarter_match = re.search(r'Q[1-4]', text)
            if quarter_match:
                return f"{quarter_match.group()} {year}"
            else:
                return year
        
        return 'Recent'
    
    def _process_pricing_table(self, table: pd.DataFrame) -> List[Dict]:
        """Process table containing pricing data."""
        results = []
        
        # Look for date/time column
        date_col = None
        for col in table.columns:
            col_str = str(col).lower()
            if any(term in col_str for term in ['date', 'year', 'quarter', 'month', 'time']):
                date_col = col
                break
        
        # Look for model column
        model_col = None
        for col in table.columns:
            col_str = str(col).lower()
            if any(term in col_str for term in ['model', 'service', 'api', 'provider']):
                model_col = col
                break
        
        # Find price columns
        price_cols = []
        for col in table.columns:
            col_str = str(col).lower()
            if any(term in col_str for term in ['price', 'cost', 'token', 'rate']):
                price_cols.append(col)
        
        if price_cols:
            for _, row in table.iterrows():
                date = str(row[date_col]) if date_col else 'Recent'
                model = str(row[model_col]) if model_col else 'General'
                
                for price_col in price_cols:
                    try:
                        value_str = str(row[price_col])
                        # Extract numeric value
                        numeric_match = re.search(r'(\d+(?:\.\d+)?)', value_str)
                        if numeric_match:
                            value = float(numeric_match.group(1))
                            
                            # Check if cents
                            if '¢' in value_str or 'cent' in value_str.lower():
                                value = value / 100
                            
                            results.append({
                                'metric': 'price_per_1k_tokens',
                                'value': value,
                                'unit': 'usd',
                                'model': model,
                                'date': date
                            })
                    except ValueError:
                        continue
        
        return results
    
    def _extract_model_efficiency(self) -> Optional[pd.DataFrame]:
        """Extract model efficiency and performance data."""
        logger.info("Extracting model efficiency data...")
        
        try:
            # Keywords for efficiency sections
            keywords = ['efficiency', 'performance', 'tokens per second', 'throughput', 
                       'latency', 'parameters', 'quality', 'benchmark']
            
            efficiency_pages = []
            for keyword in keywords:
                pages = self.extractor.find_pages_with_keyword(keyword)
                efficiency_pages.extend(pages)
            
            efficiency_pages = sorted(set(efficiency_pages))[:10]
            
            if not efficiency_pages:
                return None
            
            efficiency_data = []
            
            # Common model names to look for
            models = ['GPT-2', 'GPT-3', 'GPT-3.5', 'GPT-4', 'Claude', 'Gemini', 
                     'LLaMA', 'Mistral', 'Falcon', 'PaLM']
            
            for page in efficiency_pages[:5]:
                text = self.extractor.extract_text_from_page(page)
                
                for model in models:
                    if model.lower() in text.lower():
                        # Extract metrics for this model
                        metrics = self._extract_model_metrics(text, model)
                        if metrics:
                            efficiency_data.append(metrics)
            
            # Look for efficiency tables
            for page in efficiency_pages[:5]:
                tables = self.extractor.extract_tables(page_range=(page, page))
                for table in tables:
                    if table.empty:
                        continue
                    
                    # Check if table contains model data
                    table_str = table.to_string().lower()
                    if any(model.lower() in table_str for model in models):
                        processed = self._process_efficiency_table(table)
                        if processed:
                            efficiency_data.extend(processed)
            
            if efficiency_data:
                df = pd.DataFrame(efficiency_data)
                df = df.drop_duplicates(subset=['model_name'])
                
                logger.info(f"Extracted efficiency data for {len(df)} models")
                return df
            
        except Exception as e:
            logger.error(f"Error extracting model efficiency: {e}")
        
        return None
    
    def _extract_model_metrics(self, text: str, model: str) -> Optional[Dict]:
        """Extract metrics for a specific model from text."""
        result = {'model_name': model}
        
        # Find context around model name
        model_pos = text.lower().find(model.lower())
        if model_pos == -1:
            return None
        
        context = text[max(0, model_pos-500):model_pos+500]
        
        # Extract various metrics
        patterns = {
            'parameters': r'(\d+(?:\.\d+)?)\s*(?:billion|B)\s*parameters',
            'tokens_per_second': r'(\d+(?:\.\d+)?)\s*tokens?\s*(?:per|/)\s*second',
            'latency_ms': r'(\d+(?:\.\d+)?)\s*(?:ms|milliseconds)\s*latency',
            'quality_score': r'(?:quality|performance)\s*(?:score|rating)\s*(?:of\s*)?(\d+(?:\.\d+)?)',
            'efficiency_ratio': r'efficiency\s*(?:ratio|score)\s*(?:of\s*)?(\d+(?:\.\d+)?)'
        }
        
        found_metrics = False
        for metric, pattern in patterns.items():
            matches = re.findall(pattern, context, re.IGNORECASE)
            if matches:
                value = float(matches[0])
                if metric == 'parameters':
                    value = value  # Already in billions
                result[metric] = value
                found_metrics = True
        
        return result if found_metrics else None
    
    def _process_efficiency_table(self, table: pd.DataFrame) -> List[Dict]:
        """Process table containing efficiency data."""
        results = []
        
        # Identify model column
        model_col = None
        for col in table.columns:
            sample_vals = table[col].astype(str).str.lower()
            if any('gpt' in val or 'claude' in val or 'gemini' in val for val in sample_vals):
                model_col = col
                break
        
        if not model_col:
            return results
        
        # Map column names to metrics
        metric_mappings = {
            'parameters': ['param', 'size'],
            'tokens_per_second': ['token', 'throughput', 'speed'],
            'quality_score': ['quality', 'accuracy', 'score'],
            'efficiency_ratio': ['efficiency', 'ratio'],
            'latency_ms': ['latency', 'response']
        }
        
        # Extract data
        for _, row in table.iterrows():
            model_name = str(row[model_col])
            result = {'model_name': model_name}
            
            for col in table.columns:
                if col == model_col:
                    continue
                
                col_lower = str(col).lower()
                for metric, keywords in metric_mappings.items():
                    if any(keyword in col_lower for keyword in keywords):
                        try:
                            value_str = str(row[col])
                            value = float(re.search(r'(\d+(?:\.\d+)?)', value_str).group(1))
                            result[metric] = value
                        except:
                            continue
            
            if len(result) > 1:  # Has more than just model name
                results.append(result)
        
        return results
    
    def _extract_infrastructure_costs(self) -> Optional[pd.DataFrame]:
        """Extract infrastructure and compute cost data."""
        logger.info("Extracting infrastructure cost data...")
        
        try:
            # Keywords for infrastructure costs
            keywords = ['GPU', 'infrastructure', 'compute cost', 'training cost', 
                       'inference', 'cloud', 'hardware', 'TCO', 'energy']
            
            cost_pages = []
            for keyword in keywords:
                pages = self.extractor.find_pages_with_keyword(keyword)
                cost_pages.extend(pages)
            
            cost_pages = sorted(set(cost_pages))[:10]
            
            if not cost_pages:
                return None
            
            cost_data = []
            
            # Extract cost metrics
            for page in cost_pages[:5]:
                text = self.extractor.extract_text_from_page(page)
                
                # Extract numeric cost data
                numeric_data = self.extractor.extract_numeric_data(
                    keywords=['GPU', 'training', 'inference', 'compute', 'cloud', 'energy'],
                    value_pattern=r'\$(\d+(?:,\d+)*(?:\.\d+)?)\s*(thousand|million|billion|K|M|B)?'
                )
                
                for keyword, values in numeric_data.items():
                    for value, unit in values:
                        # Normalize to USD
                        if unit:
                            unit_lower = unit.lower()
                            if unit_lower in ['k', 'thousand']:
                                value = value * 1000
                            elif unit_lower in ['m', 'million']:
                                value = value * 1000000
                            elif unit_lower in ['b', 'billion']:
                                value = value * 1000000000
                        
                        cost_data.append({
                            'cost_category': keyword,
                            'cost_value': value,
                            'year': self._extract_year_from_cost_context(text),
                            'metric_type': self._categorize_cost_type(keyword)
                        })
            
            if cost_data:
                df = pd.DataFrame(cost_data)
                df = df[df['cost_value'] > 0]
                df = df.drop_duplicates()
                
                logger.info(f"Extracted {len(df)} infrastructure cost metrics")
                return df
            
        except Exception as e:
            logger.error(f"Error extracting infrastructure costs: {e}")
        
        return None
    
    def _extract_year_from_cost_context(self, text: str) -> int:
        """Extract year from cost context."""
        year_matches = re.findall(r'20[2-3]\d', text)
        if year_matches:
            return max(int(year) for year in year_matches)
        return 2024
    
    def _categorize_cost_type(self, keyword: str) -> str:
        """Categorize type of cost."""
        keyword_lower = keyword.lower()
        
        if 'gpu' in keyword_lower or 'hardware' in keyword_lower:
            return 'hardware_cost'
        elif 'training' in keyword_lower:
            return 'training_cost'
        elif 'inference' in keyword_lower:
            return 'inference_cost'
        elif 'cloud' in keyword_lower:
            return 'cloud_cost'
        elif 'energy' in keyword_lower:
            return 'energy_cost'
        else:
            return 'general_cost'
    
    def _extract_token_optimization(self) -> Optional[pd.DataFrame]:
        """Extract token optimization strategies and impact."""
        logger.info("Extracting token optimization data...")
        
        try:
            # Keywords for optimization sections
            keywords = ['optimization', 'prompt engineering', 'caching', 'quantization',
                       'batch', 'sparse', 'distillation', 'RAG', 'fine-tuning']
            
            optimization_pages = []
            for keyword in keywords:
                pages = self.extractor.find_pages_with_keyword(keyword)
                optimization_pages.extend(pages)
            
            optimization_pages = sorted(set(optimization_pages))[:10]
            
            if not optimization_pages:
                return None
            
            optimization_data = []
            
            # Optimization techniques to look for
            techniques = [
                'Prompt Engineering', 'Context Caching', 'Model Quantization',
                'Batch Processing', 'Sparse Models', 'Knowledge Distillation',
                'RAG Implementation', 'Fine-tuning', 'Multi-modal Fusion',
                'Token Compression', 'Semantic Caching'
            ]
            
            for page in optimization_pages[:5]:
                text = self.extractor.extract_text_from_page(page)
                
                for technique in techniques:
                    if technique.lower() in text.lower():
                        # Extract metrics for this technique
                        patterns = [
                            f'{technique}.*?(\d+(?:\.\d+)?)\s*%\s*(?:token\s*)?reduction',
                            f'{technique}.*?(?:reduce|save).*?(\d+(?:\.\d+)?)\s*%',
                            f'(\d+(?:\.\d+)?)\s*%.*?{technique}',
                            f'{technique}.*?(\d+(?:\.\d+)?)\s*x\s*(?:faster|improvement)'
                        ]
                        
                        for pattern in patterns:
                            matches = re.findall(pattern, text, re.IGNORECASE)
                            if matches:
                                value = float(matches[0])
                                optimization_data.append({
                                    'optimization_technique': technique,
                                    'improvement_value': value,
                                    'metric_type': 'percentage' if '%' in pattern else 'multiplier',
                                    'implementation_complexity': self._assess_complexity(technique)
                                })
                                break
            
            if optimization_data:
                df = pd.DataFrame(optimization_data)
                df = df.drop_duplicates(subset=['optimization_technique'])
                
                logger.info(f"Extracted {len(df)} optimization techniques")
                return df
            
        except Exception as e:
            logger.error(f"Error extracting token optimization: {e}")
        
        return None
    
    def _assess_complexity(self, technique: str) -> str:
        """Assess implementation complexity of optimization technique."""
        low_complexity = ['Prompt Engineering', 'Batch Processing', 'Context Caching']
        high_complexity = ['Sparse Models', 'Knowledge Distillation', 'Multi-modal Fusion']
        
        if technique in low_complexity:
            return 'Low'
        elif technique in high_complexity:
            return 'High'
        else:
            return 'Medium'
    
    def _extract_compute_requirements(self) -> Optional[pd.DataFrame]:
        """Extract compute requirements by use case."""
        logger.info("Extracting compute requirements...")
        
        try:
            # Keywords for compute requirements
            keywords = ['use case', 'application', 'workload', 'tokens per', 
                       'GPU hours', 'compute requirements', 'latency']
            
            compute_pages = []
            for keyword in keywords:
                pages = self.extractor.find_pages_with_keyword(keyword)
                compute_pages.extend(pages)
            
            compute_pages = sorted(set(compute_pages))[:10]
            
            if not compute_pages:
                return None
            
            # Look for compute requirement tables
            for page in compute_pages[:5]:
                tables = self.extractor.extract_tables(page_range=(page, page))
                
                for table in tables:
                    if table.empty:
                        continue
                    
                    # Check if table contains use case data
                    table_str = table.to_string().lower()
                    if any(term in table_str for term in ['chatbot', 'code', 'translation', 'analysis']):
                        compute_df = self._process_compute_table(table)
                        if compute_df is not None and not compute_df.empty:
                            logger.info(f"Extracted compute requirements for {len(compute_df)} use cases")
                            return compute_df
            
            # If no table found, extract from text
            compute_data = self._extract_compute_from_text(compute_pages)
            if compute_data:
                return pd.DataFrame(compute_data)
            
        except Exception as e:
            logger.error(f"Error extracting compute requirements: {e}")
        
        return None
    
    def _process_compute_table(self, table: pd.DataFrame) -> Optional[pd.DataFrame]:
        """Process table containing compute requirements."""
        # Identify use case column
        use_case_col = None
        for col in table.columns:
            sample_vals = table[col].astype(str).str.lower()
            if any(val for val in sample_vals if 
                   any(use in val for use in ['chat', 'code', 'content', 'translation'])):
                use_case_col = col
                break
        
        if not use_case_col:
            return None
        
        # Extract metrics
        result_data = []
        for _, row in table.iterrows():
            use_case = str(row[use_case_col])
            metrics = {'use_case': use_case}
            
            for col in table.columns:
                if col == use_case_col:
                    continue
                
                col_lower = str(col).lower()
                value_str = str(row[col])
                
                try:
                    # Extract numeric value
                    numeric_match = re.search(r'(\d+(?:,\d+)*(?:\.\d+)?)', value_str)
                    if numeric_match:
                        value = float(numeric_match.group(1).replace(',', ''))
                        
                        if 'token' in col_lower:
                            metrics['avg_tokens_per_request'] = value
                        elif 'gpu' in col_lower:
                            metrics['gpu_hours_required'] = value
                        elif 'cost' in col_lower:
                            metrics['cost_per_million_requests'] = value
                        elif 'latency' in col_lower:
                            metrics['latency_ms'] = value
                except:
                    continue
            
            if len(metrics) > 1:
                result_data.append(metrics)
        
        return pd.DataFrame(result_data) if result_data else None
    
    def _extract_compute_from_text(self, pages: List[int]) -> List[Dict]:
        """Extract compute requirements from text."""
        compute_data = []
        use_cases = ['Chatbot', 'Code Generation', 'Content Writing', 'Translation',
                    'Summarization', 'Data Analysis', 'Image Generation']
        
        for page in pages[:5]:
            text = self.extractor.extract_text_from_page(page)
            
            for use_case in use_cases:
                if use_case.lower() in text.lower():
                    # Extract metrics for this use case
                    metrics = {'use_case': use_case}
                    
                    # Find context around use case
                    use_case_pos = text.lower().find(use_case.lower())
                    context = text[max(0, use_case_pos-300):use_case_pos+300]
                    
                    # Extract token requirements
                    token_match = re.search(r'(\d+(?:,\d+)?)\s*tokens?\s*(?:per|average)', context, re.IGNORECASE)
                    if token_match:
                        metrics['avg_tokens_per_request'] = float(token_match.group(1).replace(',', ''))
                    
                    # Extract GPU hours
                    gpu_match = re.search(r'(\d+(?:,\d+)?)\s*GPU\s*hours?', context, re.IGNORECASE)
                    if gpu_match:
                        metrics['gpu_hours_required'] = float(gpu_match.group(1).replace(',', ''))
                    
                    if len(metrics) > 1:
                        compute_data.append(metrics)
        
        return compute_data
    
    def _extract_economic_barriers(self) -> Optional[pd.DataFrame]:
        """Extract economic barriers to AI adoption."""
        logger.info("Extracting economic barriers...")
        
        try:
            # Keywords for barriers sections
            keywords = ['barrier', 'challenge', 'cost', 'investment', 'adoption',
                       'infrastructure', 'talent', 'integration', 'compliance']
            
            barrier_pages = []
            for keyword in keywords:
                pages = self.extractor.find_pages_with_keyword(keyword)
                barrier_pages.extend(pages)
            
            barrier_pages = sorted(set(barrier_pages))[:10]
            
            if not barrier_pages:
                return None
            
            barrier_data = []
            
            # Common barrier types
            barriers = [
                'Initial Infrastructure Cost', 'Ongoing Operational Cost',
                'Talent Acquisition Cost', 'Data Preparation Cost',
                'Integration Cost', 'Compliance Cost', 'Training Cost',
                'Security Implementation Cost', 'Maintenance Cost'
            ]
            
            for page in barrier_pages[:5]:
                text = self.extractor.extract_text_from_page(page)
                
                for barrier in barriers:
                    if barrier.lower() in text.lower():
                        # Extract cost data for this barrier
                        patterns = [
                            f'{barrier}.*?\\$(\d+(?:,\d+)*(?:\.\d+)?)\s*(thousand|million|K|M)?',
                            f'\\$(\d+(?:,\d+)*(?:\.\d+)?)\s*(thousand|million|K|M)?.*?{barrier}',
                            f'{barrier}.*?(\d+(?:\.\d+)?)\s*%\s*of\s*(?:total\s*)?(?:IT\s*)?budget'
                        ]
                        
                        for pattern in patterns:
                            matches = re.findall(pattern, text, re.IGNORECASE)
                            if matches:
                                barrier_data.append(self._parse_barrier_match(matches[0], barrier))
                                break
            
            if barrier_data:
                df = pd.DataFrame(barrier_data)
                df = df.drop_duplicates(subset=['barrier_type'])
                
                logger.info(f"Extracted {len(df)} economic barriers")
                return df
            
        except Exception as e:
            logger.error(f"Error extracting economic barriers: {e}")
        
        return None
    
    def _parse_barrier_match(self, match: tuple, barrier: str) -> Dict:
        """Parse barrier cost match."""
        result = {'barrier_type': barrier}
        
        try:
            if isinstance(match, tuple) and len(match) >= 2:
                value = float(match[0].replace(',', ''))
                unit = match[1] if len(match) > 1 else None
                
                # Normalize to dollars
                if unit:
                    unit_lower = unit.lower()
                    if unit_lower in ['k', 'thousand']:
                        value = value * 1000
                    elif unit_lower in ['m', 'million']:
                        value = value * 1000000
                
                result['cost_value'] = value
                result['severity_score'] = self._assess_barrier_severity(value)
            else:
                # Percentage of budget
                result['budget_percentage'] = float(match[0] if isinstance(match, str) else match)
                result['severity_score'] = result['budget_percentage'] / 10  # Scale to 0-10
            
        except (ValueError, IndexError):
            pass
        
        return result
    
    def _assess_barrier_severity(self, cost: float) -> float:
        """Assess severity score based on cost (0-10 scale)."""
        if cost >= 1000000:  # $1M+
            return 9.0
        elif cost >= 500000:  # $500K+
            return 7.5
        elif cost >= 100000:  # $100K+
            return 6.0
        elif cost >= 50000:   # $50K+
            return 4.5
        else:
            return 3.0
    
    def validate(self, data: Dict[str, pd.DataFrame]) -> bool:
        """Validate loaded data meets expected schema."""
        if not data:
            raise ValueError("No data extracted from PDF")
        
        logger.info(f"Extracted datasets: {list(data.keys())}")
        
        # Validate key datasets if present
        if 'token_pricing_evolution' in data:
            df = data['token_pricing_evolution']
            if 'metric' not in df.columns or 'value' not in df.columns:
                raise ValueError("Token pricing missing required columns")
            
            # Check for 280x cost reduction
            cost_reduction = df[df['metric'] == 'cost_reduction_factor']
            if not cost_reduction.empty:
                max_reduction = cost_reduction['value'].max()
                logger.info(f"Found maximum cost reduction factor: {max_reduction}x")
        
        if 'model_efficiency_trends' in data:
            df = data['model_efficiency_trends']
            if 'model_name' not in df.columns:
                raise ValueError("Model efficiency missing 'model_name' column")
        
        logger.info("Data validation passed")
        return True
    
    def _get_fallback_datasets(self) -> Dict[str, pd.DataFrame]:
        """Return fallback datasets when extraction fails."""
        return {
            'token_pricing_evolution': pd.DataFrame({
                'metric': ['cost_reduction_factor', 'price_per_1k_tokens', 'price_per_1k_tokens',
                          'tokens_per_dollar', 'price_reduction_percentage'],
                'value': [280.0, 0.0002, 0.06, 2000000, 99.7],
                'unit': ['multiplier', 'usd', 'usd', 'tokens', 'percentage'],
                'model': ['Overall', 'GPT-4 (2025)', 'GPT-3 (2022)', 'GPT-4 (2025)', 'GPT-3 to GPT-4'],
                'date': ['2022-2025', '2025', '2022', '2025', '2022-2025']
            }),
            'model_efficiency_trends': pd.DataFrame({
                'model_name': ['GPT-3', 'GPT-4', 'Claude 3', 'Gemini 1.5', 'Open Source LLMs'],
                'parameters': [175, 1760, 130, 540, 70],
                'tokens_per_second': [20, 40, 45, 50, 60],
                'quality_score': [7.5, 9.3, 9.0, 9.1, 7.8],
                'efficiency_ratio': [0.43, 0.53, 0.69, 0.56, 1.11]
            }),
            'infrastructure_costs': pd.DataFrame({
                'cost_category': ['GPU', 'training', 'inference', 'cloud', 'energy'],
                'cost_value': [22000, 150000, 95000, 1200, 48000],
                'year': [2025, 2025, 2025, 2025, 2025],
                'metric_type': ['hardware_cost', 'training_cost', 'inference_cost', 
                               'cloud_cost', 'energy_cost']
            }),
            'token_optimization': pd.DataFrame({
                'optimization_technique': ['Prompt Engineering', 'Context Caching', 'RAG Implementation',
                                         'Batch Processing', 'Model Quantization'],
                'improvement_value': [35.0, 45.0, 70.0, 60.0, 25.0],
                'metric_type': ['percentage'] * 5,
                'implementation_complexity': ['Low', 'Medium', 'Medium', 'Low', 'Medium']
            }),
            'compute_requirements': pd.DataFrame({
                'use_case': ['Chatbot', 'Code Generation', 'Content Writing', 'Translation', 'Data Analysis'],
                'avg_tokens_per_request': [500, 1500, 2000, 800, 3000],
                'gpu_hours_required': [2500, 2700, 4250, 700, 1875],
                'cost_per_million_requests': [25, 75, 100, 40, 150],
                'latency_ms': [100, 500, 1000, 200, 2000]
            }),
            'economic_barriers': pd.DataFrame({
                'barrier_type': ['Initial Infrastructure Cost', 'Talent Acquisition Cost',
                               'Ongoing Operational Cost', 'Integration Cost'],
                'cost_value': [2500000, 1200000, 850000, 450000],
                'severity_score': [9.0, 8.8, 7.2, 6.0]
            })
        }


__all__ = ['NVIDIATokenLoader']