#!/usr/bin/env python3
import os
import glob
import re

# Find all markdown files
files = glob.glob(r'src\content\organizations\**\*.md', recursive=True)

fixed_count = 0
for filepath in files:
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Split frontmatter and body
        match = re.match(r'(---.*?---\n)(.*)', content, re.DOTALL)
        if not match:
            continue
            
        frontmatter = match.group(1)
        body = match.group(2)
        
        # Replace double quotes with single quotes in body only
        new_body = body.replace('"', "'")
        
        if new_body != body:
            new_content = frontmatter + new_body
            with open(filepath, 'w', encoding='utf-8', newline='') as f:
                f.write(new_content)
            fixed_count += 1
            print(f"Fixed: {os.path.basename(filepath)}")
    except Exception as e:
        print(f"Error processing {filepath}: {e}")

print(f"\nProcessed {len(files)} files, fixed {fixed_count} files")
