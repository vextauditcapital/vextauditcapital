import os
import json

path = r"C:\Users\shyam\.gemini\antigravity\brain\0b69a188-ffdf-4bb1-acb7-45e6ea5edd18\.system_generated\logs\transcript.jsonl"

with open(path, 'r', encoding='utf-8') as f:
    for idx, line in enumerate(f):
        try:
            obj = json.loads(line)
            content = obj.get('content', '')
            if 'GST Audit & Compliance' in content and 'Total B2B Price' in content:
                # Save each match with index
                out_path = f"C:\\Users\\shyam\\.gemini\\antigravity\\scratch\\table_{idx+1}.txt"
                with open(out_path, 'w', encoding='utf-8') as out:
                    out.write(content)
                print(f"Saved match at line {idx+1} to {out_path} (length {len(content)})")
        except Exception as e:
            pass
