#!/usr/bin/env python3
"""
Check for any interests that don't match the predefined list.
This helps identify potential typos or case mismatches.
"""

import os
import re
from pathlib import Path
from collections import defaultdict

# Predefined interests from the admin config
PREDEFINED_INTERESTS = {
    "anti-racism",
    "arts-culture",
    "book",
    "disability/neurodivergent",
    "education",
    "environment",
    "general",
    "health-wellness",
    "indigenous",
    "international",
    "lgbtq2s",
    "low-income",
    "seniors",
    "social-impact",
    "sports-rec",
    "tech",
    "urban-issues",
    "women+",
    "youth"
}

def extract_interests_from_file(file_path):
    """Extract interests from a markdown file."""
    interests = []
    try:
        with open(file_path, 'r') as f:
            content = f.read()
        
        # Find interests in frontmatter
        if content.startswith('---\n'):
            end = content.find('\n---\n', 4)
            if end > 0:
                frontmatter = content[4:end]
                
                # Find the interests line
                for line in frontmatter.split('\n'):
                    line = line.strip()
                    
                    # Skip if not interests line
                    if not line.startswith('interests:'):
                        continue
                    
                    # Handle empty interests
                    if line == 'interests:':
                        continue
                    
                    # Extract content after "interests:"
                    after_colon = line[10:].strip()  # Skip "interests:" (10 chars)
                    
                    # Single line array format: interests: ["item1", "item2"]
                    if after_colon.startswith('[') and after_colon.endswith(']'):
                        # Remove brackets and split
                        items_str = after_colon[1:-1]
                        if items_str:
                            items = items_str.split(',')
                            for item in items:
                                item = item.strip().strip('"')
                                if item:
                                    interests.append(item)
                    
                    # Single item format: interests: "item"
                    elif after_colon.startswith('"') and after_colon.endswith('"'):
                        item = after_colon[1:-1]
                        if item:
                            interests.append(item)
                    
                    # Empty array: interests: []
                    elif after_colon == '[]':
                        continue
    
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
    
    return interests

def main():
    """Check all organizations for interest mismatches."""
    base_dir = Path("src/content/organizations")
    
    # Track all interests found
    found_interests = defaultdict(list)
    # Track invalid interests
    invalid_interests = defaultdict(list)
    
    print("Checking all organization interests...\n")
    
    for org_file in base_dir.rglob("*.md"):
        interests = extract_interests_from_file(org_file)
        org_name = org_file.stem
        
        for interest in interests:
            found_interests[interest].append(org_name)
            if interest not in PREDEFINED_INTERESTS:
                invalid_interests[interest].append(org_name)
    
    # Print results
    print(f"Total predefined interests: {len(PREDEFINED_INTERESTS)}")
    print(f"Total interests found in files: {len(found_interests)}\n")
    
    # Check for invalid interests
    if invalid_interests:
        print("❌ INVALID INTERESTS FOUND:")
        for interest, orgs in sorted(invalid_interests.items()):
            print(f"  - '{interest}' in {len(orgs)} organization(s):")
            for org in orgs[:3]:  # Show first 3
                print(f"    • {org}")
            if len(orgs) > 3:
                print(f"    • ... and {len(orgs) - 3} more")
        print()
    else:
        print("✅ No invalid interests found!\n")
    
    # Check which predefined interests are not being used
    unused_interests = PREDEFINED_INTERESTS - set(found_interests.keys())
    if unused_interests:
        print("⚠️  Unused predefined interests:")
        for interest in sorted(unused_interests):
            print(f"  - {interest}")
    else:
        print("✅ All predefined interests are being used!\n")
    
    # Show count of each interest
    print("\nInterest usage count:")
    for interest in sorted(PREDEFINED_INTERESTS):
        count = len(found_interests.get(interest, []))
        print(f"  - {interest}: {count} organizations")

if __name__ == "__main__":
    main()
