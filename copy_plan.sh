#!/bin/bash
# Script to copy all changes from WSL to OneDrive

WSL_DIR="/home/rcasa/AI-Adoption-Dashboard"
ONEDRIVE_DIR="/mnt/c/Users/rcasa/OneDrive/Documents/AI-Adoption-Dashboard"

echo "=== Copy Plan for AI-Adoption-Dashboard ==="
echo "From: $WSL_DIR"
echo "To: $ONEDRIVE_DIR"
echo ""

# Get all modified files
echo "=== Modified Files ==="
git status --porcelain | grep "^ M " | awk '{print $2}' > modified_files.txt
cat modified_files.txt
echo ""

# Get all new/untracked files
echo "=== New Files ==="
git status --porcelain | grep "^?? " | awk '{print $2}' > new_files.txt
cat new_files.txt
echo ""

# Get all deleted files
echo "=== Deleted Files ==="
git status --porcelain | grep "^ D " | awk '{print $2}' > deleted_files.txt
cat deleted_files.txt

# Count files
MODIFIED_COUNT=$(wc -l < modified_files.txt)
NEW_COUNT=$(wc -l < new_files.txt)
DELETED_COUNT=$(wc -l < deleted_files.txt)

echo ""
echo "=== Summary ==="
echo "Modified files: $MODIFIED_COUNT"
echo "New files: $NEW_COUNT"
echo "Deleted files: $DELETED_COUNT"
echo "Total changes: $((MODIFIED_COUNT + NEW_COUNT + DELETED_COUNT))"