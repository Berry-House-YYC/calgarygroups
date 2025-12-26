import os
import json
import re

def update_descriptions():
    descriptions_path = os.path.join('scripts', 'generated_descriptions', 'descriptions.json')
    orgs_dir = os.path.join('src', 'content', 'organizations')

    with open(descriptions_path, 'r', encoding='utf-8') as f:
        descriptions = json.load(f)

    print(f"Loaded {len(descriptions)} descriptions.")

    updated_count = 0
    fixed_format_count = 0

    # Iterate through all markdown files
    for root, dirs, files in os.walk(orgs_dir):
        for file in files:
            if file.endswith('.md'):
                file_path = os.path.join(root, file)
                
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                # FIX MALFORMED FRONTMATTER (Missing newline)
                if content.startswith('---layout:'):
                    content = content.replace('---layout:', '---\nlayout:', 1)
                    # We need to write this fix immediately so regex works
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    fixed_format_count += 1
                
                # Also handle other potential keys if layout isn't first
                elif re.match(r'^---[a-z]+:', content):
                     content = re.sub(r'^---([a-z]+):', r'---\n\1:', content, count=1)
                     with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                     fixed_format_count += 1

                # Extract Frontmatter
                # Relaxed regex to be more robust
                match = re.search(r'^---\n(.*?)\n---', content, re.DOTALL)
                if match:
                    frontmatter_raw = match.group(1)
                    
                    # Extract Name (Quoted or Unquoted)
                    # Look for name: followed by quote or just text until newline
                    name_match = re.search(r'name:\s*(?:"(.*?)"|(.*?))(\n|$)', frontmatter_raw)
                    
                    if name_match:
                        # group(1) is quoted content, group(2) is unquoted content
                        name = name_match.group(1) or name_match.group(2)
                        name = name.strip()
                        
                        if name in descriptions:
                            description = descriptions[name]
                            
                            # Check if description is already there
                            # We check for a substring of the description
                            desc_snippet = description[:50]
                            # Escape for regex check just in case
                            if desc_snippet in frontmatter_raw:
                                # print(f"Skipping {name}, already updated.")
                                continue

                            # Update Frontmatter
                            # Escape double quotes in description
                            desc_escaped = description.replace('"', '\\"')
                            new_frontmatter = frontmatter_raw.rstrip() + f'\ndescription: "{desc_escaped}"\n'
                            
                            # Reconstruct content
                            # Add description to the body as well, at the top
                            body = content[match.end():] # Everything after the second ---
                            if body.startswith('\n'):
                                body = body[1:] # Remove leading newline if present from split
                            
                            # Remove "Focused on..." line if it exists
                            body = re.sub(r'Focused on .*?(\n|$)', '', body, flags=re.IGNORECASE).strip()
                            
                            new_body = f"{description}\n\n{body}\n"
                            
                            new_content = f"---\n{new_frontmatter}---\n\n{new_body}"
                            
                            with open(file_path, 'w', encoding='utf-8') as f:
                                f.write(new_content)
                            
                            updated_count += 1
                            print(f"Updated {name}")
                        else:
                            # print(f"Description not found for {name}")
                            pass
                    else:
                        print(f"Could not find name in {file_path}")
                else:
                    print(f"Invalid markdown format in {file_path}")

    print(f"Fixed formatting in {fixed_format_count} files.")
    print(f"Undated descriptions in {updated_count} files.")

if __name__ == "__main__":
    update_descriptions()
