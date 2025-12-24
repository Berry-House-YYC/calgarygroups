import os
import json
import re

def apply_refined_descriptions():
    refined_path = os.path.join('scripts', 'generated_descriptions', 'refined_descriptions.json')
    old_path = os.path.join('scripts', 'generated_descriptions', 'descriptions.json')
    orgs_dir = os.path.join('src', 'content', 'organizations')

    with open(refined_path, 'r', encoding='utf-8') as f:
        refined_data = json.load(f)

    try:
        with open(old_path, 'r', encoding='utf-8') as f:
            old_data = json.load(f)
    except FileNotFoundError:
        old_data = {}

    # Map fileBasename (derived from name slug) to file path? 
    # Or just iterate all files and check name?
    # Better to iterate all files once to build a map of Name -> FilePath
    
    name_to_file = {}
    for root, dirs, files in os.walk(orgs_dir):
        for file in files:
            if file.endswith('.md'):
                path = os.path.join(root, file)
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Extract Name
                name_match = re.search(r'^name:\s*(?:"(.*?)"|(.*?))$', content, re.MULTILINE)
                if name_match:
                    name = (name_match.group(1) or name_match.group(2)).strip()
                    name_to_file[name] = path

    updated_count = 0
    
    for org_name, new_desc in refined_data.items():
        if org_name not in name_to_file:
            print(f"Skipping {org_name}: File not found.")
            continue
            
        file_path = name_to_file[org_name]
        old_desc = old_data.get(org_name, "")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 1. Update Frontmatter
        # Regex to find description line
        desc_pattern = r'(^description:\s*)(?:"(?:[^"\\]|\\.)*"|.*?)$'
        
        # Check if description exists in frontmatter
        if re.search(desc_pattern, content, re.MULTILINE):
            # Replace existing
            new_line = f'description: "{new_desc}"'
            content = re.sub(desc_pattern, new_line, content, count=1, flags=re.MULTILINE)
        else:
            # Add to end of frontmatter (before last ---)
            # Find the second ---
            parts = content.split('---')
            if len(parts) >= 3:
                frontmatter = parts[1]
                if not frontmatter.strip().endswith('\n'):
                    frontmatter += '\n'
                frontmatter += f'description: "{new_desc}"\n'
                parts[1] = frontmatter
                content = '---'.join(parts)
        
        # 2. Update Body
        # If old description is in body, replace it
        if old_desc and old_desc in content:
            content = content.replace(old_desc, new_desc)
        elif new_desc not in content:
            # If new description is NOT in body, insert it.
            # Try to insert after frontmatter
            parts = content.split('---', 2)
            if len(parts) >= 3:
                body = parts[2]
                # Insert at top of body, ensuring blank lines
                body = f"\n\n{new_desc}\n\n" + body.lstrip()
                content = f"---{parts[1]}---{body}"
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
            
        print(f"Updated {org_name}")
        updated_count += 1

    print(f"Update complete. Modified {updated_count} files.")

if __name__ == "__main__":
    apply_refined_descriptions()
