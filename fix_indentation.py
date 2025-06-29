import re

# Read the file
with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Find the problematic section and fix indentation
# The issue is that lines after "elif current_view == "💰 Investment Case":" are not properly indented

# Split the content into lines
lines = content.split('\n')

# Find the start of the Investment Case section
investment_case_start = None
for i, line in enumerate(lines):
    if 'elif current_view == "💰 Investment Case":' in line:
        investment_case_start = i
        break

if investment_case_start is not None:
    # Find where this section ends (next elif or else)
    investment_case_end = None
    for i in range(investment_case_start + 1, len(lines)):
        if lines[i].strip().startswith('elif ') or lines[i].strip().startswith('else:'):
            investment_case_end = i
            break
    
    if investment_case_end is None:
        investment_case_end = len(lines)
    
    # Fix indentation for all lines in this section
    for i in range(investment_case_start + 1, investment_case_end):
        line = lines[i]
        # Skip empty lines
        if line.strip() == '':
            continue
        # Add proper indentation (8 spaces or 2 levels)
        if not line.startswith('    '):
            lines[i] = '        ' + line.lstrip()

# Write the fixed content back
with open('app.py', 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines))

print("Indentation fixed!") 