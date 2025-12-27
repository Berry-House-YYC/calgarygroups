#!/usr/bin/env python3
"""
Add 'book' interest to organizations that are clearly book clubs.
This script updates organizations that have 'book' or 'book club' in their name
or are obviously book-related.
"""

import os
import re
from pathlib import Path

def update_frontmatter(file_path, add_book=False):
    """Update the frontmatter of a markdown file."""
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Split frontmatter and content
    if content.startswith('---\n'):
        try:
            end = content.index('\n---\n', 4)
            frontmatter_str = content[4:end]
            body = content[end+5:]
            
            # Parse YAML
            frontmatter = yaml.safe_load(frontmatter_str)
            
            # Add book interest if needed
            if add_book and 'interests' in frontmatter:
                if isinstance(frontmatter['interests'], list):
                    if 'book' not in frontmatter['interests']:
                        frontmatter['interests'].append('book')
                        frontmatter['interests'].sort()
                        print(f"Added 'book' interest to {file_path.name}")
                        
                        # Write back
                        new_frontmatter = yaml.dump(frontmatter, default_flow_style=False, sort_keys=False)
                        new_content = f'---\n{new_frontmatter}---\n{body}'
                        
                        with open(file_path, 'w') as f:
                            f.write(new_content)
                        return True
                elif isinstance(frontmatter['interests'], str):
                    # Convert single string to list
                    interests = [frontmatter['interests']]
                    if 'book' not in interests:
                        interests.append('book')
                        interests.sort()
                        frontmatter['interests'] = interests
                        print(f"Added 'book' interest to {file_path.name}")
                        
                        new_frontmatter = yaml.dump(frontmatter, default_flow_style=False, sort_keys=False)
                        new_content = f'---\n{new_frontmatter}---\n{body}'
                        
                        with open(file_path, 'w') as f:
                            f.write(new_content)
                        return True
        except Exception as e:
            print(f"Error processing {file_path}: {e}")
    
    return False

def main():
    """Main function to update book clubs."""
    base_dir = Path("src/content/organizations")
    updated_count = 0
    
    # Patterns that clearly indicate a book club
    book_patterns = [
        r'book\s*club',
        r'bookworms?',
        r'book\s*meetup',
        r'literary\s*club',
        r'reading\s*club',
        r'page\s*turners',
        r'queerreads',
        r'manga\s*club',
        r'intentional\s*book',
        r'violet\s*book',
        r'ladies\s*that\s*read',
        r'monthly\s*manga',
        r'just\s*read',
        r'sunday\s*book'
    ]
    
    for org_file in base_dir.rglob("*.md"):
        # Check if it's a clear book club based on name
        name_check = org_file.stem.lower().replace('-', ' ')
        is_book_club = any(re.search(pattern, name_check) for pattern in book_patterns)
        
        # Also check the actual organization name in frontmatter
        if not is_book_club:
            try:
                with open(org_file, 'r') as f:
                    content = f.read()
                    if content.startswith('---\n'):
                        end = content.index('\n---\n', 4)
                        frontmatter_str = content[4:end]
                        frontmatter = yaml.safe_load(frontmatter_str)
                        if 'name' in frontmatter:
                            org_name = frontmatter['name'].lower()
                            is_book_club = any(re.search(pattern, org_name) for pattern in book_patterns)
            except:
                pass
        
        if is_book_club:
            if update_frontmatter(org_file, add_book=True):
                updated_count += 1
    
    print(f"\nUpdated {updated_count} organizations with 'book' interest")

if __name__ == "__main__":
    main()
