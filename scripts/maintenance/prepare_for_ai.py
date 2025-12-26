import json
import os

def prepare_data():
    input_path = os.path.join('scripts', 'scraped_content', 'scraped_data.json')
    output_path = os.path.join('scripts', 'scraped_content', 'ai_input.json')
    
    with open(input_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    prepared = []
    for item in data:
        if not item.get('success'):
            continue
            
        # Combine title, meta description and start of main text
        parts = []
        if item.get('title'):
            parts.append(f"Title: {item['title']}")
        if item.get('meta_description'):
            parts.append(f"Meta: {item['meta_description']}")
        
        main_text = item.get('main_text', '')
        # Clean up excessive whitespace
        main_text = ' '.join(main_text.split())
        # Take first 1000 chars as context
        parts.append(f"Content: {main_text[:1000]}")
        
        context = " | ".join(parts)
        
        prepared.append({
            "name": item['name'],
            "context": context
        })
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(prepared, f, indent=2, ensure_ascii=False)
    
    print(f"Prepared {len(prepared)} items for AI processing")

if __name__ == "__main__":
    prepare_data()
