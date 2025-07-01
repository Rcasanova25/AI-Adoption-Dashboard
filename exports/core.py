"""
Core export system for AI Adoption Dashboard

Provides the main export management functionality with support for multiple formats,
quality assurance, progress tracking, and enterprise-grade features.
"""

import os
import uuid
import json
import time
import threading
from datetime import datetime, timedelta
from enum import Enum, auto
from typing import Dict, List, Optional, Any, Callable, Union
from dataclasses import dataclass, field
from pathlib import Path
import logging

import pandas as pd
import streamlit as st

# Set up logging
logger = logging.getLogger(__name__)


class ExportFormat(Enum):
    """Supported export formats"""
    PDF = "pdf"
    POWERPOINT = "pptx"
    EXCEL = "xlsx"
    JSON = "json"
    XML = "xml"
    CSV = "csv"
    HTML = "html"
    PNG = "png"
    SVG = "svg"
    INTERACTIVE_HTML = "interactive.html"


class ExportStatus(Enum):
    """Export job status"""
    PENDING = auto()
    IN_PROGRESS = auto()
    COMPLETED = auto()
    FAILED = auto()
    CANCELLED = auto()


@dataclass
class ExportJob:
    """Represents an export job"""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    format: ExportFormat = ExportFormat.PDF
    persona: Optional[str] = None
    view: Optional[str] = None
    data: Optional[Dict[str, Any]] = None
    options: Dict[str, Any] = field(default_factory=dict)
    status: ExportStatus = ExportStatus.PENDING
    created_at: datetime = field(default_factory=datetime.now)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    error_message: Optional[str] = None
    file_path: Optional[str] = None
    file_size: Optional[int] = None
    progress: float = 0.0
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ExportSettings:
    """Export configuration settings"""
    # Branding
    company_name: str = "AI Adoption Dashboard"
    company_logo: Optional[str] = None
    brand_colors: Dict[str, str] = field(default_factory=lambda: {
        'primary': '#1f77b4',
        'secondary': '#ff7f0e', 
        'accent': '#2ca02c',
        'text': '#333333',
        'background': '#ffffff'
    })
    
    # Layout
    page_orientation: str = "portrait"  # portrait, landscape
    page_size: str = "A4"  # A4, Letter, Legal
    margins: Dict[str, float] = field(default_factory=lambda: {
        'top': 1.0, 'bottom': 1.0, 'left': 1.0, 'right': 1.0
    })
    
    # Content
    include_executive_summary: bool = True
    include_methodology: bool = True
    include_appendix: bool = True
    include_cover_page: bool = True
    include_table_of_contents: bool = True
    
    # Quality
    image_dpi: int = 300
    chart_width: int = 1200
    chart_height: int = 800
    compress_images: bool = True
    
    # Security
    password_protect: bool = False
    password: Optional[str] = None
    watermark: Optional[str] = None
    
    # Metadata
    author: str = "AI Adoption Dashboard"
    subject: str = "AI Adoption Analysis Report"
    keywords: List[str] = field(default_factory=lambda: [
        "AI", "Artificial Intelligence", "Adoption", "Analysis", "Dashboard"
    ])


class ExportManager:
    """
    Main export manager for the AI Adoption Dashboard
    
    Handles export job creation, queue management, progress tracking,
    and coordination between different export formats.
    """
    
    def __init__(self, output_dir: str = "exports/output"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        self.jobs: Dict[str, ExportJob] = {}
        self.job_queue: List[str] = []
        self.active_jobs: Dict[str, threading.Thread] = {}
        self.max_concurrent_jobs = 3
        
        # Initialize exporters
        self._initialize_exporters()
        
        # Default settings
        self.default_settings = ExportSettings()
        
    def _initialize_exporters(self):
        """Initialize all export format handlers"""
        from .pdf import PDFExporter
        from .powerpoint import PowerPointExporter
        from .excel import ExcelExporter
        from .data import DataExporter
        from .images import ImageExporter
        from .html import HTMLExporter
        
        self.exporters = {
            ExportFormat.PDF: PDFExporter(self.output_dir),
            ExportFormat.POWERPOINT: PowerPointExporter(self.output_dir),
            ExportFormat.EXCEL: ExcelExporter(self.output_dir),
            ExportFormat.JSON: DataExporter(self.output_dir),
            ExportFormat.XML: DataExporter(self.output_dir),
            ExportFormat.CSV: DataExporter(self.output_dir),
            ExportFormat.PNG: ImageExporter(self.output_dir),
            ExportFormat.SVG: ImageExporter(self.output_dir),
            ExportFormat.HTML: HTMLExporter(self.output_dir),
            ExportFormat.INTERACTIVE_HTML: HTMLExporter(self.output_dir),
        }
    
    def create_export_job(
        self,
        format: ExportFormat,
        persona: Optional[str] = None,
        view: Optional[str] = None,
        data: Optional[Dict[str, Any]] = None,
        settings: Optional[ExportSettings] = None,
        **options
    ) -> str:
        """
        Create a new export job
        
        Args:
            format: Export format
            persona: Target persona (Business Leader, Policymaker, Researcher)
            view: Specific view to export
            data: Data to export
            settings: Export settings
            **options: Additional export options
            
        Returns:
            Job ID
        """
        job = ExportJob(
            format=format,
            persona=persona,
            view=view,
            data=data,
            options=options
        )
        
        # Apply settings
        if settings:
            job.metadata['settings'] = settings
        else:
            job.metadata['settings'] = self.default_settings
            
        # Add job metadata
        job.metadata.update({
            'timestamp': datetime.now().isoformat(),
            'user_agent': getattr(st, 'user_agent', 'unknown'),
            'session_id': getattr(st.session_state, 'session_id', 'unknown')
        })
        
        self.jobs[job.id] = job
        self.job_queue.append(job.id)
        
        logger.info(f"Created export job {job.id} for format {format.value}")
        
        # Start processing if under limit
        self._process_queue()
        
        return job.id
    
    def _process_queue(self):
        """Process pending jobs in the queue"""
        if len(self.active_jobs) >= self.max_concurrent_jobs:
            return
            
        if not self.job_queue:
            return
            
        job_id = self.job_queue.pop(0)
        job = self.jobs.get(job_id)
        
        if not job or job.status != ExportStatus.PENDING:
            return
            
        # Start job in background thread
        thread = threading.Thread(target=self._execute_job, args=(job_id,))
        thread.daemon = True
        thread.start()
        
        self.active_jobs[job_id] = thread
        
        # Continue processing queue
        self._process_queue()
    
    def _execute_job(self, job_id: str):
        """Execute an export job"""
        job = self.jobs.get(job_id)
        if not job:
            return
            
        try:
            job.status = ExportStatus.IN_PROGRESS
            job.started_at = datetime.now()
            job.progress = 0.1
            
            logger.info(f"Starting export job {job_id}")
            
            # Get appropriate exporter
            exporter = self.exporters.get(job.format)
            if not exporter:
                raise ValueError(f"No exporter available for format {job.format}")
            
            # Update progress
            job.progress = 0.2
            
            # Execute export
            file_path = exporter.export(
                data=job.data,
                persona=job.persona,
                view=job.view,
                settings=job.metadata.get('settings', self.default_settings),
                progress_callback=lambda p: setattr(job, 'progress', 0.2 + (p * 0.7)),
                **job.options
            )
            
            # Complete job
            job.file_path = str(file_path)
            job.file_size = file_path.stat().st_size if file_path.exists() else 0
            job.status = ExportStatus.COMPLETED
            job.completed_at = datetime.now()
            job.progress = 1.0
            
            logger.info(f"Completed export job {job_id}: {file_path}")
            
        except Exception as e:
            job.status = ExportStatus.FAILED
            job.error_message = str(e)
            job.completed_at = datetime.now()
            logger.error(f"Failed export job {job_id}: {e}")
            
        finally:
            # Remove from active jobs
            if job_id in self.active_jobs:
                del self.active_jobs[job_id]
            
            # Process next job in queue
            self._process_queue()
    
    def get_job_status(self, job_id: str) -> Optional[ExportJob]:
        """Get status of an export job"""
        return self.jobs.get(job_id)
    
    def get_all_jobs(self) -> List[ExportJob]:
        """Get all export jobs"""
        return list(self.jobs.values())
    
    def get_recent_jobs(self, hours: int = 24) -> List[ExportJob]:
        """Get recent export jobs"""
        cutoff = datetime.now() - timedelta(hours=hours)
        return [job for job in self.jobs.values() if job.created_at >= cutoff]
    
    def cancel_job(self, job_id: str) -> bool:
        """Cancel an export job"""
        job = self.jobs.get(job_id)
        if not job:
            return False
            
        if job.status in [ExportStatus.COMPLETED, ExportStatus.FAILED]:
            return False
            
        job.status = ExportStatus.CANCELLED
        job.completed_at = datetime.now()
        
        # Remove from queue
        if job_id in self.job_queue:
            self.job_queue.remove(job_id)
            
        # Stop active thread (best effort)
        if job_id in self.active_jobs:
            # Note: Python threads can't be forcibly stopped
            # The export process should check job status periodically
            pass
            
        logger.info(f"Cancelled export job {job_id}")
        return True
    
    def cleanup_old_jobs(self, days: int = 7):
        """Clean up old completed jobs and files"""
        cutoff = datetime.now() - timedelta(days=days)
        
        jobs_to_remove = []
        for job_id, job in self.jobs.items():
            if (job.completed_at and job.completed_at < cutoff and 
                job.status in [ExportStatus.COMPLETED, ExportStatus.FAILED]):
                
                # Remove file if it exists
                if job.file_path and os.path.exists(job.file_path):
                    try:
                        os.remove(job.file_path)
                        logger.info(f"Removed old export file: {job.file_path}")
                    except Exception as e:
                        logger.warning(f"Failed to remove file {job.file_path}: {e}")
                
                jobs_to_remove.append(job_id)
        
        # Remove jobs from memory
        for job_id in jobs_to_remove:
            del self.jobs[job_id]
            
        logger.info(f"Cleaned up {len(jobs_to_remove)} old export jobs")
    
    def get_export_statistics(self) -> Dict[str, Any]:
        """Get export system statistics"""
        total_jobs = len(self.jobs)
        if total_jobs == 0:
            return {
                'total_jobs': 0,
                'success_rate': 0,
                'avg_processing_time': 0,
                'format_distribution': {},
                'persona_distribution': {}
            }
        
        completed_jobs = [j for j in self.jobs.values() if j.status == ExportStatus.COMPLETED]
        failed_jobs = [j for j in self.jobs.values() if j.status == ExportStatus.FAILED]
        
        # Calculate processing times
        processing_times = []
        for job in completed_jobs:
            if job.started_at and job.completed_at:
                processing_times.append(
                    (job.completed_at - job.started_at).total_seconds()
                )
        
        # Format distribution
        format_dist = {}
        for job in self.jobs.values():
            fmt = job.format.value
            format_dist[fmt] = format_dist.get(fmt, 0) + 1
        
        # Persona distribution
        persona_dist = {}
        for job in self.jobs.values():
            persona = job.persona or 'General'
            persona_dist[persona] = persona_dist.get(persona, 0) + 1
        
        return {
            'total_jobs': total_jobs,
            'completed_jobs': len(completed_jobs),
            'failed_jobs': len(failed_jobs),
            'pending_jobs': len([j for j in self.jobs.values() if j.status == ExportStatus.PENDING]),
            'active_jobs': len(self.active_jobs),
            'success_rate': len(completed_jobs) / total_jobs if total_jobs > 0 else 0,
            'avg_processing_time': sum(processing_times) / len(processing_times) if processing_times else 0,
            'format_distribution': format_dist,
            'persona_distribution': persona_dist,
            'total_file_size': sum(job.file_size or 0 for job in completed_jobs)
        }


# Global export manager instance
_export_manager = None

def get_export_manager() -> ExportManager:
    """Get the global export manager instance"""
    global _export_manager
    if _export_manager is None:
        _export_manager = ExportManager()
    return _export_manager