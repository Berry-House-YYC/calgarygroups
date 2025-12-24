import os
import re

def migrate_contact_info():
    orgs_dir = os.path.join('src', 'content', 'organizations')
    files_fixed = 0
    
    print(f"Scanning directory: {orgs_dir}...\n")

    for root, dirs, files in os.walk(orgs_dir):
        for file in files:
            if not file.endswith('.md'):
                continue
            
            file_path = os.path.join(root, file)
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Regex to find **Contact Info:** and subsequent list items
            # It captures:
            # 1. The "**Contact Info:**" line
            # 2. Any list items starting with "- Website:" or "- Email:" or "- Social:"
            # It stops when it hits a blank line or "Notes:" or end of file
            
            pattern = r'\*\*Contact Info:\*\*\n((?:- .+\n?)+)'
            match = re.search(pattern, content)
            
            if match:
                list_block = match.group(1)
                
                # Parse the list items
                new_lines = [
                    '<div class="org-contact-info">',
                    '  <strong>Contact Info:</strong>',
                    '  <ul class="list-none pl-0">'
                ]
                
                for line in list_block.strip().split('\n'):
                    line = line.strip()
                    if line.startswith('- Website:'):
                         url = line.replace('- Website:', '').strip()
                         new_lines.append(f'    <li>Website: <a href="{url}" target="_blank">{url}</a></li>')
                    elif line.startswith('- Email:'):
                         email = line.replace('- Email:', '').strip()
                         new_lines.append(f'    <li>Email: <a href="mailto:{email}">{email}</a></li>')
                    elif line.startswith('- Social:'):
                         # Handle social if present (rare case from earlier example)
                         social = line.replace('- Social:', '').strip()
                         new_lines.append(f'    <li>Social: {social}</li>')
                
                new_lines.append('  </ul>')
                new_lines.append('</div>')
                
                new_block = '\n'.join(new_lines)
                
                # Replace the old block with new HTML block
                new_content = content.replace(match.group(0).strip(), new_block)
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                
                files_fixed += 1
                print(f"Migrated {file}")

    print(f"\nMigration complete. Updated {files_fixed} files.")

if __name__ == "__main__":
    migrate_contact_info()
