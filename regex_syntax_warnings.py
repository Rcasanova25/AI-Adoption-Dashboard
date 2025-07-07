"""Fix regex syntax warnings in loader files."""
import os
import re
from pathlib import Path


def fix_regex_patterns():
    """Fix invalid regex escape sequences in all loader files."""
    
    loader_files = [
        "data/loaders/goldman_sachs.py",
        "data/loaders/oecd.py",
        "data/loaders/nvidia.py",
        "data/loaders/federal_reserve.py", 
        "data/loaders/academic.py",
        "data/loaders/mckinsey.py",
        "data/loaders/ai_index.py"
    ]
    
    # Pattern replacements to fix regex warnings
    fixes = [
        # Fix double backslashes in regex patterns (be more specific to avoid false positives)
        (r'\\\\d(?=[+*?})\]]|$)', r'\\d'),
        (r'\\\\s(?=[+*?})\]]|$)', r'\\s'),
        (r'\\\\w(?=[+*?})\]]|$)', r'\\w'),
        (r'\\\\(?=[()\[\]{}+*?.])', r'\\'),
        
        # Fix common regex escape sequences
        (r'\\\\(\d+)', r'\\\\\1'),  # Don't change octal sequences
        
        # Fix f-strings that should be raw f-strings (rf"...")
        # Only add 'r' if not already present
        (r'(?<!r)f"([^"]*(?:\\[dswDSW\[\](){}+*?.|])+[^"]*)"', r'rf"\1"'),
        (r"(?<!r)f'([^']*(?:\\[dswDSW\[\](){}+*?.|])+[^']*)'", r"rf'\1'"),
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
                    changes_made.append(f"Applied pattern: {pattern[:50]}...")
            
            # Additional specific fixes for common problematic patterns
            additional_fixes = [
                # Fix string literals that should be raw strings when containing regex
                (r'("[^"]*\\[dswDSW\[\](){}+*?.|]+[^"]*")', lambda m: 'r' + m.group(1) if not m.group(1).startswith('r"') and not m.group(1).startswith('f"') else m.group(1)),
                (r"('[^']*\\[dswDSW\[\](){}+*?.|]+[^']*')", lambda m: 'r' + m.group(1) if not m.group(1).startswith("r'") and not m.group(1).startswith("f'") else m.group(1)),
            ]
            
            for pattern, replacement in additional_fixes:
                if callable(replacement):
                    content = re.sub(pattern, replacement, content)
                else:
                    content = re.sub(pattern, replacement, content)
            
            # Check for remaining problematic patterns and warn
            problematic_patterns = [
                r'f"[^"]*\\[dswDSW\[\](){}+*?.|]+[^"]*"',  # f-strings with regex that weren't fixed
                r"f'[^']*\\[dswDSW\[\](){}+*?.|]+[^']*'",
                r'"[^"]*\\[dswDSW\[\](){}+*?.|]+[^"]*"',   # Non-raw strings with regex
                r"'[^']*\\[dswDSW\[\](){}+*?.|]+[^']*'",
            ]
            
            remaining_issues = []
            for pattern in problematic_patterns:
                matches = re.findall(pattern, content)
                if matches:
                    remaining_issues.extend(matches)
            
            # Write back if changed
            if content != original_content:
                # Create backup
                backup_path = file_path + '.backup'
                with open(backup_path, 'w', encoding='utf-8') as f:
                    f.write(original_content)
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                fixed_files.append(file_path)
                print(f"✅ Fixed regex patterns in: {file_path}")
                print(f"   Backup created: {backup_path}")
                
                if changes_made:
                    print(f"   Changes: {len(changes_made)} pattern fixes applied")
                
                if remaining_issues:
                    print(f"   ⚠️  {len(remaining_issues)} potential issues remain (manual review needed)")
                    for issue in remaining_issues[:3]:  # Show first 3
                        print(f"      {issue}")
                    if len(remaining_issues) > 3:
                        print(f"      ... and {len(remaining_issues) - 3} more")
            else:
                print(f"📄 No changes needed: {file_path}")
                
        except Exception as e:
            print(f"❌ Error processing {file_path}: {e}")
    
    return fixed_files


def validate_regex_patterns(file_path):
    """Validate that regex patterns in a file are syntactically correct."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find potential regex patterns
        regex_patterns = []
        
        # Look for re.compile, re.search, re.match, etc.
        for match in re.finditer(r're\.\w+\s*\(\s*[rf]*["\']([^"\']+)["\']', content):
            regex_patterns.append(match.group(1))
        
        # Look for patterns in string literals that look like regex
        for match in re.finditer(r'[rf]*["\']([^"\']*\\[dswDSW\[\](){}+*?.|]+[^"\']*)["\']', content):
            regex_patterns.append(match.group(1))
        
        invalid_patterns = []
        for pattern in regex_patterns:
            try:
                re.compile(pattern)
            except re.error as e:
                invalid_patterns.append((pattern, str(e)))
        
        return invalid_patterns
        
    except Exception as e:
        print(f"Error validating {file_path}: {e}")
        return []


if __name__ == "__main__":
    print("🔧 Fixing regex syntax warnings...")
    fixed = fix_regex_patterns()
    print(f"\n✅ Fixed {len(fixed)} files")
    
    if fixed:
        print("\nFixed files:")
        for f in fixed:
            print(f"  - {f}")
        
        print("\n🔍 Validating fixed files...")
        for file_path in fixed:
            invalid_patterns = validate_regex_patterns(file_path)
            if invalid_patterns:
                print(f"⚠️  {file_path} still has invalid patterns:")
                for pattern, error in invalid_patterns:
                    print(f"   Pattern: {pattern}")
                    print(f"   Error: {error}")
            else:
                print(f"✅ {file_path} validation passed")
    
    print("\n🎯 Recommendation: Review the backup files and test your loaders before committing changes.")