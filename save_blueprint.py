import os
import json

path = r"C:\Users\shyam\.gemini\antigravity\brain\0b69a188-ffdf-4bb1-acb7-45e6ea5edd18\.system_generated\logs\transcript.jsonl"
out_path = r"C:\Users\shyam\.gemini\antigravity\scratch\original_blueprint.md"

if os.path.exists(path):
    print("Reading transcript.jsonl...")
    with open(path, 'r', encoding='utf-8') as f:
        for idx, line in enumerate(f):
            if idx == 4354:
                try:
                    obj = json.loads(line)
                    content = obj.get('content', '')
                    with open(out_path, 'w', encoding='utf-8') as out_f:
                        out_f.write(content)
                    print(f"Successfully saved blueprint to {out_path}")
                except Exception as e:
                    print(f"Error parsing json: {e}")
                break
else:
    print("Path does not exist")
