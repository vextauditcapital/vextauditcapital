import os
import json

path = r"C:\Users\shyam\.gemini\antigravity\brain\0b69a188-ffdf-4bb1-acb7-45e6ea5edd18\.system_generated\logs\transcript.jsonl"
if not os.path.exists(path):
    print(f"Log file not found at {path}")
else:
    print("Searching log file...")
    with open(path, 'r', encoding='utf-8') as f:
        for idx, line in enumerate(f):
            try:
                obj = json.loads(line)
                content = obj.get('content', '') or ''
                if 'To permanently resolve these' in content:
                    print(f"Match found: Line index: {idx}, Step index: {obj.get('step_index')}, Source: {obj.get('source')}, Type: {obj.get('type')}")
                    print(content[:500])
                    print("-" * 40)
            except Exception as e:
                pass
