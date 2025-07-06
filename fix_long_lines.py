import os
import re

MAX_LINE_LENGTH = 100
MAX_RECURSION_DEPTH = 10
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))


def break_long_line(line, depth=0):
    if len(line) <= MAX_LINE_LENGTH or depth > MAX_RECURSION_DEPTH:
        return [line]
    # Try to break at the last space or comma before the limit
    break_points = [m.start() for m in re.finditer(r'[ ,]', line[:MAX_LINE_LENGTH])]
    if not break_points:
        # No good break point, or already indented, return as-is to avoid infinite recursion
        return [line]
    split_at = break_points[-1] + 1
    match = re.match(r'\s*', line)
    indent = (match.group(0) if match else '') + '    '
    first = line[:split_at].rstrip() + '\n'
    rest = indent + line[split_at:].lstrip()
    # If rest is not shorter, avoid recursion
    if len(rest) >= len(line):
        return [line]
    return [first] + break_long_line(rest, depth + 1)


def fix_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    new_lines = []
    for line in lines:
        # Only process code lines, skip docstrings and comments for safety
        if (len(line) > MAX_LINE_LENGTH and not line.strip().startswith('#') and not re.match(r'\s*[\'\"]', line.strip())):
            new_lines.extend(break_long_line(line))
        else:
            new_lines.append(line)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)


def fix_project(root):
    for dirpath, _, filenames in os.walk(root):
        for filename in filenames:
            if filename.endswith('.py') and filename not in ('fix_long_lines.py', 'cleanup_whitespace.py'):
                filepath = os.path.join(dirpath, filename)
                fix_file(filepath)


if __name__ == '__main__':
    fix_project(PROJECT_ROOT)
    print('Long line fix complete. Please manually review changes for correctness, especially for strings and comments.') 