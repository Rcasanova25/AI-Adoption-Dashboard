# Required PDF Data Files for AI Adoption Dashboard

## ⚠️ CRITICAL: Missing Data Files

The dashboard cannot function without the following PDF files. These must be uploaded to the deployment environment.

## 📁 Required Directory Structure

```
/mount/src/ai-adoption-dashboard/
└── AI adoption resources/
    └── AI dashboard resources 1/
        ├── hai_ai_index_report_2025.pdf
        ├── the-state-of-ai-how-organizations-are-rewiring-to-capture-value_final.pdf
        ├── oecd-artificial-intelligence-review-2025.pdf
        ├── cost-benefit-analysis-artificial-intelligence-evidence-from-a-field-experiment-on-gpt-4o-1.pdf
        ├── the-economic-impact-of-large-language-models.pdf
        ├── gs-new-decade-begins.pdf
        ├── nvidia-cost-trends-ai-inference-at-scale.pdf
        ├── wpiea2024231-print-pdf.pdf
        ├── w30957.pdf
        └── Machines of mind_ The case for an AI-powered productivity boom.pdf
```

## 📄 Required PDF Files (10 files)

### 1. **Stanford HAI AI Index Report 2025**
- **Filename**: `hai_ai_index_report_2025.pdf`
- **Source**: Stanford Human-Centered AI Institute
- **Purpose**: Core adoption trends, sector analysis, geographic data
- **Required for**: Historical trends, sector analysis, firm size analysis

### 2. **McKinsey State of AI Report**
- **Filename**: `the-state-of-ai-how-organizations-are-rewiring-to-capture-value_final.pdf`
- **Source**: McKinsey & Company
- **Purpose**: Financial impact, use cases, implementation barriers
- **Required for**: Financial impact view, ROI analysis

### 3. **OECD 2025 AI Report**
- **Filename**: `oecd-artificial-intelligence-review-2025.pdf`
- **Source**: Organisation for Economic Co-operation and Development
- **Purpose**: Policy insights, international adoption patterns
- **Required for**: OECD 2025 findings view

### 4. **Richmond Fed AI Cost-Benefit Analysis**
- **Filename**: `cost-benefit-analysis-artificial-intelligence-evidence-from-a-field-experiment-on-gpt-4o-1.pdf`
- **Source**: Federal Reserve Bank of Richmond
- **Purpose**: Economic impact analysis, productivity gains
- **Required for**: Productivity research view

### 5. **St. Louis Fed LLM Economic Impact**
- **Filename**: `the-economic-impact-of-large-language-models.pdf`
- **Source**: Federal Reserve Bank of St. Louis
- **Purpose**: LLM economic analysis, labor impact
- **Required for**: Labor impact analysis

### 6. **Goldman Sachs New Decade Report**
- **Filename**: `gs-new-decade-begins.pdf`
- **Source**: Goldman Sachs Research
- **Purpose**: GDP impact projections, sector productivity
- **Required for**: Economic projections

### 7. **NVIDIA Token Economics Report**
- **Filename**: `nvidia-cost-trends-ai-inference-at-scale.pdf`
- **Source**: NVIDIA Research
- **Purpose**: Token pricing, cost trends, optimization strategies
- **Required for**: Token economics view, AI cost trends

### 8. **IMF Working Paper**
- **Filename**: `wpiea2024231-print-pdf.pdf`
- **Source**: International Monetary Fund
- **Purpose**: Global economic impact analysis
- **Required for**: Global economic perspectives

### 9. **NBER Working Paper**
- **Filename**: `w30957.pdf`
- **Source**: National Bureau of Economic Research
- **Purpose**: Academic research on AI productivity
- **Required for**: Academic perspectives

### 10. **Machines of Mind Report**
- **Filename**: `Machines of mind_ The case for an AI-powered productivity boom.pdf`
- **Source**: Research report
- **Purpose**: AI productivity analysis
- **Required for**: Productivity boom analysis

## 🚀 Upload Instructions

### For Streamlit Cloud Deployment:

1. **Create Directory Structure**:
   ```bash
   mkdir -p "AI adoption resources/AI dashboard resources 1"
   ```

2. **Upload Files**:
   - Use Streamlit Cloud file manager
   - Or commit files to git repository (if size permits)
   - Or use git LFS for large files

3. **Verify Upload**:
   ```bash
   ls -la "AI adoption resources/AI dashboard resources 1/"
   ```

### For Local Deployment:

1. **Copy Files**:
   ```bash
   cp /path/to/pdf/files/* "AI adoption resources/AI dashboard resources 1/"
   ```

2. **Set Permissions**:
   ```bash
   chmod 644 "AI adoption resources/AI dashboard resources 1/"*.pdf
   ```

## ✅ Verification

After uploading, verify files are accessible:

```python
import os
from pathlib import Path

data_dir = Path("AI adoption resources/AI dashboard resources 1")
required_files = [
    "hai_ai_index_report_2025.pdf",
    "the-state-of-ai-how-organizations-are-rewiring-to-capture-value_final.pdf",
    "oecd-artificial-intelligence-review-2025.pdf",
    "cost-benefit-analysis-artificial-intelligence-evidence-from-a-field-experiment-on-gpt-4o-1.pdf",
    "the-economic-impact-of-large-language-models.pdf",
    "gs-new-decade-begins.pdf",
    "nvidia-cost-trends-ai-inference-at-scale.pdf",
    "wpiea2024231-print-pdf.pdf",
    "w30957.pdf",
    "Machines of mind_ The case for an AI-powered productivity boom.pdf"
]

for file in required_files:
    path = data_dir / file
    if path.exists():
        print(f"✅ {file}")
    else:
        print(f"❌ {file} - MISSING")
```

## 🔍 Alternative: Use Sample Data

If original PDFs are not available, you can:

1. Create sample CSV files with the expected data structure
2. Place them in a `sample_data/` directory
3. Update data loaders to check for CSV alternatives

## ⚠️ Important Notes

- **File Size**: Some PDFs may be large (10-50MB each)
- **Git Limits**: GitHub has a 100MB file size limit
- **Solution**: Use Git LFS or external storage for large files
- **Permissions**: Ensure files are readable by the application user

---

**Without these files, the dashboard will show "0/25 datasets available" and cannot function properly.**