import os
import re

def fix_newlines():
    orgs_dir = os.path.join('src', 'content', 'organizations')
    count = 0
    
    for root, dirs, files in os.walk(orgs_dir):
        for file in files:
            if file.endswith('.md'):
                path = os.path.join(root, file)
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                original_content = content
                
                # Ensure newline before the closing --- of frontmatter
                # We target the --- that is NOT at the start of the file
                # Simplest way: Split by ---, ensure the middle part ends with newline
                
                parts = content.split('---')
                if len(parts) >= 3:
                    # parts[0] is empty (before first ---)
                    # parts[1] is frontmatter
                    # parts[2] is body
                    
                    if not parts[1].endswith('\n'):
                        parts[1] += '\n'
                        content = '---'.join(parts)
                
                if content != original_content:
                    with open(path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    count += 1

    print(f"Fixed newlines in {count} files.")

if __name__ == "__main__":
    fix_newlines()
