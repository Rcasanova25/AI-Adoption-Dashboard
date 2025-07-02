"""
Automated PDF Data Ingestion Pipeline
Automatically extracts and integrates data from research PDFs
"""

import os
import re
import json
import logging
import hashlib
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple, Union
import pandas as pd
from datetime import datetime
import PyPDF2
import pdfplumber
import numpy as np
from dataclasses import dataclass
import streamlit as st

from .pdf_extractor import PDFDataExtractor, IntelligentDataMapper
from .automated_research_scanner import AutomatedResearchScanner, ResearchDocument
from .models import validate_dataset, safe_validate_data

logger = logging.getLogger(__name__)


class PDFTextProcessor:
    """Enhanced PDF text extraction with real PDF parsing capabilities"""
    
    def __init__(self):
        self.extraction_patterns = {
            'percentage': re.compile(r'(\d+(?:\.\d+)?)\s*%'),
            'currency': re.compile(r'\$\s*(\d+(?:,\d{3})*(?:\.\d+)?)\s*(billion|million|trillion)?'),
            'year': re.compile(r'\b(19|20)\d{2}\b'),
            'adoption_rate': re.compile(r'adoption\s+(?:rate|reached|at)\s+(\d+(?:\.\d+)?)\s*%', re.IGNORECASE),
            'growth_rate': re.compile(r'(?:grew|increased|rose|gained)\s+(?:by\s+)?(\d+(?:\.\d+)?)\s*%', re.IGNORECASE),
            'sector_data': re.compile(r'(Technology|Financial|Healthcare|Manufacturing|Retail|Education|Energy|Government)\s*[:\-]?\s*(\d+(?:\.\d+)?)\s*%', re.IGNORECASE)
        }
    
    def extract_text_from_pdf(self, filepath: str) -> str:
        """Extract all text from PDF using multiple methods for reliability"""
        text = ""
        
        # Try pdfplumber first (better for tables)
        try:
            with pdfplumber.open(filepath) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
        except Exception as e:
            logger.warning(f"pdfplumber extraction failed: {e}")
        
        # Fallback to PyPDF2 if needed
        if not text.strip():
            try:
                with open(filepath, 'rb') as file:
                    pdf_reader = PyPDF2.PdfReader(file)
                    for page_num in range(len(pdf_reader.pages)):
                        page = pdf_reader.pages[page_num]
                        text += page.extract_text() + "\n"
            except Exception as e:
                logger.error(f"PyPDF2 extraction failed: {e}")
        
        return text
    
    def extract_tables_from_pdf(self, filepath: str) -> List[pd.DataFrame]:
        """Extract tables from PDF"""
        tables = []
        
        try:
            with pdfplumber.open(filepath) as pdf:
                for page in pdf.pages:
                    page_tables = page.extract_tables()
                    for table in page_tables:
                        if table and len(table) > 1:  # Has header and at least one row
                            df = pd.DataFrame(table[1:], columns=table[0])
                            df = df.dropna(how='all')  # Remove empty rows
                            if not df.empty:
                                tables.append(df)
        except Exception as e:
            logger.error(f"Table extraction failed: {e}")
        
        return tables
    
    def extract_statistics(self, text: str) -> Dict[str, Any]:
        """Extract key statistics from text"""
        statistics = {
            'adoption_rates': [],
            'financial_metrics': [],
            'growth_rates': [],
            'years_mentioned': [],
            'sector_specific': {}
        }
        
        # Extract adoption rates
        for match in self.extraction_patterns['adoption_rate'].finditer(text):
            rate = float(match.group(1))
            context = text[max(0, match.start()-50):min(len(text), match.end()+50)]
            statistics['adoption_rates'].append({
                'value': rate,
                'context': context.strip()
            })
        
        # Extract financial metrics
        for match in self.extraction_patterns['currency'].finditer(text):
            value = float(match.group(1).replace(',', ''))
            unit = match.group(2) if match.group(2) else 'dollars'
            context = text[max(0, match.start()-50):min(len(text), match.end()+50)]
            statistics['financial_metrics'].append({
                'value': value,
                'unit': unit,
                'context': context.strip()
            })
        
        # Extract growth rates
        for match in self.extraction_patterns['growth_rate'].finditer(text):
            rate = float(match.group(1))
            context = text[max(0, match.start()-50):min(len(text), match.end()+50)]
            statistics['growth_rates'].append({
                'value': rate,
                'context': context.strip()
            })
        
        # Extract years
        years = list(set(self.extraction_patterns['year'].findall(text)))
        statistics['years_mentioned'] = sorted([int(y) for y in years])
        
        # Extract sector-specific data
        for match in self.extraction_patterns['sector_data'].finditer(text):
            sector = match.group(1).title()
            rate = float(match.group(2))
            statistics['sector_specific'][sector] = rate
        
        return statistics


class AutomatedDataIngestionPipeline:
    """Main pipeline for automated data ingestion from PDFs"""
    
    def __init__(self, resources_path: str = "AI adoption resources"):
        self.resources_path = Path(resources_path)
        self.text_processor = PDFTextProcessor()
        self.pdf_extractor = PDFDataExtractor()
        self.data_mapper = IntelligentDataMapper()
        self.scanner = AutomatedResearchScanner([str(self.resources_path)])
        self.processed_files_cache = self._load_processed_cache()
    
    def _load_processed_cache(self) -> Dict[str, Any]:
        """Load cache of processed files to avoid reprocessing"""
        cache_file = Path("data/processed_pdfs_cache.json")
        if cache_file.exists():
            try:
                with open(cache_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Error loading cache: {e}")
        return {}
    
    def _save_processed_cache(self):
        """Save processed files cache"""
        cache_file = Path("data/processed_pdfs_cache.json")
        cache_file.parent.mkdir(exist_ok=True)
        try:
            with open(cache_file, 'w') as f:
                json.dump(self.processed_files_cache, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving cache: {e}")
    
    def scan_for_pdfs(self) -> List[Path]:
        """Scan resources folder for PDF files"""
        pdf_files = []
        
        for root, dirs, files in os.walk(self.resources_path):
            for file in files:
                if file.lower().endswith('.pdf'):
                    pdf_files.append(Path(root) / file)
        
        logger.info(f"Found {len(pdf_files)} PDF files in resources folder")
        return pdf_files
    
    def process_pdf(self, filepath: Path) -> Dict[str, Any]:
        """Process a single PDF and extract data"""
        file_hash = self._calculate_file_hash(filepath)
        
        # Check cache
        if file_hash in self.processed_files_cache:
            logger.info(f"Using cached data for: {filepath.name}")
            return self.processed_files_cache[file_hash]
        
        logger.info(f"Processing new PDF: {filepath.name}")
        
        # Extract text and tables
        text = self.text_processor.extract_text_from_pdf(str(filepath))
        tables = self.text_processor.extract_tables_from_pdf(str(filepath))
        statistics = self.text_processor.extract_statistics(text)
        
        # Identify document metadata
        doc_metadata = self._identify_document_metadata(filepath, text)
        
        # Structure extracted data
        extracted_data = {
            'metadata': doc_metadata,
            'statistics': statistics,
            'tables': [self._table_to_dict(table) for table in tables],
            'text_length': len(text),
            'extraction_date': datetime.now().isoformat(),
            'file_hash': file_hash
        }
        
        # Cache the result
        self.processed_files_cache[file_hash] = extracted_data
        self._save_processed_cache()
        
        return extracted_data
    
    def _calculate_file_hash(self, filepath: Path) -> str:
        """Calculate file hash for caching"""
        with open(filepath, 'rb') as f:
            return hashlib.md5(f.read()).hexdigest()
    
    def _identify_document_metadata(self, filepath: Path, text: str) -> Dict[str, Any]:
        """Identify document metadata from filename and content"""
        filename = filepath.name
        
        # Identify authority
        authority = "Unknown"
        credibility = "B"
        
        for auth, patterns in self.scanner.integration_rules['authority_patterns'].items():
            if any(pattern.lower() in filename.lower() or pattern.lower() in text[:1000].lower() 
                   for pattern in patterns):
                authority = auth
                # Set credibility based on authority
                if auth in ['Stanford', 'McKinsey', 'Goldman Sachs', 'Federal Reserve', 'OECD']:
                    credibility = "A+"
                elif auth in ['NBER', 'IMF', 'MIT', 'Harvard', 'World Bank']:
                    credibility = "A"
                break
        
        # Extract year
        years = self.text_processor.extraction_patterns['year'].findall(text[:1000])
        year = max(years) if years else str(datetime.now().year)
        
        return {
            'filename': filename,
            'filepath': str(filepath),
            'authority': authority,
            'credibility': credibility,
            'year': year,
            'title': filename.replace('.pdf', '').replace('_', ' ').title()
        }
    
    def _table_to_dict(self, table: pd.DataFrame) -> Dict[str, Any]:
        """Convert DataFrame table to dictionary format"""
        return {
            'headers': table.columns.tolist(),
            'data': table.values.tolist(),
            'shape': table.shape
        }
    
    def generate_integrated_dataset(self, pdf_data_list: List[Dict[str, Any]], 
                                  dataset_type: str) -> pd.DataFrame:
        """Generate integrated dataset from multiple PDF extractions"""
        integrated_data = []
        
        for pdf_data in pdf_data_list:
            if dataset_type == 'adoption_rates':
                # Extract adoption rate data
                for stat in pdf_data['statistics'].get('adoption_rates', []):
                    integrated_data.append({
                        'value': stat['value'],
                        'context': stat['context'],
                        'source': pdf_data['metadata']['title'],
                        'authority': pdf_data['metadata']['authority'],
                        'year': pdf_data['metadata']['year'],
                        'credibility': pdf_data['metadata']['credibility']
                    })
                
                # Also check sector-specific data
                for sector, rate in pdf_data['statistics'].get('sector_specific', {}).items():
                    integrated_data.append({
                        'sector': sector,
                        'adoption_rate': rate,
                        'source': pdf_data['metadata']['title'],
                        'authority': pdf_data['metadata']['authority'],
                        'year': pdf_data['metadata']['year'],
                        'credibility': pdf_data['metadata']['credibility']
                    })
            
            elif dataset_type == 'financial_impact':
                # Extract financial metrics
                for metric in pdf_data['statistics'].get('financial_metrics', []):
                    integrated_data.append({
                        'value': metric['value'],
                        'unit': metric['unit'],
                        'context': metric['context'],
                        'source': pdf_data['metadata']['title'],
                        'authority': pdf_data['metadata']['authority'],
                        'year': pdf_data['metadata']['year']
                    })
            
            elif dataset_type == 'growth_rates':
                # Extract growth rates
                for rate in pdf_data['statistics'].get('growth_rates', []):
                    integrated_data.append({
                        'growth_rate': rate['value'],
                        'context': rate['context'],
                        'source': pdf_data['metadata']['title'],
                        'authority': pdf_data['metadata']['authority'],
                        'year': pdf_data['metadata']['year']
                    })
        
        if integrated_data:
            df = pd.DataFrame(integrated_data)
            # Remove duplicates based on value and source
            df = df.drop_duplicates(subset=['value', 'source'] if 'value' in df.columns else None)
            return df
        
        return pd.DataFrame()
    
    @st.cache_data(ttl=3600)
    def run_pipeline(self) -> Dict[str, pd.DataFrame]:
        """Run the complete ingestion pipeline"""
        logger.info("Starting automated data ingestion pipeline")
        
        # Scan for PDFs
        pdf_files = self.scan_for_pdfs()
        
        # Process each PDF
        all_pdf_data = []
        for pdf_file in pdf_files:
            try:
                pdf_data = self.process_pdf(pdf_file)
                all_pdf_data.append(pdf_data)
            except Exception as e:
                logger.error(f"Error processing {pdf_file}: {e}")
                continue
        
        # Generate integrated datasets
        datasets = {
            'adoption_rates': self.generate_integrated_dataset(all_pdf_data, 'adoption_rates'),
            'financial_impact': self.generate_integrated_dataset(all_pdf_data, 'financial_impact'),
            'growth_rates': self.generate_integrated_dataset(all_pdf_data, 'growth_rates'),
            'metadata': pd.DataFrame([data['metadata'] for data in all_pdf_data])
        }
        
        # Validate datasets
        for name, df in datasets.items():
            if not df.empty:
                validation = safe_validate_data(df, name, show_warnings=True)
                if validation.is_valid:
                    logger.info(f"✅ {name} dataset validated successfully")
                else:
                    logger.warning(f"⚠️ {name} dataset validation warnings: {validation.warnings}")
        
        logger.info(f"Pipeline completed. Processed {len(all_pdf_data)} PDFs")
        return datasets


# Initialize global pipeline instance
pdf_pipeline = AutomatedDataIngestionPipeline()