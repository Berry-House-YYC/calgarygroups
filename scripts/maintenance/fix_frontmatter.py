import os
import re

def fix_frontmatter():
    orgs_dir = os.path.join('src', 'content', 'organizations')
    count = 0
    
    for root, dirs, files in os.walk(orgs_dir):
        for file in files:
            if file.endswith('.md'):
                path = os.path.join(root, file)
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                original_content = content
                
                # 1. Fix mashed permalink/description
                # Matches: permalink: "..."description: "..."
                # or permalink: "..." description: "..."
                # We want to insert a newline.
                
                # Pattern: Look for permalink, then closing quote, then description
                # Note: `permalink` value might end with `/`.
                
                mashed_pattern = r'(permalink:.*?)"description:'
                if re.search(mashed_pattern, content):
                    content = re.sub(mashed_pattern, r'\1"\ndescription:', content)
                
                # Also check for "description" without quotes if it was unquoted
                mashed_pattern_2 = r'(permalink:.*?)description:'
                # Be careful not to match the one we just fixed if we didn't use correct lookbehind? 
                # The previous sub adds \n.
                # Let's just iterate lines to be safer? No, regex is fine if specific.
                
                # 2. Deduplicate description in frontmatter
                # If we have multiple `description:` lines between the first two `---`.
                parts = content.split('---')
                if len(parts) >= 3:
                    frontmatter = parts[1]
                    lines = frontmatter.split('\n')
                    new_lines = []
                    desc_lines = []
                    
                    for line in lines:
                        if line.strip().startswith('description:'):
                            desc_lines.append(line)
                        else:
                            new_lines.append(line)
                    
                    # If multiple descriptions, keep the last one (which should be the refined one)
                    if desc_lines:
                        # Add the last description line to the end of new_lines
                        new_lines.append(desc_lines[-1])
                    
                    parts[1] = '\n'.join(new_lines)
                    content = '---'.join(parts)
                
                if content != original_content:
                    with open(path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    print(f"Fixed {file}")
                    count += 1

    print(f"Fixed formatting in {count} files.")

if __name__ == "__main__":
    fix_frontmatter()
