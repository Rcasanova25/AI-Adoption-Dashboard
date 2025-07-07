#!/usr/bin/env python3
"""
Batch converter script to help convert Streamlit views to Dash.
This script automates the conversion process for all views.
"""

import os
import re
import shutil
from pathlib import Path
from typing import List, Dict, Tuple
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ViewConverter:
    """Converts Streamlit views to Dash format."""
    
    def __init__(self):
        self.views_dir = Path("views")
        self.template_path = Path("views/view_template_dash.py")
        self.converted_count = 0
        self.failed_conversions = []
        
    def get_all_streamlit_views(self) -> List[Path]:
        """Find all Streamlit view files that need conversion."""
        views = []
        for category_dir in self.views_dir.iterdir():
            if category_dir.is_dir() and category_dir.name not in ['__pycache__']:
                for view_file in category_dir.glob("*.py"):
                    # Skip if already converted or is __init__.py
                    if not view_file.name.endswith("_dash.py") and view_file.name != "__init__.py":
                        views.append(view_file)
        return views
    
    def analyze_streamlit_view(self, file_path: Path) -> Dict[str, any]:
        """Analyze a Streamlit view to extract key information."""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        analysis = {
            'has_title': 'st.title' in content or 'st.header' in content,
            'has_metrics': 'st.metric' in content,
            'has_columns': 'st.columns' in content,
            'has_selectbox': 'st.selectbox' in content,
            'has_multiselect': 'st.multiselect' in content,
            'has_slider': 'st.slider' in content,
            'has_plotly': 'st.plotly_chart' in content,
            'has_dataframe': 'st.dataframe' in content,
            'has_expander': 'st.expander' in content,
            'has_tabs': 'st.tabs' in content,
            'has_checkbox': 'st.checkbox' in content,
            'has_radio': 'st.radio' in content,
            'title': self.extract_title(content),
            'data_requirements': self.extract_data_requirements(content)
        }
        
        return analysis
    
    def extract_title(self, content: str) -> str:
        """Extract the title from st.title or st.write calls."""
        # Look for st.title
        title_match = re.search(r'st\.title\(["\'](.+?)["\']\)', content)
        if title_match:
            return title_match.group(1)
        
        # Look for st.write with emoji
        write_match = re.search(r'st\.write\(["\'](\*\*)?([📊🎯💰🏢🔧🌍👥🎓📈].+?)(\*\*)?["\']\)', content)
        if write_match:
            return write_match.group(2)
        
        return "View Title"
    
    def extract_data_requirements(self, content: str) -> List[str]:
        """Extract what data the view expects."""
        requirements = []
        
        # Common data patterns
        patterns = [
            r'data\.get\(["\'](\w+)["\']\)',
            r'data\[["\'](\w+)["\']\]',
            r'(\w+)\s*=\s*data\.get\(["\'](\w+)["\']\)'
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, content)
            for match in matches:
                if isinstance(match, tuple):
                    requirements.extend([m for m in match if m and m != 'data'])
                else:
                    requirements.append(match)
        
        return list(set(requirements))
    
    def create_dash_view(self, streamlit_path: Path, analysis: Dict) -> str:
        """Create a Dash version of the view based on analysis."""
        view_name = streamlit_path.stem
        category = streamlit_path.parent.name
        
        # Read template
        with open(self.template_path, 'r', encoding='utf-8') as f:
            template = f.read()
        
        # Customize template based on analysis
        dash_content = template
        
        # Replace placeholders
        dash_content = dash_content.replace("[VIEW_NAME]", view_name)
        dash_content = dash_content.replace("[View Title]", analysis['title'])
        dash_content = dash_content.replace("[View description - comprehensive analysis of AI adoption patterns]", 
                                          f"Analysis view for {view_name.replace('_', ' ').title()}")
        
        # Add specific imports if needed
        extra_imports = []
        if analysis['has_dataframe']:
            extra_imports.append("from dash import dash_table")
        
        if extra_imports:
            import_line = "import dash_bootstrap_components as dbc"
            dash_content = dash_content.replace(
                import_line,
                import_line + "\n" + "\n".join(extra_imports)
            )
        
        return dash_content
    
    def convert_single_view(self, streamlit_path: Path) -> bool:
        """Convert a single Streamlit view to Dash."""
        try:
            logger.info(f"Converting {streamlit_path}...")
            
            # Analyze the view
            analysis = self.analyze_streamlit_view(streamlit_path)
            
            # Create output path
            dash_path = streamlit_path.parent / f"{streamlit_path.stem}_dash.py"
            
            # Skip if already exists
            if dash_path.exists():
                logger.info(f"  Already converted: {dash_path}")
                return True
            
            # Generate Dash version
            dash_content = self.create_dash_view(streamlit_path, analysis)
            
            # Write the file
            with open(dash_path, 'w', encoding='utf-8') as f:
                f.write(dash_content)
            
            logger.info(f"  ✅ Created: {dash_path}")
            self.converted_count += 1
            return True
            
        except Exception as e:
            logger.error(f"  ❌ Failed to convert {streamlit_path}: {e}")
            self.failed_conversions.append((streamlit_path, str(e)))
            return False
    
    def convert_all_views(self):
        """Convert all Streamlit views to Dash."""
        logger.info("Starting batch conversion of Streamlit views to Dash...")
        logger.info("=" * 60)
        
        # Get all views
        views = self.get_all_streamlit_views()
        logger.info(f"Found {len(views)} Streamlit views to convert")
        
        # Convert each view
        for view in views:
            self.convert_single_view(view)
        
        # Summary
        logger.info("=" * 60)
        logger.info(f"Conversion complete!")
        logger.info(f"  ✅ Successfully converted: {self.converted_count}")
        logger.info(f"  ❌ Failed conversions: {len(self.failed_conversions)}")
        
        if self.failed_conversions:
            logger.info("\nFailed conversions:")
            for path, error in self.failed_conversions:
                logger.info(f"  - {path}: {error}")
    
    def create_view_status_report(self):
        """Create a report of all views and their conversion status."""
        report_path = Path("VIEW_CONVERSION_STATUS.md")
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write("# View Conversion Status Report\n\n")
            f.write("## Summary\n\n")
            
            all_views = list(self.views_dir.rglob("*.py"))
            streamlit_views = [v for v in all_views if not v.name.endswith("_dash.py") and v.name != "__init__.py"]
            dash_views = [v for v in all_views if v.name.endswith("_dash.py")]
            
            f.write(f"- Total Streamlit views: {len(streamlit_views)}\n")
            f.write(f"- Converted to Dash: {len(dash_views)}\n")
            f.write(f"- Remaining to convert: {len(streamlit_views) - len(dash_views)}\n\n")
            
            f.write("## Detailed Status\n\n")
            
            for category_dir in sorted(self.views_dir.iterdir()):
                if category_dir.is_dir() and category_dir.name not in ['__pycache__']:
                    f.write(f"### {category_dir.name.title()}\n\n")
                    
                    for view_file in sorted(category_dir.glob("*.py")):
                        if view_file.name != "__init__.py" and not view_file.name.endswith("_dash.py"):
                            dash_version = category_dir / f"{view_file.stem}_dash.py"
                            status = "✅" if dash_version.exists() else "❌"
                            f.write(f"- {status} {view_file.stem}\n")
                    
                    f.write("\n")
        
        logger.info(f"\n📄 Created conversion status report: {report_path}")


def main():
    """Run the batch conversion."""
    converter = ViewConverter()
    
    # Check if template exists
    if not converter.template_path.exists():
        logger.error(f"Template not found: {converter.template_path}")
        logger.error("Please ensure view_template_dash.py exists in the views directory")
        return
    
    # Run conversion
    converter.convert_all_views()
    
    # Create status report
    converter.create_view_status_report()
    
    logger.info("\n🎉 Batch conversion complete!")
    logger.info("Next steps:")
    logger.info("1. Review the generated Dash views")
    logger.info("2. Customize each view with specific logic from the original")
    logger.info("3. Test each view individually")
    logger.info("4. Update dash_view_manager.py to include all converted views")


if __name__ == "__main__":
    main()