import os
import re
import yaml
import sys

# Requirements
REQUIRED_FRONTMATTER = {
    'layout': str,
    'name': str,
    'type': str,
    'interests': list,
    'age_range': str,
    'identity_focused': bool, 
    'meeting_format': str,
    'location_area': str, 
    'status': str,
    'permalink': str
}

VALID_TYPES = [
    'Nonprofit', 'Grassroots', 'Social Club', 'Chapter', 
    'Small Business', 'Cooperative'
]

VALID_INTERESTS = [
    'lgbtq2s', 'anti-racism', 'arts-culture', 'youth', 
    'disability/neurodivergent', 'environment', 'health-wellness', 
    'indigenous', 'low-income', 'tech', 'seniors', 
    'social-impact', 'sports-rec', 'urban-issues', 'women+', 
    # New ones added:
    'book', 'general'
]

def validate_org_files():
    orgs_dir = os.path.join('src', 'content', 'organizations')
    files_checked = 0
    errors = []

    print(f"Scanning directory: {orgs_dir}...\n")

    for root, dirs, files in os.walk(orgs_dir):
        for file in files:
            if not file.endswith('.md'):
                continue
            
            files_checked += 1
            file_path = os.path.join(root, file)
            # relative path for cleaner output
            rel_path = os.path.relpath(file_path, orgs_dir)

            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                # 1. Parse Frontmatter
                # Split by ---, assume first block is frontmatter
                parts = content.split('---', 2)
                if len(parts) < 3:
                     errors.append(f"{rel_path}: Invalid frontmatter structure (missing --- delimiters)")
                     continue
                
                raw_frontmatter = parts[1]
                body = parts[2]

                try:
                    data = yaml.safe_load(raw_frontmatter)
                except yaml.YAMLError as e:
                    errors.append(f"{rel_path}: YAML parsing error: {e}")
                    continue
                
                if not data:
                    errors.append(f"{rel_path}: Empty frontmatter")
                    continue

                # 2. Schema Validation
                for key, expected_type in REQUIRED_FRONTMATTER.items():
                    if key not in data:
                        errors.append(f"{rel_path}: Missing required field '{key}'")
                    elif not isinstance(data[key], expected_type):
                        errors.append(f"{rel_path}: Field '{key}' has wrong type. Expected {expected_type}, got {type(data[key])}")

                # Validate Type
                if 'type' in data and data['type'] not in VALID_TYPES:
                    errors.append(f"{rel_path}: Invalid type '{data['type']}'")
                
                # Validate Interests
                if 'interests' in data:
                    for interest in data['interests']:
                        if interest not in VALID_INTERESTS:
                             errors.append(f"{rel_path}: Invalid interest '{interest}'")

                # 3. Content Validation
                
                # Check Description
                # Description can be in frontmatter OR body
                desc_valid = False
                
                # Check frontmatter description
                if 'description' in data and data['description'] and len(data['description']) > 20:
                    desc_valid = True
                
                # Check body for description-like text (non-contact info)
                # Naive check: does body have text that isn't **Contact Info**?
                # Usually our body starts with description text
                if not desc_valid:
                    # Strip whitespace
                    clean_body = body.strip()
                    # Remove "Contact Info" section
                    clean_body = re.sub(r'\*\*Contact Info:\*\*.*', '', clean_body, flags=re.DOTALL)
                    if len(clean_body.strip()) > 20:
                        desc_valid = True
                
                if not desc_valid:
                     errors.append(f"{rel_path}: Missing or too short description (< 20 chars)")

                # Check Contact Info
                if "Contact Info" not in body and "Website" not in body and "http" not in body:
                     errors.append(f"{rel_path}: Missing contact info/website link")

            except Exception as e:
                errors.append(f"{rel_path}: Unexpected error: {e}")

    # Report
    print(f"Checked {files_checked} files.")
    
    if errors:
        print(f"\nFound {len(errors)} issues:")
        for err in errors:
            print(f" - {err}")
        sys.exit(1)
    else:
        print("\n[SUCCESS] All organization files passed validation!")
        sys.exit(0)

if __name__ == "__main__":
    validate_org_files()
