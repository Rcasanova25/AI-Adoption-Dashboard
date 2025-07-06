import os

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))


def clean_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    cleaned = []
    for line in lines:
        # Remove trailing whitespace
        cleaned_line = line.rstrip()
        # Only keep blank lines if they are truly empty
        if cleaned_line == '':
            cleaned.append('\n')
        else:
            cleaned.append(cleaned_line + '\n')
    with open(filepath, 'w', encoding='utf-8') as f:
        f.writelines(cleaned)


def clean_project(root):
    for dirpath, _, filenames in os.walk(root):
        for filename in filenames:
            if filename.endswith('.py'):
                filepath = os.path.join(dirpath, filename)
                clean_file(filepath)


if __name__ == '__main__':
    clean_project(PROJECT_ROOT)
    print('Whitespace cleanup complete.')
