# 🤖 Automated Research Integration Guide

## Overview

The AI Adoption Dashboard now includes an **Automated Research Scanner** that can detect, analyze, and integrate new research PDFs automatically. This guide explains how to set up and use this powerful feature.

---

## 🚀 Quick Start

1. **Place PDFs in watched folders:**
   - `/AI adoption resources/` (your existing folder)
   - `/research_documents/` (optional)
   - `/new_research/` (optional)

2. **Access the Research Scanner:**
   - Add to main navigation: `"Research Scanner"` in VIEW_TYPES
   - Or use directly in code: `show_research_scanner()`

3. **Run a scan:**
   - Click "🔄 Scan for New Research Documents"
   - Review detected documents
   - Generate integration code
   - Copy code to `research_integration.py`

---

## 📁 Folder Structure

```
AI-Adoption-Dashboard/
├── AI adoption resources/        # Main research folder (monitored)
│   ├── existing_pdfs.pdf        # Your 25+ existing PDFs
│   └── new_research.pdf         # New PDFs automatically detected
├── data/
│   ├── automated_research_scanner.py   # Scanner module
│   ├── pdf_extractor.py               # PDF extraction module
│   ├── research_integration.py        # Where generated code goes
│   └── scan_history.json              # Tracking file (auto-created)
└── views/
    └── research_scanner.py            # UI component
```

---

## 🔍 How It Works

### 1. **Automatic Detection**
The scanner monitors folders and detects new PDFs by:
- Calculating file hash (prevents duplicates)
- Extracting metadata from filename
- Categorizing based on content patterns
- Assigning credibility ratings

### 2. **Intelligent Categorization**
Documents are automatically categorized as:
- `economic_analysis` - GDP, growth, productivity studies
- `policy_research` - Regulations, governance, frameworks
- `technical_analysis` - Implementation, architecture, MLOps
- `sector_analysis` - Industry-specific research
- `adoption_studies` - Deployment and maturity analysis
- `workforce_impact` - Employment, skills, talent studies
- `cost_analysis` - ROI, pricing, investment research
- `case_studies` - Implementation examples

### 3. **Credibility Rating**
Automatic credibility assignment based on source:
- **A+**: Stanford, MIT, Federal Reserve, OECD, IMF, NBER
- **A**: McKinsey, Goldman Sachs, Major consultancies
- **B+**: Industry reports, Technology vendors
- **B**: White papers, General documentation

### 4. **Code Generation**
The system generates:
- Python method for data extraction
- DataFrame structure with proper columns
- Source attribution and metadata
- Registry entry for tracking

---

## 🛠️ Setup Instructions

### Basic Setup (No PDF Parsing)

```python
# The system works out of the box for:
# - File detection and categorization
# - Integration code templates
# - Source tracking and history
```

### Advanced Setup (Full PDF Extraction)

To enable automatic content extraction from PDFs:

```bash
# Install PDF parsing libraries
pip install PyPDF2 pdfplumber
pip install camelot-py[cv]  # For table extraction
pip install tabula-py      # Alternative table extraction

# For NLP-based analysis
pip install spacy
python -m spacy download en_core_web_sm
```

---

## 📋 Usage Workflow

### Step 1: Add New Research PDFs
Simply drop new PDF files into the watched folder:
```
/AI adoption resources/new_ai_study_2024.pdf
/AI adoption resources/oecd_ai_report_2024.pdf
```

### Step 2: Run Scanner
```python
# In the dashboard UI:
1. Navigate to "Research Scanner" view
2. Click "🔄 Scan for New Research Documents"
3. Review detected documents in "New Documents" tab
```

### Step 3: Preview & Generate Code
```python
# For each new document:
1. Click "🔍 Preview Extraction" to see extracted data
2. Click "⚡ Generate Integration Code" 
3. Review the generated Python code
4. Copy the code snippets
```

### Step 4: Integration
```python
# Add to research_integration.py:

# 1. Add the generated method to ResearchDataIntegrator class
def get_economic_analysis_abc123_data(self) -> pd.DataFrame:
    # Generated code here
    
# 2. Add registry entry to self.data_sources in __init__
'abc123': {
    'name': 'New Economic Analysis',
    'file': 'new_study.pdf',
    # etc.
}

# 3. Add to load_authentic_data_collection() 
'new_economic_data': research_integrator.get_economic_analysis_abc123_data(),
```

### Step 5: Update Dashboard Views
```python
# Use the new data in relevant views
economic_data = load_new_economic_analysis_data()
# Display in appropriate dashboard view
```

---

## 🎯 Best Practices

### 1. **File Naming Convention**
Use descriptive filenames for better auto-categorization:
```
Good: Stanford_AI_Index_2025_Report.pdf
Good: OECD_Employment_Outlook_AI_Analysis_2024.pdf
Good: Goldman_Sachs_Economic_Impact_AI_2024.pdf

Avoid: document1.pdf, report.pdf, untitled.pdf
```

### 2. **Folder Organization**
Organize by source or category:
```
/AI adoption resources/
  /academic/          # Stanford, MIT, NBER
  /government/        # Fed, OECD, IMF
  /industry/          # McKinsey, Goldman Sachs
  /technical/         # NVIDIA, implementation guides
```

### 3. **Regular Scanning**
- Run scans weekly or when adding new documents
- Review high-priority documents first (A+ credibility)
- Batch integrate related documents

### 4. **Quality Control**
- Always review generated code before integration
- Verify data extraction accuracy
- Test integration in development first
- Maintain source attribution

---

## 🔧 Advanced Features

### Custom Authority Patterns
Add new recognized authorities:
```python
# In automated_research_scanner.py
'authority_patterns': {
    'Your Organization': ['YourOrg', 'Your Organization Name'],
    # Add more...
}
```

### Custom Categories
Add domain-specific categories:
```python
'category_keywords': {
    'your_category': ['keyword1', 'keyword2', 'keyword3'],
    # Add more...
}
```

### Extraction Rules
Customize PDF extraction patterns:
```python
# In pdf_extractor.py
'statistics': {
    'your_pattern': r'your regex pattern',
    # Add more...
}
```

---

## 📊 Integration Status Tracking

The system tracks document status:
- **pending**: Newly detected, awaiting review
- **ready**: Code generated, ready for integration
- **integrated**: Successfully added to dashboard
- **failed**: Integration attempted but failed
- **skipped**: Manually marked to skip

Access tracking via:
- Integration History tab in UI
- `scan_history.json` file
- Dashboard metrics

---

## 🚨 Troubleshooting

### Common Issues

1. **"No new documents found"**
   - Check folder paths are correct
   - Ensure PDFs are in watched folders
   - Verify file permissions

2. **"Preview extraction failed"**
   - Install PDF parsing libraries
   - Check PDF is not corrupted
   - Try manual extraction

3. **"Generated code has errors"**
   - Review and manually adjust code
   - Check data structure compatibility
   - Verify column names match dashboard

### Debug Mode
```python
# Enable detailed logging
import logging
logging.basicConfig(level=logging.DEBUG)

# Check scanner state
scanner = AutomatedResearchScanner(watch_folders)
print(f"Tracked documents: {len(scanner.scanned_documents)}")
print(f"Watch folders: {scanner.watch_folders}")
```

---

## 🎯 Example: Complete Integration Flow

Let's say you add: `IMF_Global_AI_Economic_Impact_2024.pdf`

1. **Scanner detects:**
   - Authority: IMF (auto-detected)
   - Category: economic_analysis
   - Credibility: A+
   - Priority: High (score: 19)

2. **Generated code:**
```python
def get_economic_analysis_a1b2c3d4_data(self) -> pd.DataFrame:
    """
    IMF Global AI Economic Impact 2024
    Source: IMF_Global_AI_Economic_Impact_2024.pdf
    Authority: IMF
    Category: economic_analysis
    """
    # Extracted data here
```

3. **Integration complete:**
   - Data available in dashboard
   - Source tracked and attributed
   - Ready for visualization

---

## 🔮 Future Enhancements

Planned improvements:
- **OCR Support**: Extract from scanned PDFs
- **Multi-language**: Support non-English documents  
- **AI Enhancement**: Use LLMs for intelligent extraction
- **Auto-commit**: Direct git integration
- **Webhooks**: Notify on new documents
- **Cloud Storage**: Monitor Google Drive, Dropbox
- **API Integration**: Pull from research APIs

---

## 📞 Support

For issues or questions:
1. Check the Integration History tab
2. Review scan_history.json
3. Enable debug logging
4. Check GitHub issues

**Remember**: The automated scanner is a powerful tool to accelerate research integration, but always review generated code for accuracy and security before adding to production!

---

**🎓 With this system, your dashboard can grow automatically as new research becomes available, maintaining its position as the most comprehensive AI adoption resource!**