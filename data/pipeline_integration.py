"""
Pipeline Integration Module
Seamlessly integrates automated PDF extraction with existing data loading system
"""

import streamlit as st
import pandas as pd
import logging
from typing import Dict, Any, Optional, Tuple
from datetime import datetime
import os
from pathlib import Path

logger = logging.getLogger(__name__)


class PipelineIntegrationManager:
    """Manages integration between automated and manual data pipelines"""
    
    def __init__(self):
        self.use_automated_pipeline = self._check_automation_prerequisites()
        self.integration_status = {}
    
    def _check_automation_prerequisites(self) -> bool:
        """Check if automated pipeline can be enabled"""
        prerequisites = {
            'pdf_libraries': self._check_pdf_libraries(),
            'resources_folder': self._check_resources_folder(),
            'write_permissions': self._check_write_permissions()
        }
        
        all_met = all(prerequisites.values())
        
        if all_met:
            logger.info("✅ All prerequisites met for automated pipeline")
        else:
            missing = [k for k, v in prerequisites.items() if not v]
            logger.warning(f"⚠️ Missing prerequisites for automation: {missing}")
        
        return all_met
    
    def _check_pdf_libraries(self) -> bool:
        """Check if PDF processing libraries are available"""
        try:
            import PyPDF2
            import pdfplumber
            return True
        except ImportError as e:
            logger.warning(f"PDF libraries not available: {e}")
            return False
    
    def _check_resources_folder(self) -> bool:
        """Check if AI adoption resources folder exists and has PDFs"""
        resources_path = Path("AI adoption resources")
        if not resources_path.exists():
            logger.warning(f"Resources folder not found: {resources_path}")
            return False
        
        pdf_files = list(resources_path.rglob("*.pdf"))
        if not pdf_files:
            logger.warning("No PDF files found in resources folder")
            return False
        
        logger.info(f"Found {len(pdf_files)} PDF files in resources folder")
        return True
    
    def _check_write_permissions(self) -> bool:
        """Check if we can write cache files"""
        try:
            cache_dir = Path("data")
            cache_dir.mkdir(exist_ok=True)
            test_file = cache_dir / "test_write.tmp"
            test_file.write_text("test")
            test_file.unlink()
            return True
        except Exception as e:
            logger.warning(f"Write permissions issue: {e}")
            return False
    
    @st.cache_data(ttl=3600)
    def get_integration_strategy(self) -> Dict[str, str]:
        """Determine integration strategy based on system capabilities"""
        if self.use_automated_pipeline:
            return {
                'primary_method': 'automated',
                'fallback_method': 'manual',
                'pdf_extraction': 'enabled',
                'data_source': 'hybrid'
            }
        else:
            return {
                'primary_method': 'manual',
                'fallback_method': 'none',
                'pdf_extraction': 'disabled',
                'data_source': 'manual'
            }
    
    def load_data_with_strategy(self, dataset_name: str) -> Tuple[pd.DataFrame, Dict[str, Any]]:
        """Load data using the appropriate strategy"""
        strategy = self.get_integration_strategy()
        metadata = {
            'strategy_used': strategy['primary_method'],
            'pdf_extraction_enabled': strategy['pdf_extraction'] == 'enabled',
            'load_timestamp': datetime.now().isoformat()
        }
        
        if strategy['primary_method'] == 'automated':
            try:
                df, extraction_info = self._load_automated(dataset_name)
                metadata.update(extraction_info)
                return df, metadata
            except Exception as e:
                logger.warning(f"Automated loading failed for {dataset_name}: {e}")
                if strategy['fallback_method'] == 'manual':
                    logger.info(f"Falling back to manual loading for {dataset_name}")
                    df = self._load_manual(dataset_name)
                    metadata['strategy_used'] = 'manual_fallback'
                    return df, metadata
                else:
                    raise
        else:
            df = self._load_manual(dataset_name)
            return df, metadata
    
    def _load_automated(self, dataset_name: str) -> Tuple[pd.DataFrame, Dict[str, Any]]:
        """Load data using automated pipeline"""
        from .automated_loaders import automated_loader
        
        loader_mapping = {
            'historical_data': automated_loader.load_historical_data_automated,
            'sector_data': automated_loader.load_sector_data_automated,
            'financial_impact': automated_loader.load_financial_impact_automated
        }
        
        if dataset_name in loader_mapping:
            df = loader_mapping[dataset_name]()
            extraction_info = {
                'extraction_method': 'automated_pdf',
                'source_type': 'pdf_extraction'
            }
            return df, extraction_info
        else:
            raise ValueError(f"Automated loader not available for {dataset_name}")
    
    def _load_manual(self, dataset_name: str) -> pd.DataFrame:
        """Load data using manual/existing pipeline"""
        from .research_integration import research_integrator
        
        loader_mapping = {
            'historical_data': research_integrator.get_authentic_historical_data,
            'sector_data': research_integrator.get_authentic_sector_data_2025,
            'financial_impact': research_integrator.get_authentic_financial_impact_data,
            'investment_data': research_integrator.get_authentic_investment_data,
            'productivity_data': research_integrator.get_authentic_productivity_data,
            'skill_gap_data': research_integrator.get_authentic_skill_gap_data,
            'geographic_data': research_integrator.get_authentic_geographic_data,
            'governance_data': research_integrator.get_authentic_governance_data,
            'environmental_data': research_integrator.get_authentic_environmental_data,
            'cost_trend_data': research_integrator.get_authentic_cost_trend_data,
            'token_economics_data': research_integrator.get_authentic_token_economics_data,
            'maturity_data': research_integrator.get_authentic_maturity_data,
            'firm_size_data': research_integrator.get_authentic_firm_size_impact_data
        }
        
        if dataset_name in loader_mapping:
            return loader_mapping[dataset_name]()
        else:
            raise ValueError(f"Manual loader not available for {dataset_name}")
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get comprehensive system status for monitoring"""
        strategy = self.get_integration_strategy()
        
        status = {
            'integration_strategy': strategy,
            'automation_enabled': self.use_automated_pipeline,
            'prerequisites': {
                'pdf_libraries': self._check_pdf_libraries(),
                'resources_folder': self._check_resources_folder(),
                'write_permissions': self._check_write_permissions()
            },
            'system_info': {
                'timestamp': datetime.now().isoformat(),
                'python_version': os.sys.version.split()[0],
                'streamlit_available': True  # If we're running this, Streamlit is available
            }
        }
        
        return status
        
    def display_integration_status(self):
        """Display integration status in Streamlit sidebar"""
        with st.sidebar:
            st.subheader("🔧 Data Pipeline Status")
            
            status = self.get_system_status()
            
            # Show current strategy
            if status['automation_enabled']:
                st.success("🚀 Automated PDF extraction enabled")
                st.info("📊 Using hybrid data loading (PDF + manual)")
            else:
                st.warning("📋 Using manual data integration")
                st.info("💡 Install PDF libraries to enable automation")
            
            # Show prerequisites
            with st.expander("System Prerequisites"):
                for name, met in status['prerequisites'].items():
                    icon = "✅" if met else "❌"
                    st.write(f"{icon} {name.replace('_', ' ').title()}")
            
            # Show extraction stats if available
            if status['automation_enabled']:
                try:
                    from .automated_loaders import automated_loader
                    metadata_df = automated_loader.get_extraction_metadata()
                    if not metadata_df.empty:
                        st.metric("PDFs Processed", len(metadata_df))
                        st.metric("Unique Sources", len(metadata_df['authority'].unique()))
                except Exception as e:
                    st.error(f"Error getting extraction stats: {e}")


# Global integration manager
integration_manager = PipelineIntegrationManager()


@st.cache_data(ttl=3600, show_spinner=True)  
def load_all_datasets_integrated() -> Tuple[Dict[str, pd.DataFrame], Dict[str, Any]]:
    """
    Main entry point for integrated data loading
    This replaces the original load_all_datasets with intelligent automation
    """
    logger.info("🔄 Starting integrated data loading")
    
    datasets = {}
    overall_metadata = {
        'load_timestamp': datetime.now().isoformat(),
        'integration_strategy': integration_manager.get_integration_strategy(),
        'individual_loads': {}
    }
    
    # Define all datasets to load
    dataset_names = [
        'historical_data', 'sector_data', 'financial_impact', 'investment_data',
        'productivity_data', 'skill_gap_data', 'geographic_data', 'governance_data',  
        'environmental_data', 'cost_trend_data', 'token_economics_data', 
        'maturity_data', 'firm_size_data'
    ]
    
    # Load each dataset with appropriate strategy
    for dataset_name in dataset_names:
        try:
            df, metadata = integration_manager.load_data_with_strategy(dataset_name)
            datasets[dataset_name] = df
            overall_metadata['individual_loads'][dataset_name] = metadata
            
            logger.info(f"✅ Loaded {dataset_name} using {metadata['strategy_used']} method")
            
        except Exception as e:
            logger.error(f"❌ Failed to load {dataset_name}: {e}")
            # Create empty DataFrame to prevent app crashes
            datasets[dataset_name] = pd.DataFrame()
            overall_metadata['individual_loads'][dataset_name] = {
                'strategy_used': 'failed',
                'error': str(e)
            }
    
    # Summary statistics
    successful_loads = len([k for k, v in datasets.items() if not v.empty])
    overall_metadata['summary'] = {
        'total_datasets': len(dataset_names),
        'successful_loads': successful_loads,
        'success_rate': successful_loads / len(dataset_names) * 100,
        'automated_loads': len([v for v in overall_metadata['individual_loads'].values() 
                               if v.get('strategy_used') == 'automated']),
        'manual_loads': len([v for v in overall_metadata['individual_loads'].values() 
                            if v.get('strategy_used') in ['manual', 'manual_fallback']])
    }
    
    logger.info(f"📊 Integration complete: {successful_loads}/{len(dataset_names)} datasets loaded")
    
    return datasets, overall_metadata