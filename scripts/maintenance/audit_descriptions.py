import os
import re
import json

def audit_descriptions():
    orgs_dir = os.path.join('src', 'content', 'organizations')
    scraped_data_path = os.path.join('scripts', 'scraped_content', 'scraped_data.json')
    
    with open(scraped_data_path, 'r', encoding='utf-8') as f:
        scraped_data = json.load(f)
        
    # Map name to URL for reference
    name_to_url = {item['name']: item['url'] for item in scraped_data}

    missing_desc = []
    empty_desc = []
    weak_desc = [] # Contains "Instagram" or "social media"
    
    count = 0
    for root, dirs, files in os.walk(orgs_dir):
        for file in files:
            if file.endswith('.md'):
                count += 1
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Extract Name
                name_match = re.search(r'name:\s*(?:"(.*?)"|(.*?))(\n|$)', content)
                if name_match:
                     name = name_match.group(1) or name_match.group(2)
                     name = name.strip()
                else:
                    name = "Unknown"

                # Extract Description
                desc_match = re.search(r'description:\s*"(.*?)"', content)
                if not desc_match:
                    # Check for unquoted description
                    desc_match = re.search(r'description:\s*([^\n"]+)', content)
                
                if not desc_match:
                    missing_desc.append(name)
                else:
                    description = desc_match.group(1).strip()
                    if not description:
                        empty_desc.append(name)
                    elif "instagram" in description.lower() or "social media" in description.lower():
                        weak_desc.append((name, description))

    print(f"Scanned {count} files.")
    print(f"Missing Descriptions ({len(missing_desc)}):")
    for name in missing_desc:
        print(f" - {name} ({name_to_url.get(name, 'No URL')})")
        
    print(f"\nEmpty Descriptions ({len(empty_desc)}):")
    for name in empty_desc:
        print(f" - {name} ({name_to_url.get(name, 'No URL')})")

    print(f"\nWeak/Placeholder Descriptions ({len(weak_desc)}):")
    for name, desc in weak_desc:
        print(f" - {name}: {desc} ({name_to_url.get(name, 'No URL')})")

if __name__ == "__main__":
    audit_descriptions()
