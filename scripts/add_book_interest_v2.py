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
        lines = f.readlines()
    
    # Find frontmatter boundaries
    if lines and lines[0].strip() == '---':
        # Find end of frontmatter
        end_idx = -1
        for i in range(1, len(lines)):
            if lines[i].strip() == '---':
                end_idx = i
                break
        
        if end_idx > 0:
            # Process frontmatter lines
            frontmatter_lines = lines[1:end_idx]
            in_interests = False
            interests_idx = -1
            interests_line = None
            
            # Find interests line
            for i, line in enumerate(frontmatter_lines):
                if line.strip().startswith('interests:'):
                    in_interests = True
                    interests_idx = i
                    interests_line = line
                    break
            
            if add_book and interests_idx >= 0:
                # Check if book is already in interests
                if 'book' not in interests_line:
                    # Parse existing interests
                    if interests_line.strip() == 'interests:':
                        # Empty list case
                        frontmatter_lines[interests_idx] = 'interests: ["book"]\n'
                    elif interests_line.strip().startswith('interests: ['):
                        # List case - add book to the list
                        content = interests_line.strip()
                        if content.endswith(']'):
                            # Remove closing bracket
                            content = content[:-1]
                            if not content.endswith('['):
                                content += ', '
                            content += '"book"]\n'
                            frontmatter_lines[interests_idx] = content
                    elif '"' in interests_line:
                        # Single string case - convert to list
                        match = re.search(r'"([^"]+)"', interests_line)
                        if match:
                            existing = match.group(1)
                            frontmatter_lines[interests_idx] = f'interests: ["{existing}", "book"]\n'
                    
                    print(f"Added 'book' interest to {file_path.name}")
                    
                    # Reconstruct file
                    new_lines = ['---\n'] + frontmatter_lines + ['---\n'] + lines[end_idx+1:]
                    
                    with open(file_path, 'w') as f:
                        f.writelines(new_lines)
                    return True
    
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
        r'sunday\s*book',
        r'paperback\s*therapy'
    ]
    
    for org_file in base_dir.rglob("*.md"):
        # Check if it's a clear book club based on filename
        name_check = org_file.stem.lower().replace('-', ' ')
        is_book_club = any(re.search(pattern, name_check) for pattern in book_patterns)
        
        if is_book_club:
            if update_frontmatter(org_file, add_book=True):
                updated_count += 1
    
    print(f"\nUpdated {updated_count} organizations with 'book' interest")

if __name__ == "__main__":
    main()
