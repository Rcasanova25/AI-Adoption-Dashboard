#!/usr/bin/env python3
"""Fix double 'r' prefix issues created by regex fixing script."""

import os
import re
from pathlib import Path

def fix_double_r_prefixes():
    """Fix rr"..." and rrf"..." syntax errors."""
    
    loader_files = [
        "data/loaders/goldman_sachs.py",
        "data/loaders/oecd.py",
        "data/loaders/nvidia.py",
        "data/loaders/federal_reserve.py", 
        "data/loaders/academic.py",
        "data/loaders/mckinsey.py",
        "data/loaders/ai_index.py"
    ]
    
    fixes = [
        # Fix double r prefixes
        (r'\brr"', r'r"'),
        (r"\brr'", r"r'"),
        (r'\brrf"', r'rf"'),
        (r"\brrf'", r"rf'"),
        (r'\bfrr"', r'rf"'),  # In case it became frr instead of rrf
        (r"\bfrr'", r"rf'"),
    ]
    
    fixed_files = []
    
    for file_path in loader_files:
        if not os.path.exists(file_path):
            print(f"⚠️  File not found: {file_path}")
            continue
            
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            changes_made = []
            
            # Apply fixes
            for pattern, replacement in fixes:
                matches = re.findall(pattern, content)
                if matches:
                    content = re.sub(pattern, replacement, content)
                    changes_made.append(f"Fixed {len(matches)} instances of {pattern}")
            
            # Write back if changed
            if content != original_content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                fixed_files.append(file_path)
                print(f"✅ Fixed double r prefixes in: {file_path}")
                for change in changes_made:
                    print(f"   {change}")
            else:
                print(f"📄 No double r prefixes found: {file_path}")
                
        except Exception as e:
            print(f"❌ Error processing {file_path}: {e}")
    
    return fixed_files

if __name__ == "__main__":
    print("🔧 Fixing double 'r' prefix syntax errors...")
    fixed = fix_double_r_prefixes()
    print(f"\n✅ Fixed {len(fixed)} files")
    
    if fixed:
        print("\nFixed files:")
        for f in fixed:
            print(f"  - {f}")
        
        print("\n🧪 Now test your imports again:")
        print('python -c "from data.loaders import goldman_sachs; print(\'Goldman Sachs loader works\')"')