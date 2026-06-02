import os
import json

path = r"C:\Users\shyam\.gemini\antigravity\brain\0b69a188-ffdf-4bb1-acb7-45e6ea5edd18\.system_generated\logs\transcript.jsonl"

with open(path, 'r', encoding='utf-8') as f:
    for line in f:
        try:
            obj = json.loads(line)
            content = obj.get('content', '')
            if 'ROC Annual Compliance Audit' in content and 'VNz3svW' in content and 'zcsYoXk' in content:
                # This has the original user table! Let's print the entire thing or write to file
                out_path = r"C:\Users\shyam\.gemini\antigravity\scratch\original_user_table.txt"
                with open(out_path, 'w', encoding='utf-8') as out:
                    out.write(content)
                print(f"Saved original user table content to {out_path} (length {len(content)})")
                break
        except Exception as e:
            pass
