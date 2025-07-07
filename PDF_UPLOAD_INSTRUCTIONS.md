# PDF Upload Instructions for AI Adoption Dashboard

## Where to Place PDF Files

The dashboard needs PDF files to display real data. Currently it's using demo data.

### 📁 Directory Structure

Place your PDF files in this exact location:

```
ai-adoption-dashboard/
├── AI adoption resources/              <-- Create this folder
│   └── AI dashboard resources 1/       <-- Create this subfolder
│       ├── hai_ai_index_report_2025.pdf
│       ├── the-state-of-ai-how-organizations-are-rewiring-to-capture-value_final.pdf
│       └── (other PDFs listed below)
├── app_dash.py
└── (other files)
```

### 📄 Required PDF Files (10 files)

Place these exact files in `AI adoption resources/AI dashboard resources 1/`:

1. **hai_ai_index_report_2025.pdf**
   - Stanford HAI AI Index Report

2. **the-state-of-ai-how-organizations-are-rewiring-to-capture-value_final.pdf**
   - McKinsey State of AI Report

3. **oecd-artificial-intelligence-review-2025.pdf**
   - OECD AI Report 2025

4. **cost-benefit-analysis-artificial-intelligence-evidence-from-a-field-experiment-on-gpt-4o-1.pdf**
   - Richmond Fed AI Cost-Benefit Analysis

5. **the-economic-impact-of-large-language-models.pdf**
   - St. Louis Fed LLM Economic Impact

6. **gs-new-decade-begins.pdf**
   - Goldman Sachs AI Report

7. **nvidia-cost-trends-ai-inference-at-scale.pdf**
   - NVIDIA Token Economics Report

8. **wpiea2024231-print-pdf.pdf**
   - IMF Working Paper

9. **w30957.pdf**
   - NBER Working Paper

10. **Machines of mind_ The case for an AI-powered productivity boom.pdf**
    - AI Productivity Report

## 🚀 Quick Setup

### Windows Command Line:
```cmd
cd C:\Users\rcasa\OneDrive\Documents\ai-adoption-dashboard
mkdir "AI adoption resources\AI dashboard resources 1"
```

Then copy your PDF files to:
```
C:\Users\rcasa\OneDrive\Documents\ai-adoption-dashboard\AI adoption resources\AI dashboard resources 1\
```

### Windows PowerShell:
```powershell
cd C:\Users\rcasa\OneDrive\Documents\ai-adoption-dashboard
New-Item -ItemType Directory -Path "AI adoption resources\AI dashboard resources 1" -Force
```

### Linux/Mac:
```bash
cd /path/to/ai-adoption-dashboard
mkdir -p "AI adoption resources/AI dashboard resources 1"
```

## ✅ Verification

After placing the PDFs:

1. **Restart the Dash app**:
   ```bash
   python app_dash.py
   ```

2. **Check the loading message**:
   - Should say "Successfully loaded X datasets from PDFs!"
   - Instead of "Using Demo Data"

3. **View the data**:
   - Charts will show real data from the PDFs
   - More detailed insights will be available

## 🔍 Troubleshooting

### PDFs not loading?

1. **Check file names**: Must match exactly (case-sensitive)
2. **Check location**: Must be in `AI adoption resources/AI dashboard resources 1/`
3. **Check console**: Look for error messages when app starts
4. **Java required**: Some PDF processing needs Java installed

### Still using demo data?

The app will use demo data if:
- PDFs are missing or in wrong location
- PDF processing fails (missing Java/dependencies)
- File names don't match exactly

### Need Java?

Some PDF processing requires Java:
- Windows: Download from https://adoptium.net/
- Mac: `brew install openjdk`
- Linux: `sudo apt install default-jdk`

## 📊 What Happens After Upload

Once PDFs are in place:
1. App extracts data from PDFs automatically
2. Real adoption rates, financial data, etc. are displayed
3. All 21 views show actual research data
4. Charts and insights reflect real AI adoption trends

The dashboard will automatically detect and load the PDFs on next restart!