"""
Automated Research Scanner and Integration System
Automatically detects, processes, and integrates new research PDFs into the dashboard
"""

import os
import hashlib
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
import pandas as pd
from dataclasses import dataclass, asdict
import re

logger = logging.getLogger(__name__)


@dataclass
class ResearchDocument:
    """Data class for research document metadata"""
    filename: str
    filepath: str
    file_hash: str
    detected_date: str
    file_size: int
    title: Optional[str] = None
    authority: Optional[str] = None
    year: Optional[str] = None
    category: Optional[str] = None
    credibility_rating: Optional[str] = None
    integration_status: str = 'pending'
    extraction_method: Optional[str] = None
    key_findings: Optional[Dict] = None
    data_tables: Optional[List[Dict]] = None


class AutomatedResearchScanner:
    """
    Automated scanner for new research documents
    Monitors folders and integrates new PDFs automatically
    """
    
    def __init__(self, watch_folders: List[str], config_path: str = "data/research_scanner_config.json"):
        self.watch_folders = watch_folders
        self.config_path = config_path
        self.scanned_documents = self._load_scan_history()
        self.integration_rules = self._load_integration_rules()
        
    def _load_scan_history(self) -> Dict[str, ResearchDocument]:
        """Load history of previously scanned documents"""
        history_file = Path(self.config_path).parent / "scan_history.json"
        if history_file.exists():
            try:
                with open(history_file, 'r') as f:
                    data = json.load(f)
                    return {k: ResearchDocument(**v) for k, v in data.items()}
            except Exception as e:
                logger.error(f"Error loading scan history: {e}")
        return {}
    
    def _save_scan_history(self):
        """Save scan history to persistent storage"""
        history_file = Path(self.config_path).parent / "scan_history.json"
        try:
            data = {k: asdict(v) for k, v in self.scanned_documents.items()}
            with open(history_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving scan history: {e}")
    
    def _load_integration_rules(self) -> Dict[str, Any]:
        """Load rules for automatic document categorization and integration"""
        return {
            'authority_patterns': {
                'Stanford': ['Stanford', 'HAI', 'Human-Centered AI'],
                'McKinsey': ['McKinsey', 'McKinsey & Company'],
                'Goldman Sachs': ['Goldman Sachs', 'GS Research'],
                'Federal Reserve': ['Federal Reserve', 'Fed', 'Richmond Fed', 'St. Louis Fed'],
                'OECD': ['OECD', 'Organisation for Economic Co-operation'],
                'NBER': ['NBER', 'National Bureau of Economic Research'],
                'IMF': ['IMF', 'International Monetary Fund'],
                'NVIDIA': ['NVIDIA', 'NVIDIA Corporation'],
                'MIT': ['MIT', 'Massachusetts Institute of Technology'],
                'Harvard': ['Harvard', 'HBS', 'Harvard Business School'],
                'World Bank': ['World Bank', 'IBRD'],
                'Brookings': ['Brookings', 'Brookings Institution']
            },
            'category_keywords': {
                'economic_analysis': ['GDP', 'economic', 'growth', 'productivity', 'labor', 'wages'],
                'policy_research': ['policy', 'regulation', 'governance', 'framework', 'compliance'],
                'technical_analysis': ['technical', 'architecture', 'implementation', 'MLOps', 'engineering'],
                'sector_analysis': ['industry', 'sector', 'vertical', 'healthcare', 'finance', 'manufacturing'],
                'adoption_studies': ['adoption', 'deployment', 'implementation', 'maturity', 'readiness'],
                'cost_analysis': ['cost', 'ROI', 'investment', 'pricing', 'economics', 'budget'],
                'workforce_impact': ['workforce', 'employment', 'skills', 'talent', 'human capital'],
                'case_studies': ['case study', 'example', 'success story', 'implementation guide']
            },
            'credibility_mapping': {
                'A+': ['Stanford', 'MIT', 'Harvard', 'NBER', 'Federal Reserve', 'IMF', 'OECD', 'World Bank'],
                'A': ['McKinsey', 'Goldman Sachs', 'Brookings', 'NVIDIA', 'Deloitte', 'PwC', 'BCG'],
                'B+': ['Industry reports', 'Technology vendors', 'Research firms'],
                'B': ['White papers', 'Technical documentation', 'Blog posts']
            }
        }
    
    def _calculate_file_hash(self, filepath: str) -> str:
        """Calculate SHA256 hash of file for deduplication"""
        sha256_hash = hashlib.sha256()
        with open(filepath, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    
    def _extract_metadata_from_filename(self, filename: str) -> Dict[str, Optional[str]]:
        """Extract metadata from filename patterns"""
        metadata = {
            'title': None,
            'authority': None,
            'year': None
        }
        
        # Clean filename
        clean_name = filename.replace('.pdf', '').replace('_', ' ').replace('-', ' ')
        
        # Extract year (look for 4-digit year)
        year_match = re.search(r'20[1-9]\d', clean_name)
        if year_match:
            metadata['year'] = year_match.group()
        
        # Extract authority based on patterns
        for authority, patterns in self.integration_rules['authority_patterns'].items():
            for pattern in patterns:
                if pattern.lower() in clean_name.lower():
                    metadata['authority'] = authority
                    break
        
        # Use cleaned filename as title if no specific title found
        metadata['title'] = clean_name.strip()
        
        return metadata
    
    def _categorize_document(self, filename: str, filepath: str) -> Tuple[str, str]:
        """Categorize document based on filename and content patterns"""
        category = 'general_research'
        credibility = 'B'
        
        # Check filename for category keywords
        filename_lower = filename.lower()
        for cat, keywords in self.integration_rules['category_keywords'].items():
            if any(keyword in filename_lower for keyword in keywords):
                category = cat
                break
        
        # Determine credibility based on authority
        metadata = self._extract_metadata_from_filename(filename)
        if metadata['authority']:
            for rating, authorities in self.integration_rules['credibility_mapping'].items():
                if metadata['authority'] in authorities:
                    credibility = rating
                    break
        
        return category, credibility
    
    def scan_for_new_documents(self) -> List[ResearchDocument]:
        """Scan watch folders for new PDF documents"""
        new_documents = []
        
        for folder in self.watch_folders:
            if not os.path.exists(folder):
                logger.warning(f"Watch folder does not exist: {folder}")
                continue
            
            # Recursively scan for PDFs
            for root, _, files in os.walk(folder):
                for file in files:
                    if file.lower().endswith('.pdf'):
                        filepath = os.path.join(root, file)
                        file_hash = self._calculate_file_hash(filepath)
                        
                        # Skip if already scanned
                        if file_hash in self.scanned_documents:
                            continue
                        
                        # Extract metadata
                        metadata = self._extract_metadata_from_filename(file)
                        category, credibility = self._categorize_document(file, filepath)
                        
                        # Create new document record
                        doc = ResearchDocument(
                            filename=file,
                            filepath=filepath,
                            file_hash=file_hash,
                            detected_date=datetime.now().isoformat(),
                            file_size=os.path.getsize(filepath),
                            title=metadata['title'],
                            authority=metadata['authority'],
                            year=metadata['year'],
                            category=category,
                            credibility_rating=credibility,
                            integration_status='pending'
                        )
                        
                        new_documents.append(doc)
                        self.scanned_documents[file_hash] = doc
                        
                        logger.info(f"New document detected: {file} (Category: {category}, Credibility: {credibility})")
        
        # Save updated scan history
        if new_documents:
            self._save_scan_history()
        
        return new_documents
    
    def generate_integration_code(self, document: ResearchDocument) -> str:
        """Generate Python code to integrate the document into research_integration.py"""
        method_name = f"get_{document.category}_{document.file_hash[:8]}_data"
        
        # Generate the integration method
        code = f'''
    def {method_name}(self) -> pd.DataFrame:
        """
        {document.title}
        Source: {document.filename}
        Authority: {document.authority or 'Unknown'}
        Category: {document.category}
        """
        logger.info("Loading {document.category} research from {document.authority or 'new source'}")
        
        # TODO: Implement actual data extraction from PDF
        # This is a template - actual implementation would parse the PDF
        data = pd.DataFrame({{
            'metric': ['Placeholder metric 1', 'Placeholder metric 2'],
            'value': [0, 0],
            'data_source': ['{document.title}'] * 2,
            'credibility_rating': ['{document.credibility_rating}'] * 2,
            'year': ['{document.year or "2024"}'] * 2
        }})
        
        logger.info("✅ {document.title} data loaded")
        return data
'''
        
        # Also generate the registry entry
        registry_entry = f'''
            '{document.file_hash[:16]}': {{
                'name': '{document.title}',
                'file': '{document.filename}',
                'authority': '{document.authority or "Research Organization"}',
                'credibility': '{document.credibility_rating}',
                'last_updated': '{document.year or "2024"}'
            }},'''
        
        return code, registry_entry
    
    def get_integration_recommendations(self) -> pd.DataFrame:
        """Get recommendations for pending document integrations"""
        pending_docs = [doc for doc in self.scanned_documents.values() 
                       if doc.integration_status == 'pending']
        
        if not pending_docs:
            return pd.DataFrame()
        
        recommendations = []
        for doc in pending_docs:
            recommendations.append({
                'filename': doc.filename,
                'authority': doc.authority or 'Unknown',
                'category': doc.category,
                'credibility': doc.credibility_rating,
                'detected_date': doc.detected_date,
                'file_size_mb': round(doc.file_size / (1024 * 1024), 2),
                'integration_priority': self._calculate_priority(doc),
                'action_required': 'Review and integrate'
            })
        
        df = pd.DataFrame(recommendations)
        return df.sort_values('integration_priority', ascending=False)
    
    def _calculate_priority(self, doc: ResearchDocument) -> int:
        """Calculate integration priority based on credibility and category"""
        credibility_scores = {'A+': 10, 'A': 8, 'B+': 6, 'B': 4}
        category_scores = {
            'economic_analysis': 9,
            'policy_research': 8,
            'adoption_studies': 8,
            'sector_analysis': 7,
            'workforce_impact': 7,
            'technical_analysis': 6,
            'cost_analysis': 6,
            'case_studies': 5,
            'general_research': 4
        }
        
        cred_score = credibility_scores.get(doc.credibility_rating, 4)
        cat_score = category_scores.get(doc.category, 4)
        
        return cred_score + cat_score
    
    def mark_document_integrated(self, file_hash: str):
        """Mark a document as integrated"""
        if file_hash in self.scanned_documents:
            self.scanned_documents[file_hash].integration_status = 'integrated'
            self.scanned_documents[file_hash].extraction_method = 'automated'
            self._save_scan_history()
            logger.info(f"Document marked as integrated: {file_hash[:8]}")


# Automated integration workflow manager
class ResearchIntegrationWorkflow:
    """
    Manages the workflow for automatically integrating new research
    """
    
    def __init__(self, scanner: AutomatedResearchScanner):
        self.scanner = scanner
        self.integration_queue = []
    
    def run_integration_check(self) -> Dict[str, Any]:
        """Run a check for new documents and prepare integration"""
        # Scan for new documents
        new_docs = self.scanner.scan_for_new_documents()
        
        # Get recommendations
        recommendations = self.scanner.get_integration_recommendations()
        
        # Generate integration report
        report = {
            'scan_timestamp': datetime.now().isoformat(),
            'new_documents_found': len(new_docs),
            'pending_integrations': len(recommendations),
            'high_priority_count': len(recommendations[recommendations['integration_priority'] >= 15]) if len(recommendations) > 0 else 0,
            'recommendations': recommendations,
            'new_documents': new_docs
        }
        
        return report
    
    def generate_batch_integration_code(self, doc_hashes: List[str]) -> str:
        """Generate integration code for multiple documents"""
        code_blocks = []
        registry_entries = []
        
        for hash_id in doc_hashes:
            if hash_id in self.scanner.scanned_documents:
                doc = self.scanner.scanned_documents[hash_id]
                code, registry = self.scanner.generate_integration_code(doc)
                code_blocks.append(code)
                registry_entries.append(registry)
        
        return '\n'.join(code_blocks), '\n'.join(registry_entries)


# Streamlit UI component for automated scanning
def display_automated_scanner_dashboard():
    """Display the automated research scanner dashboard in Streamlit"""
    import streamlit as st
    
    st.markdown("### 🔍 Automated Research Scanner")
    
    # Initialize scanner
    watch_folders = [
        "AI adoption resources",
        "research_documents",
        "new_research"
    ]
    
    scanner = AutomatedResearchScanner(watch_folders)
    workflow = ResearchIntegrationWorkflow(scanner)
    
    # Run scan
    if st.button("🔄 Scan for New Research Documents"):
        with st.spinner("Scanning folders for new PDFs..."):
            report = workflow.run_integration_check()
        
        # Display results
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("New Documents", report['new_documents_found'])
        
        with col2:
            st.metric("Pending Integration", report['pending_integrations'])
        
        with col3:
            st.metric("High Priority", report['high_priority_count'])
        
        # Show recommendations table
        if report['pending_integrations'] > 0:
            st.markdown("#### 📋 Integration Recommendations")
            st.dataframe(
                report['recommendations'],
                use_container_width=True,
                hide_index=True
            )
            
            # Integration actions
            st.markdown("#### 🚀 Integration Actions")
            
            selected_docs = st.multiselect(
                "Select documents to integrate:",
                options=[doc.file_hash for doc in report['new_documents']],
                format_func=lambda x: next(d.filename for d in report['new_documents'] if d.file_hash == x)
            )
            
            if selected_docs and st.button("Generate Integration Code"):
                code, registry = workflow.generate_batch_integration_code(selected_docs)
                
                st.markdown("##### Generated Integration Code:")
                st.code(code, language='python')
                
                st.markdown("##### Registry Entries:")
                st.code(registry, language='python')
                
                st.success("✅ Integration code generated! Copy and add to research_integration.py")
    
    # Show scan history
    with st.expander("📜 Scan History"):
        history_data = []
        for doc in scanner.scanned_documents.values():
            history_data.append({
                'Filename': doc.filename,
                'Authority': doc.authority or 'Unknown',
                'Category': doc.category,
                'Status': doc.integration_status,
                'Detected': doc.detected_date[:10]
            })
        
        if history_data:
            st.dataframe(pd.DataFrame(history_data), use_container_width=True)
        else:
            st.info("No documents scanned yet")


# Export the scanner for use in other modules
automated_scanner = AutomatedResearchScanner([
    "AI adoption resources",
    "research_documents"
])