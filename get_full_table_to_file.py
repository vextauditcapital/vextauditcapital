import os
import json

path = r"C:\Users\shyam\.gemini\antigravity\brain\0b69a188-ffdf-4bb1-acb7-45e6ea5edd18\.system_generated\logs\transcript.jsonl"
out_path = r"C:\Users\shyam\.gemini\antigravity\scratch\scratch_table.txt"

with open(path, 'r', encoding='utf-8') as f:
    for line in f:
        try:
            obj = json.loads(line)
            content = obj.get('content', '')
            if 'GST Audit & Compliance' in content and 'Total B2B Price' in content:
                # Let's save this to file
                with open(out_path, 'w', encoding='utf-8') as out:
                    out.write(content)
                print(f"Saved matching content to {out_path}")
                break
        except Exception as e:
            pass
