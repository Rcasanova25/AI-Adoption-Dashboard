# Update Instructions for Economics of AI Dashboard

## Quick Integration (Minimal Changes)

To add all new features to your existing app.py with minimal changes:

### Option 1: One-Line Integration

Add these two lines after `st.set_page_config()` in your app.py:

```python
from dashboard_integration_enhanced import upgrade_dashboard
upgrade_dashboard()
```

This will:
- Replace load_data() with optimized version
- Add competitive assessment button
- Enable accessibility features
- Add progressive disclosure
- Add economic insights

### Option 2: Selective Integration

For more control, update specific parts:

#### 1. Replace Data Loading Function

Replace:
```python
@st.cache_data
def load_data():
    # ... existing code
```

With:
```python
from dashboard_integration_enhanced import load_data_enhanced as load_data
```

#### 2. Add New Features to Sidebar

After sidebar setup, add:
```python
from dashboard_integration_enhanced import inject_new_features
inject_new_features()
```

#### 3. Enhance Existing Views

In each view rendering section, add:
```python
from dashboard_integration_enhanced import add_view_enhancements
add_view_enhancements(view_type, loaded_data)
```

## Full Migration (Recommended)

For the complete Economics of AI experience:

### Step 1: Backup Current App
```bash
cp app.py app_backup.py
```

### Step 2: Use Migration Script
```bash
python migrate_app.py
```

### Step 3: Test with Transition App
```bash
streamlit run app_transition.py
```

### Step 4: Deploy New Version
```bash
cp app_new.py app.py
streamlit run app.py
```

## Testing the Integration

After updating, test these features:

1. **Competitive Assessment**: Click the "🏆 Competitive Assessment" button in sidebar
2. **Accessibility**: Check for keyboard navigation and screen reader support
3. **Progressive Disclosure**: Use the disclosure level selector in sidebar
4. **Economic Insights**: Click "💡 Economic Insights" button
5. **Performance**: Check load times (should be <3 seconds)

## Rollback

If needed, restore the original:
```bash
cp app_backup.py app.py
```

## Environment Setup

Create a `.env` file:
```
CACHE_MEMORY_SIZE=200
CACHE_MEMORY_TTL=600
ENABLE_COMPETITIVE_ASSESSOR=true
ENABLE_ACCESSIBILITY=true
```

## Support

- Issues: https://github.com/Rcasanova25/AI-Adoption-Dashboard/issues
- Documentation: See IMPLEMENTATION_SUMMARY.md