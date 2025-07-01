"""
AI Adoption Dashboard Export System

Professional-grade export capabilities for enterprise reporting and presentations.
Supports multiple formats: PDF, PowerPoint, Excel, JSON, XML, CSV, HTML, and high-res images.

Key Features:
- Multi-format export support
- Professional templates and branding
- Cross-persona comparison reports
- Executive summary generation
- Quality assurance and validation
- Background processing with progress tracking
"""

from .core import ExportManager, ExportFormat, ExportStatus
from .pdf import PDFExporter
from .powerpoint import PowerPointExporter
from .excel import ExcelExporter
from .data import DataExporter
from .images import ImageExporter
from .html import HTMLExporter
from .templates import TemplateManager
from .validation import ExportValidator

__version__ = "1.0.0"
__all__ = [
    "ExportManager",
    "ExportFormat", 
    "ExportStatus",
    "PDFExporter",
    "PowerPointExporter", 
    "ExcelExporter",
    "DataExporter",
    "ImageExporter",
    "HTMLExporter",
    "TemplateManager",
    "ExportValidator"
]