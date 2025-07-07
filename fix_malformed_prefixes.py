#!/usr/bin/env python3
"""Fix all malformed string prefixes created by faulty regex fixing."""

import os
import re
from pathlib import Path

def fix_malformed_prefixes():
    """Fix all malformed string prefixes like rr, rrfr, frr, etc."""
    
    loader_files = [
        "data/loaders/goldman_sachs.py",
        "data/loaders/oecd.py",
        "data/loaders/nvidia.py",
        "data/loaders/federal_reserve.py", 
        "data/loaders/academic.py",
        "data/loaders/mckinsey.py",
        "data/loaders/ai_index.py"
    ]
    
    # Comprehensive fixes for all possible malformed prefixes
    fixes = [
        # Fix various malformed combinations
        (r'\brrfr"', r'rf"'),   # rrfr" -> rf"
        (r"\brrfr'", r"rf'"),   # rrfr' -> rf'
        (r'\brrf"', r'rf"'),    # rrf" -> rf"
        (r"\brrf'", r"rf'"),    # rrf' -> rf'
        (r'\bfrr"', r'rf"'),    # frr" -> rf"
        (r"\bfrr'", r"rf'"),    # frr' -> rf'
        (r'\brr"', r'r"'),      # rr" -> r"
        (r"\brr'", r"r'"),      # rr' -> r'
        (r'\bffr"', r'rf"'),    # ffr" -> rf"
        (r"\bffr'", r"rf'"),    # ffr' -> rf'
        (r'\bfrf"', r'rf"'),    # frf" -> rf"
        (r"\bfrf'", r"rf'"),    # frf' -> rf'
        (r'\bff"', r'f"'),      # ff" -> f"
        (r"\bff'", r"f'"),      # ff' -> f'
        
        # Handle even more complex malformed patterns
        (r'\br+f+r*"', r'rf"'), # Multiple r's and f's before "
        (r"\br+f+r*'", r"rf'"), # Multiple r's and f's before '
        (r'\bf+r+"', r'rf"'),   # Multiple f's and r's before "
        (r"\bf+r+'", r"rf'"),   # Multiple f's and r's before '
    ]
    
    fixed_files = []
    all_issues_found = []
    
    for file_path in loader_files:
        if not os.path.exists(file_path):
            print(f"⚠️  File not found: {file_path}")
            continue
            
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            changes_made = []
            
            # First, find all malformed patterns to report
            malformed_patterns = re.findall(r'\b[rf]{2,}["\']', content)
            if malformed_patterns:
                all_issues_found.extend([(file_path, p) for p in malformed_patterns])
            
            # Apply fixes
            for pattern, replacement in fixes:
                matches = re.findall(pattern, content)
                if matches:
                    content = re.sub(pattern, replacement, content)
                    changes_made.append(f"Fixed {len(matches)} instances of {pattern}")
            
            # Additional cleanup: fix any remaining sequences of multiple r's or f's
            # This catches patterns like rrr", rrrr", etc.
            content = re.sub(r'\br{2,}"', r'r"', content)
            content = re.sub(r"\br{2,}'", r"r'", content)
            content = re.sub(r'\bf{2,}"', r'f"', content)
            content = re.sub(r"\bf{2,}'", r"f'", content)
            
            # Write back if changed
            if content != original_content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                fixed_files.append(file_path)
                print(f"✅ Fixed malformed prefixes in: {file_path}")
                for change in changes_made:
                    print(f"   {change}")
            else:
                print(f"📄 No malformed prefixes found: {file_path}")
                
        except Exception as e:
            print(f"❌ Error processing {file_path}: {e}")
    
    return fixed_files, all_issues_found

def test_syntax():
    """Test that all files have valid syntax after fixes."""
    
    loader_files = [
        "data/loaders/goldman_sachs.py",
        "data/loaders/oecd.py",
        "data/loaders/nvidia.py",
        "data/loaders/federal_reserve.py", 
        "data/loaders/academic.py",
        "data/loaders/mckinsey.py",
        "data/loaders/ai_index.py"
    ]
    
    print("\n🧪 Testing syntax...")
    
    syntax_errors = []
    
    for file_path in loader_files:
        if not os.path.exists(file_path):
            continue
            
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Try to compile the file
            compile(content, file_path, 'exec')
            print(f"   ✅ {os.path.basename(file_path)}: Syntax OK")
            
        except SyntaxError as e:
            syntax_errors.append((file_path, e))
            print(f"   ❌ {os.path.basename(file_path)}: Syntax Error - {e}")
        except Exception as e:
            print(f"   ⚠️  {os.path.basename(file_path)}: Other error - {e}")
    
    return syntax_errors

if __name__ == "__main__":
    print("🔧 Fixing all malformed string prefixes...")
    
    fixed, issues = fix_malformed_prefixes()
    
    print(f"\n📊 Summary:")
    print(f"   Fixed files: {len(fixed)}")
    print(f"   Issues found: {len(issues)}")
    
    if issues:
        print(f"\n🔍 Malformed patterns that were found:")
        for file_path, pattern in issues:
            print(f"   {os.path.basename(file_path)}: {pattern}")
    
    if fixed:
        print(f"\n✅ Fixed files:")
        for f in fixed:
            print(f"  - {f}")
    
    # Test syntax
    syntax_errors = test_syntax()
    
    if not syntax_errors:
        print(f"\n🎉 All files have valid syntax now!")
        print(f"\n🧪 Try running your app:")
        print(f"python app.py")
    else:
        print(f"\n⚠️  {len(syntax_errors)} files still have syntax errors:")
        for file_path, error in syntax_errors:
            print(f"   {os.path.basename(file_path)}: Line {error.lineno} - {error.msg}")
        
        print(f"\n💡 Consider restoring from backup and trying a different approach:")
        print(f"copy data\\loaders\\*.backup data\\loaders\\")