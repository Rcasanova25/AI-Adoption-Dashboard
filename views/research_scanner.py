"""
Research Scanner view for AI Adoption Dashboard
Automated detection and integration of new research documents
"""

import streamlit as st
import pandas as pd
from typing import Dict, Any
import logging
from datetime import datetime
import json

from data.automated_research_scanner import (
    AutomatedResearchScanner, 
    ResearchIntegrationWorkflow,
    display_automated_scanner_dashboard
)
from data.pdf_extractor import pdf_extractor, data_mapper
from Utils.data_validation import safe_download_button
from Utils.helpers import clean_filename

logger = logging.getLogger(__name__)


def show_research_scanner(
    data_year: str,
    sources_data: pd.DataFrame = None,
    dashboard_data: Dict[str, Any] = None
) -> None:
    """
    Display automated research scanner and integration interface
    
    Args:
        data_year: Selected year
        sources_data: DataFrame with existing sources (optional)
        dashboard_data: Full dashboard data dict (optional)
    """
    
    st.write("🔍 **Automated Research Scanner & Integration**")
    
    # Initialize scanner with your research folders
    watch_folders = [
        "/mnt/c/Users/rcasa/OneDrive/Documents/AI-Adoption-Dashboard/AI adoption resources",
        "research_documents",  # Additional folders can be added
        "new_research"
    ]
    
    try:
        scanner = AutomatedResearchScanner(watch_folders)
        workflow = ResearchIntegrationWorkflow(scanner)
        
        # Create tabs for different functionalities
        tab1, tab2, tab3, tab4 = st.tabs([
            "📊 Scanner Dashboard", 
            "🆕 New Documents", 
            "⏳ Pending Integration", 
            "✅ Integration History"
        ])
        
        with tab1:
            st.markdown("### 📊 Research Integration Overview")
            
            # Summary metrics
            col1, col2, col3, col4 = st.columns(4)
            
            total_scanned = len(scanner.scanned_documents)
            integrated = sum(1 for doc in scanner.scanned_documents.values() 
                           if doc.integration_status == 'integrated')
            pending = sum(1 for doc in scanner.scanned_documents.values() 
                         if doc.integration_status == 'pending')
            high_priority = sum(1 for doc in scanner.scanned_documents.values() 
                              if doc.integration_status == 'pending' and 
                              doc.credibility_rating in ['A+', 'A'])
            
            with col1:
                st.metric("Total Documents", total_scanned)
            with col2:
                st.metric("Integrated", integrated, delta=f"{(integrated/total_scanned*100):.0f}%" if total_scanned > 0 else "0%")
            with col3:
                st.metric("Pending", pending)
            with col4:
                st.metric("High Priority", high_priority, delta="A/A+ credibility")
            
            # Scan button
            st.markdown("---")
            if st.button("🔄 Scan for New Research Documents", type="primary"):
                with st.spinner("Scanning folders for new PDFs..."):
                    report = workflow.run_integration_check()
                
                if report['new_documents_found'] > 0:
                    st.success(f"✅ Found {report['new_documents_found']} new documents!")
                else:
                    st.info("No new documents found since last scan")
                
                # Store scan results in session state
                st.session_state['last_scan_report'] = report
                st.session_state['last_scan_time'] = datetime.now()
            
            # Show last scan info
            if 'last_scan_time' in st.session_state:
                st.caption(f"Last scan: {st.session_state['last_scan_time'].strftime('%Y-%m-%d %H:%M:%S')}")
        
        with tab2:
            st.markdown("### 🆕 Newly Detected Documents")
            
            # Get new documents from last scan
            if 'last_scan_report' in st.session_state:
                new_docs = st.session_state['last_scan_report']['new_documents']
                
                if new_docs:
                    for doc in new_docs:
                        with st.expander(f"📄 {doc.filename}", expanded=True):
                            col1, col2 = st.columns(2)
                            
                            with col1:
                                st.write(f"**Authority:** {doc.authority or 'Unknown'}")
                                st.write(f"**Category:** {doc.category}")
                                st.write(f"**Credibility:** {doc.credibility_rating}")
                            
                            with col2:
                                st.write(f"**Year:** {doc.year or 'Unknown'}")
                                st.write(f"**File Size:** {doc.file_size / (1024*1024):.2f} MB")
                                st.write(f"**Path:** `{doc.filename}`")
                            
                            # Extract data preview
                            if st.button(f"🔍 Preview Extraction", key=f"preview_{doc.file_hash[:8]}"):
                                with st.spinner("Extracting data preview..."):
                                    try:
                                        # Extract data from PDF
                                        extracted_data = pdf_extractor.extract_from_pdf(doc.filepath)
                                        
                                        # Show key findings
                                        st.write("**Key Findings:**")
                                        findings = extracted_data.get('key_findings', [])
                                        for finding in findings[:3]:  # Show first 3
                                            st.write(f"• {finding}")
                                        
                                        # Show statistics
                                        stats = extracted_data.get('key_statistics', [])
                                        if stats:
                                            st.write("**Key Statistics:**")
                                            stats_df = pd.DataFrame(stats)
                                            st.dataframe(stats_df, use_container_width=True)
                                    
                                    except Exception as e:
                                        st.error(f"Preview extraction failed: {str(e)}")
                                        st.info("Note: Full PDF parsing requires additional libraries (PyPDF2, pdfplumber)")
                            
                            # Generate integration code
                            if st.button(f"⚡ Generate Integration Code", key=f"generate_{doc.file_hash[:8]}"):
                                code, registry = scanner.generate_integration_code(doc)
                                
                                st.markdown("**Integration Method:**")
                                st.code(code, language='python')
                                
                                st.markdown("**Registry Entry:**")
                                st.code(registry, language='python')
                                
                                # Mark as ready for integration
                                if st.button(f"✅ Mark as Ready", key=f"ready_{doc.file_hash[:8]}"):
                                    doc.integration_status = 'ready'
                                    scanner._save_scan_history()
                                    st.success("Document marked as ready for integration!")
                                    st.rerun()
                else:
                    st.info("No new documents found. Click 'Scan for New Research Documents' to check for updates.")
            else:
                st.info("Run a scan to detect new documents")
        
        with tab3:
            st.markdown("### ⏳ Pending Integration Queue")
            
            # Get recommendations
            recommendations = scanner.get_integration_recommendations()
            
            if not recommendations.empty:
                # Sort by priority
                recommendations = recommendations.sort_values('integration_priority', ascending=False)
                
                # Display as interactive table
                st.dataframe(
                    recommendations,
                    use_container_width=True,
                    hide_index=True,
                    column_config={
                        "filename": st.column_config.TextColumn("Document", width="medium"),
                        "authority": st.column_config.TextColumn("Authority", width="small"),
                        "category": st.column_config.TextColumn("Category", width="small"),
                        "credibility": st.column_config.TextColumn("Credibility", width="small"),
                        "integration_priority": st.column_config.NumberColumn("Priority", format="%d"),
                        "file_size_mb": st.column_config.NumberColumn("Size (MB)", format="%.2f"),
                    }
                )
                
                # Batch integration
                st.markdown("#### 🚀 Batch Integration")
                
                high_priority_docs = recommendations[recommendations['integration_priority'] >= 15]
                if len(high_priority_docs) > 0:
                    if st.button("⚡ Generate Code for All High Priority Documents"):
                        # Get document hashes
                        doc_hashes = []
                        for filename in high_priority_docs['filename']:
                            for hash_id, doc in scanner.scanned_documents.items():
                                if doc.filename == filename:
                                    doc_hashes.append(hash_id)
                                    break
                        
                        # Generate batch code
                        code, registry = workflow.generate_batch_integration_code(doc_hashes)
                        
                        st.markdown("**Generated Integration Code:**")
                        st.code(code, language='python')
                        
                        st.markdown("**Registry Entries:**")
                        st.code(registry, language='python')
                        
                        st.success(f"✅ Generated integration code for {len(doc_hashes)} documents!")
                
                # Download recommendations
                safe_download_button(
                    recommendations,
                    clean_filename(f"research_integration_queue_{datetime.now().strftime('%Y%m%d')}.csv"),
                    "📥 Download Integration Queue",
                    key="download_queue",
                    help_text="Download the complete integration queue with priorities"
                )
            else:
                st.success("✅ No documents pending integration!")
        
        with tab4:
            st.markdown("### ✅ Integration History")
            
            # Build history dataframe
            history_data = []
            for doc in scanner.scanned_documents.values():
                if doc.integration_status == 'integrated':
                    history_data.append({
                        'Document': doc.filename,
                        'Authority': doc.authority or 'Unknown',
                        'Category': doc.category,
                        'Credibility': doc.credibility_rating,
                        'Integrated Date': doc.detected_date[:10],
                        'Method': doc.extraction_method or 'manual'
                    })
            
            if history_data:
                history_df = pd.DataFrame(history_data)
                
                # Summary stats
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Total Integrated", len(history_df))
                
                with col2:
                    high_cred = len(history_df[history_df['Credibility'].isin(['A+', 'A'])])
                    st.metric("High Credibility", high_cred)
                
                with col3:
                    automated = len(history_df[history_df['Method'] == 'automated'])
                    st.metric("Auto-Integrated", automated)
                
                # Display history table
                st.dataframe(history_df, use_container_width=True, hide_index=True)
                
                # Category breakdown
                st.markdown("#### 📊 Integration by Category")
                category_counts = history_df['Category'].value_counts()
                
                # Simple bar chart
                st.bar_chart(category_counts)
                
                # Download history
                safe_download_button(
                    history_df,
                    clean_filename(f"integration_history_{datetime.now().strftime('%Y%m%d')}.csv"),
                    "📥 Download Integration History",
                    key="download_history",
                    help_text="Download complete integration history"
                )
            else:
                st.info("No documents have been integrated yet")
        
        # Configuration section
        with st.expander("⚙️ Scanner Configuration"):
            st.markdown("#### Watch Folders")
            for folder in watch_folders:
                st.write(f"• `{folder}`")
            
            st.markdown("#### Supported Authorities")
            authorities = list(scanner.integration_rules['authority_patterns'].keys())
            cols = st.columns(3)
            for i, authority in enumerate(authorities):
                cols[i % 3].write(f"• {authority}")
            
            st.markdown("#### Category Keywords")
            categories = list(scanner.integration_rules['category_keywords'].keys())
            for category in categories:
                keywords = scanner.integration_rules['category_keywords'][category][:3]
                st.write(f"• **{category.replace('_', ' ').title()}:** {', '.join(keywords)}...")
    
    except Exception as e:
        logger.error(f"Error in research scanner: {e}")
        st.error("Research scanner initialization failed")
        st.info("""
        **Setup Instructions:**
        1. Ensure research folders exist and are accessible
        2. Place PDF documents in the watched folders
        3. Check file permissions
        
        **Note:** Full PDF extraction requires additional libraries:
        - PyPDF2 or pdfplumber for text extraction
        - Camelot or Tabula for table extraction
        """)


# Convenience function to add scanner to navigation
def add_research_scanner_to_menu():
    """Add research scanner to the main navigation menu"""
    return "Research Scanner"