"""
Data Export System for AI Adoption Dashboard

Comprehensive data export capabilities supporting JSON, XML, CSV formats
with structured data organization, metadata inclusion, and validation.
"""

import os
import json
import csv
import xml.etree.ElementTree as ET
from datetime import datetime
from typing import Dict, List, Optional, Any, Callable, Union
from pathlib import Path
import logging

import pandas as pd
import numpy as np
from lxml import etree

from .core import ExportSettings, ExportFormat
from .templates import TemplateManager

logger = logging.getLogger(__name__)


class DataExporter:
    """
    Professional data export system for AI Adoption Dashboard
    
    Features:
    - Multiple format support (JSON, XML, CSV)
    - Structured data organization
    - Metadata and provenance tracking
    - Data validation and quality checks
    - Compressed archives for large datasets
    - API-compatible JSON structures
    """
    
    def __init__(self, output_dir: Path):
        self.output_dir = output_dir
        self.template_manager = TemplateManager()
    
    def export(
        self,
        data: Dict[str, Any],
        persona: Optional[str] = None,
        view: Optional[str] = None,
        settings: ExportSettings = None,
        progress_callback: Optional[Callable] = None,
        format: ExportFormat = ExportFormat.JSON,
        **options
    ) -> Path:
        """
        Export data in specified format
        
        Args:
            data: Dashboard data to export
            persona: Target persona
            view: Specific view to export
            settings: Export settings
            progress_callback: Progress update callback
            format: Export format (JSON, XML, CSV)
            **options: Additional export options
            
        Returns:
            Path to generated export file
        """
        if settings is None:
            settings = ExportSettings()
            
        if progress_callback:
            progress_callback(0.1)
        
        # Generate filename
        filename = self._generate_filename(persona, view, format)
        output_path = self.output_dir / filename
        
        # Prepare data with metadata
        export_data = self._prepare_export_data(data, persona, view, settings)
        
        if progress_callback:
            progress_callback(0.3)
        
        # Export based on format
        if format == ExportFormat.JSON:
            self._export_json(export_data, output_path, settings, **options)
        elif format == ExportFormat.XML:
            self._export_xml(export_data, output_path, settings, **options)
        elif format == ExportFormat.CSV:
            self._export_csv(export_data, output_path, settings, **options)
        else:
            raise ValueError(f"Unsupported data export format: {format}")
        
        if progress_callback:
            progress_callback(1.0)
        
        logger.info(f"Generated {format.value.upper()} export: {output_path}")
        return output_path
    
    def _generate_filename(self, persona: Optional[str], view: Optional[str], format: ExportFormat) -> str:
        """Generate appropriate filename for the export"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if persona and persona != "General":
            base_name = f"AI_Dashboard_{persona.replace(' ', '_')}_Data"
        elif view:
            base_name = f"AI_Dashboard_{view.replace(' ', '_')}_Data"
        else:
            base_name = "AI_Dashboard_Complete_Data"
        
        return f"{base_name}_{timestamp}.{format.value}"
    
    def _prepare_export_data(self, data: Dict[str, Any], persona: Optional[str], view: Optional[str], settings: ExportSettings) -> Dict[str, Any]:
        """Prepare data for export with metadata and structure"""
        export_data = {
            "metadata": {
                "export_timestamp": datetime.now().isoformat(),
                "dashboard_version": "2.0",
                "export_format": "structured_data",
                "persona": persona,
                "view": view,
                "data_sources": [
                    "industry_surveys",
                    "academic_research", 
                    "government_statistics",
                    "vendor_analytics"
                ],
                "methodology": "multi_dimensional_adoption_modeling",
                "confidence_level": "95%",
                "geographic_coverage": "global",
                "temporal_coverage": "2020-2024",
                "update_frequency": "monthly",
                "data_quality": {
                    "completeness": self._calculate_completeness(data),
                    "accuracy": "high",
                    "timeliness": "current",
                    "consistency": "validated"
                }
            },
            "summary": self._generate_data_summary(data),
            "datasets": {}
        }
        
        # Process each dataset
        for dataset_name, dataset in data.items():
            if dataset is not None:
                export_data["datasets"][dataset_name] = self._process_dataset(dataset, dataset_name)
        
        return export_data
    
    def _process_dataset(self, dataset: Any, dataset_name: str) -> Dict[str, Any]:
        """Process individual dataset for export"""
        processed = {
            "name": dataset_name,
            "type": self._get_dataset_type(dataset),
            "description": self._get_dataset_description(dataset_name),
            "last_updated": datetime.now().isoformat(),
            "record_count": self._get_record_count(dataset),
            "data": self._serialize_dataset(dataset)
        }
        
        # Add schema information for DataFrames
        if isinstance(dataset, pd.DataFrame):
            processed["schema"] = self._generate_schema(dataset)
            processed["statistics"] = self._generate_statistics(dataset)
        
        return processed
    
    def _serialize_dataset(self, dataset: Any) -> Any:
        """Serialize dataset to JSON-compatible format"""
        if isinstance(dataset, pd.DataFrame):
            # Convert DataFrame to records format
            return {
                "columns": dataset.columns.tolist(),
                "data": dataset.to_dict('records'),
                "index": dataset.index.tolist() if not isinstance(dataset.index, pd.RangeIndex) else None
            }
        elif isinstance(dataset, dict):
            # Recursively serialize nested dictionaries
            return {k: self._serialize_value(v) for k, v in dataset.items()}
        elif isinstance(dataset, list):
            return [self._serialize_value(item) for item in dataset]
        else:
            return self._serialize_value(dataset)
    
    def _serialize_value(self, value: Any) -> Any:
        """Serialize individual values"""
        if isinstance(value, (np.integer, np.floating)):
            return value.item()
        elif isinstance(value, np.ndarray):
            return value.tolist()
        elif isinstance(value, pd.Timestamp):
            return value.isoformat()
        elif isinstance(value, datetime):
            return value.isoformat()
        elif pd.isna(value):
            return None
        else:
            return value
    
    def _export_json(self, data: Dict[str, Any], output_path: Path, settings: ExportSettings, **options):
        """Export data to JSON format"""
        json_options = {
            'ensure_ascii': False,
            'indent': 2 if options.get('pretty_print', True) else None,
            'separators': (',', ': ') if options.get('pretty_print', True) else (',', ':'),
            'sort_keys': options.get('sort_keys', True)
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, **json_options, default=self._json_serializer)
    
    def _export_xml(self, data: Dict[str, Any], output_path: Path, settings: ExportSettings, **options):
        """Export data to XML format"""
        root = ET.Element("ai_dashboard_export")
        
        # Add metadata
        metadata_elem = ET.SubElement(root, "metadata")
        self._dict_to_xml(data["metadata"], metadata_elem)
        
        # Add summary
        summary_elem = ET.SubElement(root, "summary")
        self._dict_to_xml(data["summary"], summary_elem)
        
        # Add datasets
        datasets_elem = ET.SubElement(root, "datasets")
        for dataset_name, dataset_data in data["datasets"].items():
            dataset_elem = ET.SubElement(datasets_elem, "dataset", name=dataset_name)
            self._dict_to_xml(dataset_data, dataset_elem)
        
        # Create XML tree and write
        tree = ET.ElementTree(root)
        ET.indent(tree, space="  ", level=0)  # Pretty print
        tree.write(output_path, encoding='utf-8', xml_declaration=True)
    
    def _export_csv(self, data: Dict[str, Any], output_path: Path, settings: ExportSettings, **options):
        """Export data to CSV format (creates multiple files if needed)"""
        csv_dir = output_path.parent / output_path.stem
        csv_dir.mkdir(exist_ok=True)
        
        # Export metadata as JSON
        metadata_path = csv_dir / "metadata.json"
        with open(metadata_path, 'w', encoding='utf-8') as f:
            json.dump({
                "metadata": data["metadata"],
                "summary": data["summary"]
            }, f, indent=2, default=self._json_serializer)
        
        # Export each dataset as CSV
        for dataset_name, dataset_data in data["datasets"].items():
            if dataset_data["type"] == "dataframe" and "data" in dataset_data["data"]:
                df_data = dataset_data["data"]["data"]
                if df_data:
                    df = pd.DataFrame(df_data)
                    csv_path = csv_dir / f"{dataset_name}.csv"
                    df.to_csv(csv_path, index=False, encoding='utf-8')
            elif dataset_data["type"] == "dict":
                # Export dict as key-value CSV
                csv_path = csv_dir / f"{dataset_name}.csv"
                with open(csv_path, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerow(['key', 'value'])
                    for k, v in dataset_data["data"].items():
                        writer.writerow([k, v])
        
        # Create a ZIP archive if multiple files
        if options.get('create_archive', True):
            import zipfile
            
            zip_path = output_path.with_suffix('.zip')
            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for file_path in csv_dir.rglob('*'):
                    if file_path.is_file():
                        zipf.write(file_path, file_path.relative_to(csv_dir))
            
            # Remove directory and return zip path
            import shutil
            shutil.rmtree(csv_dir)
            return zip_path
    
    def _dict_to_xml(self, data: Any, parent: ET.Element):
        """Convert dictionary to XML elements"""
        if isinstance(data, dict):
            for key, value in data.items():
                # Clean key name for XML
                clean_key = self._clean_xml_name(str(key))
                child = ET.SubElement(parent, clean_key)
                self._dict_to_xml(value, child)
        elif isinstance(data, list):
            for i, item in enumerate(data):
                item_elem = ET.SubElement(parent, "item", index=str(i))
                self._dict_to_xml(item, item_elem)
        else:
            parent.text = str(data) if data is not None else ""
    
    def _clean_xml_name(self, name: str) -> str:
        """Clean name for use as XML element name"""
        # Replace invalid characters
        cleaned = name.replace(' ', '_').replace('-', '_').replace('.', '_')
        # Ensure it starts with letter or underscore
        if not cleaned[0].isalpha() and not cleaned[0] == '_':
            cleaned = f"_{cleaned}"
        return cleaned
    
    def _json_serializer(self, obj):
        """Custom JSON serializer for special types"""
        if isinstance(obj, (pd.Timestamp, datetime)):
            return obj.isoformat()
        elif isinstance(obj, (np.integer, np.floating)):
            return obj.item()
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif pd.isna(obj):
            return None
        else:
            return str(obj)
    
    def _calculate_completeness(self, data: Dict[str, Any]) -> str:
        """Calculate data completeness percentage"""
        total_datasets = len(data)
        complete_datasets = 0
        
        for dataset in data.values():
            if dataset is not None:
                if isinstance(dataset, pd.DataFrame) and not dataset.empty:
                    complete_datasets += 1
                elif isinstance(dataset, dict) and dataset:
                    complete_datasets += 1
                elif isinstance(dataset, list) and dataset:
                    complete_datasets += 1
        
        completeness = (complete_datasets / total_datasets) * 100 if total_datasets > 0 else 0
        return f"{completeness:.0f}%"
    
    def _generate_data_summary(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate summary statistics for the data"""
        summary = {
            "total_datasets": len(data),
            "dataset_types": {},
            "total_records": 0,
            "date_range": {
                "earliest": None,
                "latest": None
            },
            "key_metrics": {}
        }
        
        for dataset_name, dataset in data.items():
            if dataset is not None:
                dataset_type = self._get_dataset_type(dataset)
                summary["dataset_types"][dataset_type] = summary["dataset_types"].get(dataset_type, 0) + 1
                summary["total_records"] += self._get_record_count(dataset)
                
                # Extract key metrics
                if dataset_name == 'historical_trends' and isinstance(dataset, pd.DataFrame):
                    if not dataset.empty and 'ai_use' in dataset.columns:
                        summary["key_metrics"]["current_ai_adoption"] = f"{dataset['ai_use'].iloc[-1]:.1f}%"
                        summary["key_metrics"]["ai_adoption_growth"] = f"{self._calculate_growth_rate(dataset['ai_use']):.1f}%"
                
                # Update date range
                dates = self._extract_dates(dataset)
                if dates:
                    if summary["date_range"]["earliest"] is None or min(dates) < summary["date_range"]["earliest"]:
                        summary["date_range"]["earliest"] = min(dates).isoformat()
                    if summary["date_range"]["latest"] is None or max(dates) > summary["date_range"]["latest"]:
                        summary["date_range"]["latest"] = max(dates).isoformat()
        
        return summary
    
    def _get_dataset_type(self, dataset: Any) -> str:
        """Determine the type of dataset"""
        if isinstance(dataset, pd.DataFrame):
            return "dataframe"
        elif isinstance(dataset, dict):
            return "dict"
        elif isinstance(dataset, list):
            return "list"
        else:
            return "scalar"
    
    def _get_dataset_description(self, dataset_name: str) -> str:
        """Get description for dataset"""
        descriptions = {
            "historical_trends": "Historical AI adoption trends over time",
            "geographic_data": "Geographic distribution of AI adoption rates",
            "roi_data": "Return on investment analysis and projections",
            "competitive_data": "Competitive position and market analysis",
            "labor_data": "Labor market impact and workforce analysis",
            "regulatory_data": "Regulatory landscape and policy analysis",
            "technology_data": "AI technology maturity and capability assessment",
            "adoption_barriers": "Barriers to AI adoption and mitigation strategies",
            "use_cases": "AI use cases and application scenarios",
            "investment_data": "Investment trends and funding analysis"
        }
        return descriptions.get(dataset_name, f"Data related to {dataset_name.replace('_', ' ')}")
    
    def _get_record_count(self, dataset: Any) -> int:
        """Get number of records in dataset"""
        if isinstance(dataset, pd.DataFrame):
            return len(dataset)
        elif isinstance(dataset, (list, dict)):
            return len(dataset)
        else:
            return 1 if dataset is not None else 0
    
    def _generate_schema(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Generate schema information for DataFrame"""
        schema = {
            "columns": {},
            "shape": list(df.shape),
            "dtypes": df.dtypes.astype(str).to_dict()
        }
        
        for col in df.columns:
            schema["columns"][col] = {
                "dtype": str(df[col].dtype),
                "nullable": df[col].isnull().any(),
                "unique_values": df[col].nunique(),
                "sample_values": df[col].dropna().head(3).tolist()
            }
        
        return schema
    
    def _generate_statistics(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Generate statistical summary for DataFrame"""
        stats = {
            "numeric_columns": {},
            "categorical_columns": {},
            "missing_values": df.isnull().sum().to_dict()
        }
        
        # Numeric columns
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) > 0:
            numeric_stats = df[numeric_cols].describe()
            stats["numeric_columns"] = numeric_stats.to_dict()
        
        # Categorical columns
        categorical_cols = df.select_dtypes(include=['object', 'category']).columns
        for col in categorical_cols:
            value_counts = df[col].value_counts().head(5)
            stats["categorical_columns"][col] = {
                "unique_count": df[col].nunique(),
                "top_values": value_counts.to_dict()
            }
        
        return stats
    
    def _extract_dates(self, dataset: Any) -> List[datetime]:
        """Extract dates from dataset"""
        dates = []
        
        if isinstance(dataset, pd.DataFrame):
            # Look for date columns
            date_cols = dataset.select_dtypes(include=['datetime64']).columns
            for col in date_cols:
                dates.extend(pd.to_datetime(dataset[col]).dropna().tolist())
            
            # Look for year columns
            if 'year' in dataset.columns:
                years = dataset['year'].dropna().astype(int)
                dates.extend([datetime(year, 1, 1) for year in years])
        
        return dates
    
    def _calculate_growth_rate(self, series: pd.Series) -> float:
        """Calculate compound annual growth rate"""
        if len(series) < 2:
            return 0
        
        first_value = series.iloc[0]
        last_value = series.iloc[-1]
        
        if first_value <= 0:
            return 0
        
        periods = len(series) - 1
        return ((last_value / first_value) ** (1 / periods) - 1) * 100


class APIExporter(DataExporter):
    """
    Specialized exporter for API-compatible JSON formats
    
    Features:
    - REST API compatible structure
    - OpenAPI/Swagger compatible schemas
    - Pagination support for large datasets
    - Rate limiting metadata
    - Version information
    """
    
    def export_api_format(
        self,
        data: Dict[str, Any],
        api_version: str = "v1",
        include_pagination: bool = True,
        page_size: int = 1000,
        **options
    ) -> Path:
        """Export in API-compatible format"""
        
        api_data = {
            "api_version": api_version,
            "timestamp": datetime.now().isoformat(),
            "status": "success",
            "data": {},
            "metadata": {
                "total_records": 0,
                "page_size": page_size if include_pagination else None,
                "available_endpoints": []
            }
        }
        
        # Process datasets for API format
        for dataset_name, dataset in data.items():
            if dataset is not None:
                endpoint_name = dataset_name.replace('_', '-')
                api_data["metadata"]["available_endpoints"].append(f"/{api_version}/{endpoint_name}")
                
                if isinstance(dataset, pd.DataFrame) and not dataset.empty:
                    records = dataset.to_dict('records')
                    
                    if include_pagination and len(records) > page_size:
                        # Paginate large datasets
                        pages = []
                        for i in range(0, len(records), page_size):
                            page_data = {
                                "page": (i // page_size) + 1,
                                "page_size": page_size,
                                "total_pages": (len(records) + page_size - 1) // page_size,
                                "total_records": len(records),
                                "data": records[i:i + page_size]
                            }
                            pages.append(page_data)
                        
                        api_data["data"][dataset_name] = {
                            "paginated": True,
                            "pages": pages
                        }
                    else:
                        api_data["data"][dataset_name] = {
                            "paginated": False,
                            "total_records": len(records),
                            "data": records
                        }
                    
                    api_data["metadata"]["total_records"] += len(records)
                
                elif isinstance(dataset, dict):
                    api_data["data"][dataset_name] = dataset
        
        # Generate filename
        filename = f"api_export_{api_version}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        output_path = self.output_dir / filename
        
        # Export
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(api_data, f, indent=2, default=self._json_serializer)
        
        return output_path


class DataValidator:
    """Data validation and quality assurance for exports"""
    
    @staticmethod
    def validate_export(export_path: Path, expected_format: ExportFormat) -> Dict[str, Any]:
        """Validate exported data file"""
        validation_result = {
            "valid": False,
            "format": expected_format.value,
            "file_size": 0,
            "issues": [],
            "quality_score": 0
        }
        
        if not export_path.exists():
            validation_result["issues"].append("Export file does not exist")
            return validation_result
        
        validation_result["file_size"] = export_path.stat().st_size
        
        try:
            if expected_format == ExportFormat.JSON:
                DataValidator._validate_json(export_path, validation_result)
            elif expected_format == ExportFormat.XML:
                DataValidator._validate_xml(export_path, validation_result)
            elif expected_format == ExportFormat.CSV:
                DataValidator._validate_csv(export_path, validation_result)
            
            # Calculate quality score
            issue_count = len(validation_result["issues"])
            validation_result["quality_score"] = max(0, 100 - (issue_count * 10))
            validation_result["valid"] = issue_count == 0
            
        except Exception as e:
            validation_result["issues"].append(f"Validation error: {str(e)}")
        
        return validation_result
    
    @staticmethod
    def _validate_json(file_path: Path, result: Dict[str, Any]):
        """Validate JSON file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Check required structure
            if not isinstance(data, dict):
                result["issues"].append("JSON root should be an object")
            
            if "metadata" not in data:
                result["issues"].append("Missing metadata section")
            
            if "datasets" not in data:
                result["issues"].append("Missing datasets section")
                
        except json.JSONDecodeError as e:
            result["issues"].append(f"Invalid JSON format: {str(e)}")
    
    @staticmethod
    def _validate_xml(file_path: Path, result: Dict[str, Any]):
        """Validate XML file"""
        try:
            tree = ET.parse(file_path)
            root = tree.getroot()
            
            if root.tag != "ai_dashboard_export":
                result["issues"].append("Invalid XML root element")
            
            if root.find("metadata") is None:
                result["issues"].append("Missing metadata section")
            
            if root.find("datasets") is None:
                result["issues"].append("Missing datasets section")
                
        except ET.ParseError as e:
            result["issues"].append(f"Invalid XML format: {str(e)}")
    
    @staticmethod
    def _validate_csv(file_path: Path, result: Dict[str, Any]):
        """Validate CSV file or archive"""
        if file_path.suffix == '.zip':
            # Validate ZIP archive
            import zipfile
            try:
                with zipfile.ZipFile(file_path, 'r') as zipf:
                    files = zipf.namelist()
                    if not any(f.endswith('.csv') for f in files):
                        result["issues"].append("No CSV files found in archive")
                    if 'metadata.json' not in files:
                        result["issues"].append("Missing metadata.json in archive")
            except zipfile.BadZipFile:
                result["issues"].append("Invalid ZIP archive")
        else:
            # Validate single CSV
            try:
                df = pd.read_csv(file_path)
                if df.empty:
                    result["issues"].append("CSV file is empty")
            except pd.errors.EmptyDataError:
                result["issues"].append("CSV file is empty")
            except Exception as e:
                result["issues"].append(f"Invalid CSV format: {str(e)}")