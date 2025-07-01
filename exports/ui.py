"""
Export Management UI for AI Adoption Dashboard

User-friendly interface for export configuration, queue management,
progress tracking, and quality assurance.
"""

import os
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Callable
from pathlib import Path
import logging

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

from .core import ExportManager, ExportFormat, ExportStatus, ExportSettings, get_export_manager
from .validation import ExportValidator, ValidationResult
from .templates import TemplateManager

logger = logging.getLogger(__name__)


class ExportUI:
    """
    Streamlit-based export management interface
    
    Features:
    - Export format selection and configuration
    - Real-time progress tracking
    - Export queue management
    - Quality assurance dashboard
    - Download management
    - Export history and statistics
    """
    
    def __init__(self):
        self.export_manager = get_export_manager()
        self.validator = ExportValidator()
        self.template_manager = TemplateManager()
        
        # Initialize session state
        if 'export_ui_state' not in st.session_state:
            st.session_state.export_ui_state = {
                'selected_formats': [],
                'current_settings': ExportSettings(),
                'active_jobs': {},
                'last_refresh': datetime.now()
            }
    
    def render_export_interface(self, data: Dict[str, Any], persona: Optional[str] = None, view: Optional[str] = None):
        """Render the main export interface"""
        
        st.title("📤 Export Management Center")
        st.markdown("Generate professional reports and data exports for enterprise presentations and analysis.")
        
        # Create tabs for different sections
        tab1, tab2, tab3, tab4 = st.tabs(["🎯 Quick Export", "⚙️ Advanced Settings", "📊 Queue & Progress", "📈 Statistics"])
        
        with tab1:
            self._render_quick_export(data, persona, view)
        
        with tab2:
            self._render_advanced_settings(data, persona, view)
        
        with tab3:
            self._render_queue_management()
        
        with tab4:
            self._render_statistics_dashboard()
    
    def _render_quick_export(self, data: Dict[str, Any], persona: Optional[str], view: Optional[str]):
        """Render quick export interface"""
        st.header("Quick Export")
        st.markdown("Generate exports with default settings for immediate use.")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Format selection
            st.subheader("Select Export Formats")
            
            format_options = {
                "📄 PDF Report": ExportFormat.PDF,
                "📊 PowerPoint Presentation": ExportFormat.POWERPOINT,
                "📋 Excel Workbook": ExportFormat.EXCEL,
                "🌐 Interactive HTML": ExportFormat.INTERACTIVE_HTML,
                "📊 PNG Dashboard": ExportFormat.PNG,
                "📁 JSON Data": ExportFormat.JSON,
                "📄 CSV Data Package": ExportFormat.CSV
            }
            
            selected_formats = []
            
            # Create checkboxes for each format
            for display_name, export_format in format_options.items():
                if st.checkbox(display_name, key=f"quick_{export_format.value}"):
                    selected_formats.append(export_format)
            
            # Persona-specific recommendations
            if persona:
                st.info(f"💡 **Recommended for {persona}:** {self._get_persona_recommendations(persona)}")
        
        with col2:
            # Export preview and controls
            st.subheader("Export Preview")
            
            if selected_formats:
                st.success(f"✅ {len(selected_formats)} format(s) selected")
                
                # Show estimated file sizes
                estimated_sizes = self._estimate_export_sizes(selected_formats, data)
                for fmt, size in estimated_sizes.items():
                    st.text(f"{fmt.value.upper()}: ~{size}")
                
                # Export button
                if st.button("🚀 Generate Exports", type="primary", use_container_width=True):
                    self._start_quick_exports(selected_formats, data, persona, view)
            else:
                st.warning("Please select at least one export format")
                
            # Recent exports
            self._render_recent_exports_sidebar()
    
    def _render_advanced_settings(self, data: Dict[str, Any], persona: Optional[str], view: Optional[str]):
        """Render advanced export settings interface"""
        st.header("Advanced Export Configuration")
        
        # Settings categories
        tab1, tab2, tab3, tab4 = st.tabs(["🎨 Branding", "📐 Layout", "📊 Content", "🔧 Technical"])
        
        with tab1:
            self._render_branding_settings()
        
        with tab2:
            self._render_layout_settings()
        
        with tab3:
            self._render_content_settings(data, persona)
        
        with tab4:
            self._render_technical_settings()
        
        # Action buttons
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("💾 Save Settings", use_container_width=True):
                self._save_current_settings()
                st.success("Settings saved!")
        
        with col2:
            if st.button("🔄 Reset to Defaults", use_container_width=True):
                st.session_state.export_ui_state['current_settings'] = ExportSettings()
                st.success("Settings reset to defaults!")
                st.rerun()
        
        with col3:
            if st.button("📤 Export with Settings", type="primary", use_container_width=True):
                self._show_format_selection_modal(data, persona, view)
    
    def _render_branding_settings(self):
        """Render branding configuration"""
        st.subheader("Branding & Identity")
        
        settings = st.session_state.export_ui_state['current_settings']
        
        col1, col2 = st.columns(2)
        
        with col1:
            settings.company_name = st.text_input(
                "Company Name",
                value=settings.company_name,
                help="Company name to appear in headers and footers"
            )
            
            settings.author = st.text_input(
                "Report Author",
                value=settings.author,
                help="Author name for report attribution"
            )
            
            # Color scheme
            st.markdown("**Color Scheme**")
            settings.brand_colors['primary'] = st.color_picker(
                "Primary Color",
                value=settings.brand_colors['primary'],
                help="Main brand color for headers and emphasis"
            )
            
            settings.brand_colors['secondary'] = st.color_picker(
                "Secondary Color",
                value=settings.brand_colors['secondary'],
                help="Secondary color for accents and highlights"
            )
        
        with col2:
            # Logo upload
            st.markdown("**Logo & Watermark**")
            
            uploaded_logo = st.file_uploader(
                "Company Logo",
                type=['png', 'jpg', 'jpeg', 'svg'],
                help="Upload company logo for report headers"
            )
            
            if uploaded_logo:
                st.image(uploaded_logo, width=200)
                # In a real implementation, you'd save this file
                settings.company_logo = uploaded_logo.name
            
            # Watermark
            watermark_text = st.text_input(
                "Watermark Text (optional)",
                value=settings.watermark or "",
                help="Text watermark for document security"
            )
            
            if watermark_text:
                settings.watermark = watermark_text
            
            # Additional colors
            settings.brand_colors['accent'] = st.color_picker(
                "Accent Color",
                value=settings.brand_colors['accent'],
                help="Accent color for charts and highlights"
            )
            
            settings.brand_colors['text'] = st.color_picker(
                "Text Color",
                value=settings.brand_colors['text'],
                help="Primary text color"
            )
    
    def _render_layout_settings(self):
        """Render layout configuration"""
        st.subheader("Page Layout & Formatting")
        
        settings = st.session_state.export_ui_state['current_settings']
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Page Setup**")
            
            settings.page_size = st.selectbox(
                "Page Size",
                options=["A4", "Letter", "Legal"],
                index=["A4", "Letter", "Legal"].index(settings.page_size),
                help="Standard page sizes for printed documents"
            )
            
            settings.page_orientation = st.selectbox(
                "Orientation",
                options=["portrait", "landscape"],
                index=["portrait", "landscape"].index(settings.page_orientation),
                help="Page orientation for layout"
            )
            
            st.markdown("**Margins (inches)**")
            col_top, col_bottom = st.columns(2)
            with col_top:
                settings.margins['top'] = st.number_input(
                    "Top", min_value=0.5, max_value=2.0, value=settings.margins['top'], step=0.1
                )
            with col_bottom:
                settings.margins['bottom'] = st.number_input(
                    "Bottom", min_value=0.5, max_value=2.0, value=settings.margins['bottom'], step=0.1
                )
            
            col_left, col_right = st.columns(2)
            with col_left:
                settings.margins['left'] = st.number_input(
                    "Left", min_value=0.5, max_value=2.0, value=settings.margins['left'], step=0.1
                )
            with col_right:
                settings.margins['right'] = st.number_input(
                    "Right", min_value=0.5, max_value=2.0, value=settings.margins['right'], step=0.1
                )
        
        with col2:
            st.markdown("**Image Quality**")
            
            settings.image_dpi = st.slider(
                "Image DPI",
                min_value=72, max_value=600, value=settings.image_dpi, step=24,
                help="Higher DPI for better print quality (recommended: 300 for print)"
            )
            
            col_w, col_h = st.columns(2)
            with col_w:
                settings.chart_width = st.number_input(
                    "Chart Width (px)", min_value=400, max_value=2400, 
                    value=settings.chart_width, step=100
                )
            with col_h:
                settings.chart_height = st.number_input(
                    "Chart Height (px)", min_value=300, max_value=1800, 
                    value=settings.chart_height, step=50
                )
            
            settings.compress_images = st.checkbox(
                "Compress Images",
                value=settings.compress_images,
                help="Reduce file size by compressing images"
            )
            
            # Preview
            if st.button("📋 Preview Layout"):
                self._show_layout_preview(settings)
    
    def _render_content_settings(self, data: Dict[str, Any], persona: Optional[str]):
        """Render content configuration"""
        st.subheader("Content & Structure")
        
        settings = st.session_state.export_ui_state['current_settings']
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Report Sections**")
            
            settings.include_cover_page = st.checkbox(
                "Cover Page",
                value=settings.include_cover_page,
                help="Professional cover page with title and metadata"
            )
            
            settings.include_executive_summary = st.checkbox(
                "Executive Summary",
                value=settings.include_executive_summary,
                help="High-level summary of key findings"
            )
            
            settings.include_table_of_contents = st.checkbox(
                "Table of Contents",
                value=settings.include_table_of_contents,
                help="Navigation aid for multi-page reports"
            )
            
            settings.include_methodology = st.checkbox(
                "Methodology Section",
                value=settings.include_methodology,
                help="Data sources and analytical approach"
            )
            
            settings.include_appendix = st.checkbox(
                "Appendix",
                value=settings.include_appendix,
                help="Additional data and references"
            )
        
        with col2:
            st.markdown("**Content Focus**")
            
            # Persona-specific content suggestions
            if persona:
                persona_insights = self.template_manager.get_persona_insights(persona)
                st.info(f"**{persona} Focus Areas:**")
                for insight in persona_insights[:3]:
                    st.text(f"• {insight}")
            
            # Custom keywords for focus
            custom_keywords = st.text_area(
                "Custom Focus Keywords",
                help="Keywords to emphasize in content generation",
                placeholder="e.g., ROI, competitive advantage, efficiency"
            )
            
            if custom_keywords:
                settings.keywords = [kw.strip() for kw in custom_keywords.split(',')]
            
            # Data filtering
            st.markdown("**Data Inclusion**")
            available_datasets = list(data.keys()) if data else []
            
            selected_datasets = st.multiselect(
                "Include Datasets",
                options=available_datasets,
                default=available_datasets,
                help="Select which datasets to include in exports"
            )
    
    def _render_technical_settings(self):
        """Render technical configuration"""
        st.subheader("Technical Settings")
        
        settings = st.session_state.export_ui_state['current_settings']
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Security & Access**")
            
            settings.password_protect = st.checkbox(
                "Password Protection",
                value=settings.password_protect,
                help="Add password protection to PDF exports"
            )
            
            if settings.password_protect:
                password = st.text_input(
                    "Password",
                    type="password",
                    help="Password for protected documents"
                )
                if password:
                    settings.password = password
            
            # Metadata
            st.markdown("**Metadata**")
            
            settings.subject = st.text_input(
                "Document Subject",
                value=settings.subject,
                help="Document subject for metadata"
            )
            
            keywords_text = st.text_input(
                "Keywords (comma-separated)",
                value=", ".join(settings.keywords),
                help="Keywords for document indexing"
            )
            
            if keywords_text:
                settings.keywords = [kw.strip() for kw in keywords_text.split(',')]
        
        with col2:
            st.markdown("**Performance**")
            
            # Export quality vs speed tradeoff
            quality_level = st.select_slider(
                "Quality vs Speed",
                options=["Fast", "Balanced", "High Quality"],
                value="Balanced",
                help="Balance between export speed and output quality"
            )
            
            # Concurrent exports
            max_concurrent = st.slider(
                "Max Concurrent Exports",
                min_value=1, max_value=5, value=3,
                help="Maximum number of simultaneous export jobs"
            )
            
            # Cleanup settings
            cleanup_days = st.number_input(
                "Auto-cleanup After (days)",
                min_value=1, max_value=30, value=7,
                help="Automatically remove old exports after specified days"
            )
            
            if st.button("🧹 Clean Old Exports Now"):
                self.export_manager.cleanup_old_jobs(cleanup_days)
                st.success(f"Cleaned exports older than {cleanup_days} days")
    
    def _render_queue_management(self):
        """Render export queue and progress tracking"""
        st.header("Export Queue & Progress")
        
        # Auto-refresh toggle
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            auto_refresh = st.checkbox("Auto-refresh every 5 seconds", value=True)
        
        with col2:
            if st.button("🔄 Refresh Now"):
                st.rerun()
        
        with col3:
            if st.button("🗑️ Clear Completed"):
                self._clear_completed_jobs()
                st.rerun()
        
        # Auto-refresh logic
        if auto_refresh:
            import time
            time.sleep(0.1)  # Small delay for UI responsiveness
            if datetime.now() - st.session_state.export_ui_state['last_refresh'] > timedelta(seconds=5):
                st.session_state.export_ui_state['last_refresh'] = datetime.now()
                st.rerun()
        
        # Current queue
        jobs = self.export_manager.get_all_jobs()
        
        if not jobs:
            st.info("No export jobs in queue")
            return
        
        # Filter jobs
        filter_options = ["All", "Pending", "In Progress", "Completed", "Failed"]
        selected_filter = st.selectbox("Filter Jobs", options=filter_options)
        
        if selected_filter != "All":
            status_map = {
                "Pending": ExportStatus.PENDING,
                "In Progress": ExportStatus.IN_PROGRESS,
                "Completed": ExportStatus.COMPLETED,
                "Failed": ExportStatus.FAILED
            }
            jobs = [job for job in jobs if job.status == status_map[selected_filter]]
        
        # Jobs table
        if jobs:
            self._render_jobs_table(jobs)
        else:
            st.info(f"No {selected_filter.lower()} jobs found")
        
        # Progress visualization
        if any(job.status == ExportStatus.IN_PROGRESS for job in jobs):
            st.subheader("Active Jobs Progress")
            active_jobs = [job for job in jobs if job.status == ExportStatus.IN_PROGRESS]
            
            for job in active_jobs:
                self._render_job_progress(job)
    
    def _render_statistics_dashboard(self):
        """Render export statistics and analytics"""
        st.header("Export Analytics & Statistics")
        
        # Get statistics
        stats = self.export_manager.get_export_statistics()
        
        # Key metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "Total Exports",
                stats['total_jobs'],
                delta=None
            )
        
        with col2:
            st.metric(
                "Success Rate",
                f"{stats['success_rate']:.1%}",
                delta=None
            )
        
        with col3:
            st.metric(
                "Avg Processing Time",
                f"{stats['avg_processing_time']:.1f}s",
                delta=None
            )
        
        with col4:
            st.metric(
                "Total File Size",
                self._format_file_size(stats['total_file_size']),
                delta=None
            )
        
        # Charts
        col1, col2 = st.columns(2)
        
        with col1:
            # Format distribution
            if stats['format_distribution']:
                fig = px.pie(
                    values=list(stats['format_distribution'].values()),
                    names=list(stats['format_distribution'].keys()),
                    title="Export Format Distribution"
                )
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Persona distribution
            if stats['persona_distribution']:
                fig = px.bar(
                    x=list(stats['persona_distribution'].keys()),
                    y=list(stats['persona_distribution'].values()),
                    title="Export by Persona"
                )
                st.plotly_chart(fig, use_container_width=True)
        
        # Recent activity timeline
        st.subheader("Recent Export Activity")
        recent_jobs = self.export_manager.get_recent_jobs(hours=24)
        
        if recent_jobs:
            # Create timeline data
            timeline_data = []
            for job in recent_jobs:
                timeline_data.append({
                    'time': job.created_at,
                    'format': job.format.value,
                    'status': job.status.name,
                    'persona': job.persona or 'General'
                })
            
            df = pd.DataFrame(timeline_data)
            
            # Timeline chart
            fig = px.scatter(
                df, x='time', y='format',
                color='status', size=[1]*len(df),
                title="Export Timeline (Last 24 Hours)",
                hover_data=['persona']
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No recent export activity")
    
    def _render_jobs_table(self, jobs: List):
        """Render jobs in a table format"""
        # Prepare table data
        table_data = []
        
        for job in jobs:
            # Status emoji
            status_emoji = {
                ExportStatus.PENDING: "⏳",
                ExportStatus.IN_PROGRESS: "🔄",
                ExportStatus.COMPLETED: "✅",
                ExportStatus.FAILED: "❌",
                ExportStatus.CANCELLED: "🚫"
            }
            
            # Duration calculation
            if job.started_at and job.completed_at:
                duration = (job.completed_at - job.started_at).total_seconds()
                duration_str = f"{duration:.1f}s"
            elif job.started_at:
                duration = (datetime.now() - job.started_at).total_seconds()
                duration_str = f"{duration:.1f}s (ongoing)"
            else:
                duration_str = "-"
            
            # File size
            file_size = self._format_file_size(job.file_size) if job.file_size else "-"
            
            table_data.append({
                "Status": f"{status_emoji[job.status]} {job.status.name}",
                "Format": job.format.value.upper(),
                "Persona": job.persona or "General",
                "Created": job.created_at.strftime("%H:%M:%S"),
                "Duration": duration_str,
                "File Size": file_size,
                "Progress": f"{job.progress:.0%}" if job.progress else "-",
                "Actions": job.id  # We'll use this for action buttons
            })
        
        if table_data:
            df = pd.DataFrame(table_data)
            st.dataframe(df.drop(columns=['Actions']), use_container_width=True)
            
            # Action buttons for each job
            for i, job in enumerate(jobs):
                col1, col2, col3 = st.columns([3, 1, 1])
                
                with col1:
                    if job.error_message:
                        st.error(f"Error: {job.error_message}")
                
                with col2:
                    if job.status == ExportStatus.COMPLETED and job.file_path:
                        if st.button("📥 Download", key=f"download_{job.id}"):
                            self._handle_download(job)
                
                with col3:
                    if job.status in [ExportStatus.PENDING, ExportStatus.IN_PROGRESS]:
                        if st.button("🛑 Cancel", key=f"cancel_{job.id}"):
                            self.export_manager.cancel_job(job.id)
                            st.success("Job cancelled")
                            st.rerun()
    
    def _render_job_progress(self, job):
        """Render individual job progress"""
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.write(f"**{job.format.value.upper()}** - {job.persona or 'General'}")
            progress_bar = st.progress(job.progress)
            
        with col2:
            st.metric("Progress", f"{job.progress:.0%}")
        
        # Estimated time remaining
        if job.started_at and job.progress > 0.1:
            elapsed = (datetime.now() - job.started_at).total_seconds()
            estimated_total = elapsed / job.progress
            remaining = max(0, estimated_total - elapsed)
            st.text(f"⏱️ Est. {remaining:.0f}s remaining")
    
    def _start_quick_exports(self, formats: List[ExportFormat], data: Dict[str, Any], persona: Optional[str], view: Optional[str]):
        """Start multiple export jobs with default settings"""
        settings = st.session_state.export_ui_state['current_settings']
        
        job_ids = []
        for format in formats:
            try:
                job_id = self.export_manager.create_export_job(
                    format=format,
                    persona=persona,
                    view=view,
                    data=data,
                    settings=settings
                )
                job_ids.append(job_id)
            except Exception as e:
                st.error(f"Failed to create {format.value} export job: {str(e)}")
        
        if job_ids:
            st.success(f"✅ Started {len(job_ids)} export job(s)")
            st.info("💡 Check the 'Queue & Progress' tab to monitor your exports")
            
            # Store active job IDs for tracking
            st.session_state.export_ui_state['active_jobs'].update({
                job_id: datetime.now() for job_id in job_ids
            })
    
    def _show_format_selection_modal(self, data: Dict[str, Any], persona: Optional[str], view: Optional[str]):
        """Show format selection for advanced export"""
        st.subheader("Select Export Formats")
        
        format_options = {
            "📄 PDF Report": ExportFormat.PDF,
            "📊 PowerPoint Presentation": ExportFormat.POWERPOINT,
            "📋 Excel Workbook": ExportFormat.EXCEL,
            "🌐 Interactive HTML": ExportFormat.INTERACTIVE_HTML,
            "🌐 Static HTML": ExportFormat.HTML,
            "📊 PNG Dashboard": ExportFormat.PNG,
            "🎨 SVG Graphics": ExportFormat.SVG,
            "📁 JSON Data": ExportFormat.JSON,
            "📁 XML Data": ExportFormat.XML,
            "📄 CSV Data Package": ExportFormat.CSV
        }
        
        selected_formats = []
        
        col1, col2 = st.columns(2)
        format_items = list(format_options.items())
        
        with col1:
            for i in range(0, len(format_items), 2):
                display_name, export_format = format_items[i]
                if st.checkbox(display_name, key=f"adv_{export_format.value}"):
                    selected_formats.append(export_format)
        
        with col2:
            for i in range(1, len(format_items), 2):
                if i < len(format_items):
                    display_name, export_format = format_items[i]
                    if st.checkbox(display_name, key=f"adv_{export_format.value}"):
                        selected_formats.append(export_format)
        
        if selected_formats:
            if st.button("🚀 Generate Advanced Exports", type="primary", use_container_width=True):
                self._start_quick_exports(selected_formats, data, persona, view)
    
    def _get_persona_recommendations(self, persona: str) -> str:
        """Get format recommendations for persona"""
        recommendations = {
            "Business Leader": "PDF Report, PowerPoint Presentation, Excel Workbook",
            "Policymaker": "PDF Report, Interactive HTML, PNG Dashboard",
            "Researcher": "PDF Report, JSON Data, CSV Data Package, Excel Workbook"
        }
        return recommendations.get(persona, "PDF Report, Interactive HTML, JSON Data")
    
    def _estimate_export_sizes(self, formats: List[ExportFormat], data: Dict[str, Any]) -> Dict[ExportFormat, str]:
        """Estimate file sizes for selected formats"""
        # Basic size estimation based on data and format
        base_size = len(str(data)) if data else 1000
        
        multipliers = {
            ExportFormat.PDF: 5,
            ExportFormat.POWERPOINT: 8,
            ExportFormat.EXCEL: 3,
            ExportFormat.JSON: 1,
            ExportFormat.XML: 1.5,
            ExportFormat.CSV: 0.5,
            ExportFormat.HTML: 2,
            ExportFormat.INTERACTIVE_HTML: 4,
            ExportFormat.PNG: 10,
            ExportFormat.SVG: 2
        }
        
        estimates = {}
        for fmt in formats:
            size_bytes = base_size * multipliers.get(fmt, 1)
            estimates[fmt] = self._format_file_size(size_bytes)
        
        return estimates
    
    def _format_file_size(self, size_bytes: int) -> str:
        """Format file size for display"""
        if size_bytes < 1024:
            return f"{size_bytes} B"
        elif size_bytes < 1024 * 1024:
            return f"{size_bytes / 1024:.1f} KB"
        elif size_bytes < 1024 * 1024 * 1024:
            return f"{size_bytes / (1024 * 1024):.1f} MB"
        else:
            return f"{size_bytes / (1024 * 1024 * 1024):.1f} GB"
    
    def _save_current_settings(self):
        """Save current settings to session state"""
        # In a production environment, you might save to a database or file
        st.session_state.export_ui_state['saved_settings'] = st.session_state.export_ui_state['current_settings']
    
    def _show_layout_preview(self, settings: ExportSettings):
        """Show a preview of the layout settings"""
        st.subheader("Layout Preview")
        
        # Create a visual representation of the layout
        preview_html = f"""
        <div style="
            border: 2px solid {settings.brand_colors['primary']};
            padding: 20px;
            background: {settings.brand_colors['background']};
            font-family: Arial, sans-serif;
            max-width: 400px;
        ">
            <div style="
                background: {settings.brand_colors['primary']};
                color: white;
                padding: 10px;
                margin: -{settings.margins['top']*20}px -{settings.margins['left']*20}px 10px -{settings.margins['right']*20}px;
                text-align: center;
            ">
                <h3 style="margin: 0;">{settings.company_name}</h3>
                <p style="margin: 5px 0;">AI Adoption Dashboard</p>
            </div>
            <div style="padding: 10px 0;">
                <h4 style="color: {settings.brand_colors['primary']};">Sample Content</h4>
                <p style="color: {settings.brand_colors['text']};">This is how your content will appear...</p>
                <div style="
                    background: {settings.brand_colors['accent']};
                    padding: 5px;
                    margin: 10px 0;
                    color: white;
                ">
                    Chart Area ({settings.chart_width}x{settings.chart_height}px)
                </div>
            </div>
            <div style="
                border-top: 1px solid {settings.brand_colors['primary']};
                padding-top: 5px;
                margin-top: 10px;
                font-size: 12px;
                color: {settings.brand_colors['text']};
                text-align: center;
            ">
                Page: {settings.page_size} | DPI: {settings.image_dpi}
            </div>
        </div>
        """
        
        st.markdown(preview_html, unsafe_allow_html=True)
    
    def _clear_completed_jobs(self):
        """Clear completed and failed jobs from queue"""
        jobs = self.export_manager.get_all_jobs()
        cleared_count = 0
        
        for job in jobs:
            if job.status in [ExportStatus.COMPLETED, ExportStatus.FAILED, ExportStatus.CANCELLED]:
                if job.id in self.export_manager.jobs:
                    del self.export_manager.jobs[job.id]
                    cleared_count += 1
        
        st.success(f"Cleared {cleared_count} completed jobs")
    
    def _handle_download(self, job):
        """Handle file download for completed job"""
        if job.file_path and os.path.exists(job.file_path):
            # In Streamlit, you would typically use st.download_button
            # Here we show the download information
            st.success(f"File ready: {os.path.basename(job.file_path)}")
            st.info(f"File size: {self._format_file_size(job.file_size or 0)}")
            st.info(f"Location: {job.file_path}")
        else:
            st.error("File not found or has been removed")
    
    def _render_recent_exports_sidebar(self):
        """Render recent exports in sidebar"""
        st.markdown("**Recent Exports**")
        
        recent_jobs = self.export_manager.get_recent_jobs(hours=2)
        completed_jobs = [job for job in recent_jobs if job.status == ExportStatus.COMPLETED]
        
        if completed_jobs:
            for job in completed_jobs[:5]:  # Show last 5
                status_emoji = "✅"
                time_str = job.completed_at.strftime("%H:%M") if job.completed_at else ""
                
                st.text(f"{status_emoji} {job.format.value.upper()} {time_str}")
                
                if job.file_path and os.path.exists(job.file_path):
                    if st.button(f"📥", key=f"sidebar_download_{job.id}"):
                        self._handle_download(job)
        else:
            st.text("No recent exports")


def render_export_ui(data: Dict[str, Any], persona: Optional[str] = None, view: Optional[str] = None):
    """Convenience function to render the export UI"""
    export_ui = ExportUI()
    export_ui.render_export_interface(data, persona, view)