import os

def check_migration():
    orgs_dir = os.path.join('src', 'content', 'organizations')
    missing_class = []
    
    print(f"Scanning directory: {orgs_dir}...\n")

    for root, dirs, files in os.walk(orgs_dir):
        for file in files:
            if not file.endswith('.md'):
                continue
            
            file_path = os.path.join(root, file)
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
    print(f"Found {len(missing_class)} files missing the class:")
    for f in missing_class:
        print(f"- {f}")

if __name__ == "__main__":
    check_migration()
