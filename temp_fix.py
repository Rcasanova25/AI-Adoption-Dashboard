# Read the original file
with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Find the start and end of the problematic section
start_marker = '    elif current_view == "💰 Investment Case":'
end_marker = '    elif current_view == "📊 Market Intelligence":'

# Split content
parts = content.split(start_marker)
if len(parts) > 1:
    before_section = parts[0] + start_marker
    
    # Find the end of the investment case section
    remaining = parts[1]
    end_parts = remaining.split(end_marker)
    
    if len(end_parts) > 1:
        after_section = end_marker + end_parts[1]
        
        # The problematic section content
        problematic_section = end_parts[0]
        
        # Fix the indentation by adding 4 spaces to each line
        lines = problematic_section.split('\n')
        fixed_lines = []
        
        for line in lines:
            if line.strip() == '':
                fixed_lines.append('')
            else:
                # Add 4 spaces if not already indented
                if not line.startswith('    '):
                    fixed_lines.append('    ' + line.lstrip())
                else:
                    fixed_lines.append(line)
        
        fixed_section = '\n'.join(fixed_lines)
        
        # Reconstruct the file
        new_content = before_section + '\n' + fixed_section + '\n' + after_section
        
        # Write back
        with open('app.py', 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print("Fixed indentation!")
    else:
        print("Could not find end marker")
else:
    print("Could not find start marker") 