"""Export functionality for AI Adoption Dashboard.

This module provides export capabilities for various data formats
including Excel, CSV, and PDF.
"""

import io
import json
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional, Union
import pandas as pd
import numpy as np
from pathlib import Path

# For Excel formatting
try:
    import xlsxwriter
    XLSX_AVAILABLE = True
except ImportError:
    XLSX_AVAILABLE = False
    
# For PDF generation
try:
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, Image
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.lib.enums import TA_CENTER, TA_RIGHT
    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False

# For charts in PDF
try:
    import matplotlib.pyplot as plt
    import matplotlib
    matplotlib.use('Agg')  # Non-interactive backend
    CHARTS_AVAILABLE = True
except ImportError:
    CHARTS_AVAILABLE = False

logger = logging.getLogger(__name__)


class ExportManager:
    """Manages data export functionality."""
    
    def __init__(self):
        """Initialize export manager."""
        self.supported_formats = ['csv', 'json']
        if XLSX_AVAILABLE:
            self.supported_formats.append('excel')
        if PDF_AVAILABLE:
            self.supported_formats.append('pdf')
            
    def export_financial_results(
        self,
        results: Dict[str, Any],
        format: str,
        filename: Optional[str] = None
    ) -> Union[str, bytes, io.BytesIO]:
        """Export financial calculation results.
        
        Args:
            results: Financial calculation results
            format: Export format (csv, excel, pdf, json)
            filename: Optional filename (returns bytes if None)
            
        Returns:
            File path if filename provided, otherwise bytes/BytesIO
        """
        if format not in self.supported_formats:
            raise ValueError(f"Unsupported format: {format}. Supported: {self.supported_formats}")
            
        if format == 'csv':
            return self._export_financial_csv(results, filename)
        elif format == 'excel':
            return self._export_financial_excel(results, filename)
        elif format == 'pdf':
            return self._export_financial_pdf(results, filename)
        elif format == 'json':
            return self._export_financial_json(results, filename)
            
    def _export_financial_csv(self, results: Dict, filename: Optional[str]) -> Union[str, str]:
        """Export financial results to CSV."""
        # Flatten nested results
        rows = []
        
        # Add metadata
        rows.append(['AI Investment Analysis Report'])
        rows.append(['Generated', datetime.now().strftime('%Y-%m-%d %H:%M:%S')])
        rows.append([])  # Empty row
        
        # Financial metrics
        if 'financial_metrics' in results:
            rows.append(['Financial Metrics'])
            metrics = results['financial_metrics']
            for key, value in metrics.items():
                if value is not None:
                    rows.append([key.replace('_', ' ').title(), f"{value:,.2f}" if isinstance(value, (int, float)) else str(value)])
            rows.append([])
            
        # TCO Analysis
        if 'tco_analysis' in results:
            rows.append(['Total Cost of Ownership'])
            tco = results['tco_analysis']
            for key, value in tco.items():
                if value is not None:
                    rows.append([key.replace('_', ' ').title(), f"{value:,.2f}" if isinstance(value, (int, float)) else str(value)])
            rows.append([])
            
        # Risk Analysis
        if 'risk_analysis' in results:
            rows.append(['Risk Analysis'])
            risk = results['risk_analysis']
            for key, value in risk.items():
                if value is not None and key != 'meets_threshold':
                    rows.append([key.replace('_', ' ').title(), f"{value:,.4f}" if isinstance(value, (int, float)) else str(value)])
            rows.append([])
            
        # Convert to DataFrame
        df = pd.DataFrame(rows)
        
        if filename:
            df.to_csv(filename, index=False, header=False)
            return filename
        else:
            return df.to_csv(index=False, header=False)
            
    def _export_financial_excel(self, results: Dict, filename: Optional[str]) -> Union[str, io.BytesIO]:
        """Export financial results to Excel with formatting."""
        if not XLSX_AVAILABLE:
            raise ImportError("xlsxwriter not available. Install with: pip install xlsxwriter")
            
        # Create BytesIO buffer if no filename
        if filename:
            workbook = xlsxwriter.Workbook(filename)
        else:
            output = io.BytesIO()
            workbook = xlsxwriter.Workbook(output)
            
        # Create worksheet
        worksheet = workbook.add_worksheet('AI Investment Analysis')
        
        # Define formats
        title_format = workbook.add_format({
            'bold': True,
            'font_size': 16,
            'align': 'center',
            'valign': 'vcenter',
            'bg_color': '#1E88E5',
            'font_color': 'white'
        })
        
        header_format = workbook.add_format({
            'bold': True,
            'font_size': 12,
            'bg_color': '#E3F2FD',
            'border': 1
        })
        
        metric_format = workbook.add_format({
            'num_format': '#,##0.00',
            'border': 1
        })
        
        percent_format = workbook.add_format({
            'num_format': '0.0%',
            'border': 1
        })
        
        currency_format = workbook.add_format({
            'num_format': '$#,##0',
            'border': 1
        })
        
        label_format = workbook.add_format({
            'bold': True,
            'border': 1,
            'bg_color': '#F5F5F5'
        })
        
        # Set column widths
        worksheet.set_column('A:A', 30)
        worksheet.set_column('B:B', 20)
        worksheet.set_column('C:D', 15)
        
        row = 0
        
        # Title
        worksheet.merge_range(row, 0, row, 3, 'AI Investment Analysis Report', title_format)
        row += 2
        
        # Metadata
        worksheet.write(row, 0, 'Generated:', label_format)
        worksheet.write(row, 1, datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        row += 2
        
        # Financial Metrics Section
        if 'financial_metrics' in results:
            worksheet.merge_range(row, 0, row, 3, 'Financial Metrics', header_format)
            row += 1
            
            metrics = results['financial_metrics']
            
            # NPV
            if 'npv' in metrics and metrics['npv'] is not None:
                worksheet.write(row, 0, 'Net Present Value (NPV)', label_format)
                worksheet.write(row, 1, metrics['npv'], currency_format)
                row += 1
                
            # IRR
            if 'irr' in metrics and metrics['irr'] is not None:
                worksheet.write(row, 0, 'Internal Rate of Return (IRR)', label_format)
                worksheet.write(row, 1, metrics['irr'], percent_format)
                row += 1
                
            # ROI
            if 'simple_roi_pct' in metrics:
                worksheet.write(row, 0, 'Simple ROI', label_format)
                worksheet.write(row, 1, metrics['simple_roi_pct'] / 100, percent_format)
                row += 1
                
            # Payback
            if 'payback_years' in metrics and metrics['payback_years'] is not None:
                worksheet.write(row, 0, 'Payback Period', label_format)
                worksheet.write(row, 1, f"{metrics['payback_years']:.1f} years", metric_format)
                row += 1
                
            row += 1  # Empty row
            
        # TCO Analysis Section
        if 'tco_analysis' in results:
            worksheet.merge_range(row, 0, row, 3, 'Total Cost of Ownership', header_format)
            row += 1
            
            tco = results['tco_analysis']
            
            worksheet.write(row, 0, 'Initial Cost', label_format)
            worksheet.write(row, 1, tco.get('initial_cost', 0), currency_format)
            row += 1
            
            worksheet.write(row, 0, 'Operating Costs (PV)', label_format)
            worksheet.write(row, 1, tco.get('operating_costs', 0), currency_format)
            row += 1
            
            worksheet.write(row, 0, 'Maintenance Costs (PV)', label_format)
            worksheet.write(row, 1, tco.get('maintenance_costs', 0), currency_format)
            row += 1
            
            worksheet.write(row, 0, 'Total TCO', label_format)
            worksheet.write(row, 1, tco.get('total_tco', 0), currency_format)
            row += 1
            
            row += 1  # Empty row
            
        # Risk Analysis Section
        if 'risk_analysis' in results:
            worksheet.merge_range(row, 0, row, 3, 'Risk Analysis', header_format)
            row += 1
            
            risk = results['risk_analysis']
            
            worksheet.write(row, 0, 'Expected Return', label_format)
            worksheet.write(row, 1, risk.get('expected_return', 0), percent_format)
            row += 1
            
            worksheet.write(row, 0, 'Risk-Adjusted Return', label_format)
            worksheet.write(row, 1, risk.get('risk_adjusted_return', 0), percent_format)
            row += 1
            
            worksheet.write(row, 0, 'Sharpe Ratio', label_format)
            worksheet.write(row, 1, risk.get('sharpe_ratio', 0), metric_format)
            row += 1
            
            worksheet.write(row, 0, 'Meets Risk Threshold', label_format)
            worksheet.write(row, 1, 'Yes' if risk.get('meets_threshold', False) else 'No')
            row += 1
            
        # Investment Decision
        if 'investment_decision' in results:
            row += 1
            worksheet.merge_range(row, 0, row, 3, 'Investment Decision', header_format)
            row += 1
            
            decision = results['investment_decision']
            
            recommendation = 'RECOMMENDED' if decision.get('recommended', False) else 'NOT RECOMMENDED'
            rec_format = workbook.add_format({
                'bold': True,
                'font_size': 14,
                'align': 'center',
                'bg_color': '#4CAF50' if decision.get('recommended', False) else '#F44336',
                'font_color': 'white'
            })
            
            worksheet.merge_range(row, 0, row, 3, recommendation, rec_format)
            
        # Close workbook
        workbook.close()
        
        if filename:
            return filename
        else:
            output.seek(0)
            return output
            
    def _export_financial_pdf(self, results: Dict, filename: Optional[str]) -> Union[str, io.BytesIO]:
        """Export financial results to PDF report."""
        if not PDF_AVAILABLE:
            raise ImportError("reportlab not available. Install with: pip install reportlab")
            
        # Create buffer if no filename
        if filename:
            buffer = filename
        else:
            buffer = io.BytesIO()
            
        # Create PDF document
        doc = SimpleDocTemplate(
            buffer,
            pagesize=letter,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=72
        )
        
        # Container for page elements
        elements = []
        
        # Styles
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Title'],
            fontSize=24,
            textColor=colors.HexColor('#1E88E5'),
            spaceAfter=30,
            alignment=TA_CENTER
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading1'],
            fontSize=16,
            textColor=colors.HexColor('#424242'),
            spaceAfter=12
        )
        
        # Title page
        elements.append(Paragraph('AI Investment Analysis Report', title_style))
        elements.append(Spacer(1, 0.5 * inch))
        elements.append(Paragraph(f'Generated: {datetime.now().strftime("%B %d, %Y")}', styles['Normal']))
        elements.append(PageBreak())
        
        # Executive Summary
        elements.append(Paragraph('Executive Summary', heading_style))
        
        if 'investment_decision' in results:
            decision = results['investment_decision']
            if decision.get('recommended', False):
                summary_text = "Based on comprehensive financial analysis, this AI investment is <b>RECOMMENDED</b>."
                elements.append(Paragraph(summary_text, styles['Normal']))
            else:
                summary_text = "Based on comprehensive financial analysis, this AI investment is <b>NOT RECOMMENDED</b>."
                elements.append(Paragraph(summary_text, styles['Normal']))
                
        elements.append(Spacer(1, 0.25 * inch))
        
        # Financial Metrics Table
        if 'financial_metrics' in results:
            elements.append(Paragraph('Financial Metrics', heading_style))
            
            metrics_data = [['Metric', 'Value']]
            metrics = results['financial_metrics']
            
            if 'npv' in metrics and metrics['npv'] is not None:
                metrics_data.append(['Net Present Value', f'${metrics["npv"]:,.0f}'])
            if 'irr' in metrics and metrics['irr'] is not None:
                metrics_data.append(['Internal Rate of Return', f'{metrics["irr"]*100:.1f}%'])
            if 'simple_roi_pct' in metrics:
                metrics_data.append(['Simple ROI', f'{metrics["simple_roi_pct"]:.1f}%'])
            if 'payback_years' in metrics and metrics['payback_years'] is not None:
                metrics_data.append(['Payback Period', f'{metrics["payback_years"]:.1f} years'])
                
            # Create table
            metrics_table = Table(metrics_data, colWidths=[3*inch, 2*inch])
            metrics_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#E3F2FD')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ]))
            
            elements.append(metrics_table)
            elements.append(Spacer(1, 0.5 * inch))
            
        # TCO Analysis
        if 'tco_analysis' in results:
            elements.append(Paragraph('Total Cost of Ownership', heading_style))
            
            tco = results['tco_analysis']
            tco_data = [['Cost Component', 'Amount']]
            tco_data.append(['Initial Investment', f'${tco.get("initial_cost", 0):,.0f}'])
            tco_data.append(['Operating Costs (PV)', f'${tco.get("operating_costs", 0):,.0f}'])
            tco_data.append(['Maintenance Costs (PV)', f'${tco.get("maintenance_costs", 0):,.0f}'])
            tco_data.append(['Total TCO', f'${tco.get("total_tco", 0):,.0f}'])
            
            tco_table = Table(tco_data, colWidths=[3*inch, 2*inch])
            tco_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#E3F2FD')),
                ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#FFEB3B')),
                ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ]))
            
            elements.append(tco_table)
            
        # Build PDF
        doc.build(elements)
        
        if not filename:
            buffer.seek(0)
            
        return buffer if not filename else filename
        
    def _export_financial_json(self, results: Dict, filename: Optional[str]) -> Union[str, str]:
        """Export financial results to JSON."""
        # Add metadata
        export_data = {
            'metadata': {
                'generated': datetime.now().isoformat(),
                'type': 'financial_analysis',
                'version': '1.0'
            },
            'results': results
        }
        
        if filename:
            with open(filename, 'w') as f:
                json.dump(export_data, f, indent=2, default=str)
            return filename
        else:
            return json.dumps(export_data, indent=2, default=str)
            
    def export_monte_carlo_results(
        self,
        results: Dict[str, Any],
        format: str,
        filename: Optional[str] = None,
        include_histogram: bool = True
    ) -> Union[str, bytes, io.BytesIO]:
        """Export Monte Carlo simulation results.
        
        Args:
            results: Monte Carlo simulation results
            format: Export format
            filename: Optional filename
            include_histogram: Include histogram chart (for PDF)
            
        Returns:
            File path or bytes
        """
        if format == 'csv':
            return self._export_monte_carlo_csv(results, filename)
        elif format == 'excel':
            return self._export_monte_carlo_excel(results, filename)
        elif format == 'pdf':
            return self._export_monte_carlo_pdf(results, filename, include_histogram)
        elif format == 'json':
            return json.dumps(results, indent=2, default=str)
            
    def _export_monte_carlo_csv(self, results: Dict, filename: Optional[str]) -> Union[str, str]:
        """Export Monte Carlo results to CSV."""
        rows = []
        
        # Summary statistics
        rows.append(['Monte Carlo Simulation Results'])
        rows.append(['Iterations', results.get('iterations', 0)])
        rows.append(['Mean', results.get('mean', 0)])
        rows.append(['Standard Deviation', results.get('std_dev', 0)])
        rows.append(['Minimum', results.get('min', 0)])
        rows.append(['Maximum', results.get('max', 0)])
        rows.append([])
        
        # Percentiles
        rows.append(['Percentiles'])
        percentiles = results.get('percentiles', {})
        for key, value in percentiles.items():
            rows.append([key, value])
            
        df = pd.DataFrame(rows)
        
        if filename:
            df.to_csv(filename, index=False, header=False)
            return filename
        else:
            return df.to_csv(index=False, header=False)
            
    def _export_monte_carlo_excel(self, results: Dict, filename: Optional[str]) -> Union[str, io.BytesIO]:
        """Export Monte Carlo results to Excel."""
        if not XLSX_AVAILABLE:
            raise ImportError("xlsxwriter not available")
            
        if filename:
            workbook = xlsxwriter.Workbook(filename)
        else:
            output = io.BytesIO()
            workbook = xlsxwriter.Workbook(output)
            
        worksheet = workbook.add_worksheet('Monte Carlo Results')
        
        # Formats
        header_format = workbook.add_format({
            'bold': True,
            'font_size': 14,
            'bg_color': '#1E88E5',
            'font_color': 'white'
        })
        
        label_format = workbook.add_format({'bold': True})
        number_format = workbook.add_format({'num_format': '#,##0.00'})
        
        # Write results
        row = 0
        worksheet.write(row, 0, 'Monte Carlo Simulation Results', header_format)
        row += 2
        
        # Summary stats
        worksheet.write(row, 0, 'Iterations:', label_format)
        worksheet.write(row, 1, results.get('iterations', 0))
        row += 1
        
        worksheet.write(row, 0, 'Mean:', label_format)
        worksheet.write(row, 1, results.get('mean', 0), number_format)
        row += 1
        
        worksheet.write(row, 0, 'Std Dev:', label_format)
        worksheet.write(row, 1, results.get('std_dev', 0), number_format)
        row += 1
        
        worksheet.write(row, 0, 'Min:', label_format)
        worksheet.write(row, 1, results.get('min', 0), number_format)
        row += 1
        
        worksheet.write(row, 0, 'Max:', label_format)
        worksheet.write(row, 1, results.get('max', 0), number_format)
        row += 2
        
        # Percentiles
        worksheet.write(row, 0, 'Percentiles', header_format)
        row += 1
        
        percentiles = results.get('percentiles', {})
        for key, value in percentiles.items():
            worksheet.write(row, 0, key, label_format)
            worksheet.write(row, 1, value, number_format)
            row += 1
            
        # Confidence interval
        ci = results.get('confidence_interval_90', (0, 0))
        row += 1
        worksheet.write(row, 0, '90% Confidence Interval:', label_format)
        worksheet.write(row, 1, f'{ci[0]:.2f} - {ci[1]:.2f}')
        
        # Add histogram data if available
        if 'histogram_data' in results:
            row += 2
            worksheet.write(row, 0, 'Histogram Data', header_format)
            row += 1
            
            # Create a simple histogram chart
            chart = workbook.add_chart({'type': 'column'})
            
            # Add histogram values (limited sample)
            hist_values = results['histogram_data'].get('values', [])[:100]
            for i, val in enumerate(hist_values):
                worksheet.write(row + i, 3, val)
                
            if hist_values:
                chart.add_series({
                    'values': f'=Monte Carlo Results!$D${row+1}:$D${row+len(hist_values)}',
                    'name': 'Distribution'
                })
                
                chart.set_title({'name': 'Outcome Distribution'})
                chart.set_x_axis({'name': 'Iteration'})
                chart.set_y_axis({'name': 'Value'})
                
                worksheet.insert_chart('F2', chart)
        
        workbook.close()
        
        if filename:
            return filename
        else:
            output.seek(0)
            return output
            
    def _export_monte_carlo_pdf(self, results: Dict, filename: Optional[str], include_histogram: bool) -> Union[str, io.BytesIO]:
        """Export Monte Carlo results to PDF."""
        if not PDF_AVAILABLE:
            raise ImportError("reportlab not available")
            
        if filename:
            buffer = filename
        else:
            buffer = io.BytesIO()
            
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        elements = []
        
        # Styles
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Title'],
            fontSize=20,
            textColor=colors.HexColor('#1E88E5')
        )
        
        # Title
        elements.append(Paragraph('Monte Carlo Simulation Report', title_style))
        elements.append(Spacer(1, 0.5 * inch))
        
        # Summary statistics table
        stats_data = [
            ['Statistic', 'Value'],
            ['Iterations', f"{results.get('iterations', 0):,}"],
            ['Mean', f"{results.get('mean', 0):,.2f}"],
            ['Standard Deviation', f"{results.get('std_dev', 0):,.2f}"],
            ['Minimum', f"{results.get('min', 0):,.2f}"],
            ['Maximum', f"{results.get('max', 0):,.2f}"],
            ['Coefficient of Variation', f"{results.get('coefficient_of_variation', 0):.3f}"]
        ]
        
        stats_table = Table(stats_data, colWidths=[3*inch, 2*inch])
        stats_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#E3F2FD')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ]))
        
        elements.append(stats_table)
        elements.append(Spacer(1, 0.5 * inch))
        
        # Percentiles
        elements.append(Paragraph('Percentile Analysis', styles['Heading2']))
        
        percentiles = results.get('percentiles', {})
        perc_data = [['Percentile', 'Value']]
        for key, value in percentiles.items():
            perc_data.append([key.upper(), f"{value:,.2f}"])
            
        perc_table = Table(perc_data, colWidths=[2*inch, 2*inch])
        perc_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#E3F2FD')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ]))
        
        elements.append(perc_table)
        
        # Histogram (if matplotlib available)
        if include_histogram and CHARTS_AVAILABLE and 'histogram_data' in results:
            elements.append(PageBreak())
            elements.append(Paragraph('Distribution Analysis', styles['Heading2']))
            
            # Create histogram
            try:
                hist_values = results['histogram_data'].get('values', [])
                if hist_values:
                    plt.figure(figsize=(8, 6))
                    plt.hist(hist_values, bins=50, edgecolor='black', alpha=0.7)
                    plt.xlabel('Value')
                    plt.ylabel('Frequency')
                    plt.title('Monte Carlo Simulation Results Distribution')
                    plt.grid(True, alpha=0.3)
                    
                    # Save to temporary file
                    import tempfile
                    with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
                        plt.savefig(tmp.name, dpi=150, bbox_inches='tight')
                        plt.close()
                        
                        # Add image to PDF
                        img = Image(tmp.name, width=6*inch, height=4.5*inch)
                        elements.append(img)
                        
                        # Clean up
                        import os
                        os.unlink(tmp.name)
            except Exception as e:
                logger.error(f"Failed to create histogram: {e}")
        
        doc.build(elements)
        
        if not filename:
            buffer.seek(0)
            
        return buffer if not filename else filename
        
    def export_batch_results(
        self,
        results_list: List[Dict],
        format: str,
        filename: Optional[str] = None
    ) -> Union[str, bytes, io.BytesIO]:
        """Export multiple calculation results in batch.
        
        Args:
            results_list: List of calculation results
            format: Export format
            filename: Optional filename
            
        Returns:
            File path or bytes
        """
        if format == 'excel' and XLSX_AVAILABLE:
            return self._export_batch_excel(results_list, filename)
        elif format == 'json':
            export_data = {
                'metadata': {
                    'generated': datetime.now().isoformat(),
                    'count': len(results_list)
                },
                'results': results_list
            }
            if filename:
                with open(filename, 'w') as f:
                    json.dump(export_data, f, indent=2, default=str)
                return filename
            else:
                return json.dumps(export_data, indent=2, default=str)
        else:
            raise ValueError(f"Batch export not supported for format: {format}")
            
    def _export_batch_excel(self, results_list: List[Dict], filename: Optional[str]) -> Union[str, io.BytesIO]:
        """Export batch results to Excel with multiple sheets."""
        if filename:
            workbook = xlsxwriter.Workbook(filename)
        else:
            output = io.BytesIO()
            workbook = xlsxwriter.Workbook(output)
            
        # Summary sheet
        summary_sheet = workbook.add_worksheet('Summary')
        header_format = workbook.add_format({'bold': True, 'bg_color': '#E3F2FD'})
        
        summary_sheet.write(0, 0, 'Analysis Summary', header_format)
        summary_sheet.write(1, 0, 'Total Analyses:', header_format)
        summary_sheet.write(1, 1, len(results_list))
        summary_sheet.write(2, 0, 'Generated:', header_format)
        summary_sheet.write(2, 1, datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        
        # Individual sheets for each result
        for i, result in enumerate(results_list):
            sheet_name = f'Analysis_{i+1}'
            worksheet = workbook.add_worksheet(sheet_name[:31])  # Excel limit
            
            # Write results to individual sheet
            row = 0
            for key, value in result.items():
                if isinstance(value, dict):
                    worksheet.write(row, 0, key, header_format)
                    row += 1
                    for sub_key, sub_value in value.items():
                        worksheet.write(row, 0, f"  {sub_key}")
                        worksheet.write(row, 1, str(sub_value))
                        row += 1
                else:
                    worksheet.write(row, 0, key)
                    worksheet.write(row, 1, str(value))
                    row += 1
                    
        workbook.close()
        
        if filename:
            return filename
        else:
            output.seek(0)
            return output


# Global export manager instance
export_manager = ExportManager()