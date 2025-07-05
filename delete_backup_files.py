import os

files_to_delete = [
    "C:/Users/rcasa/OneDrive/Documents/AI-Adoption-Dashboard/app_backup.py",
    "C:/Users/rcasa/OneDrive/Documents/AI-Adoption-Dashboard/delete_temp_files.py"
]

for file_path in files_to_delete:
    if os.path.exists(file_path):
        os.remove(file_path)
        print(f"Deleted: {file_path}")
    else:
        print(f"File not found: {file_path}")
