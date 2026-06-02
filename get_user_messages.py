import os
import json

path = r"C:\Users\shyam\.gemini\antigravity\brain\0b69a188-ffdf-4bb1-acb7-45e6ea5edd18\.system_generated\logs\transcript.jsonl"
if not os.path.exists(path):
    print(f"Log file not found at {path}")
else:
    print("Searching log file for user messages with rzp...")
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            try:
                obj = json.loads(line)
                if obj.get('type') == 'USER_INPUT':
                    content = obj.get('content', '')
                    if 'GST Audit' in content and 'rzp.io' in content:
                        print(f"\nUser Input at Step {obj.get('step_index')}:")
                        print(content)
                        print("="*80)
            except Exception as e:
                pass
