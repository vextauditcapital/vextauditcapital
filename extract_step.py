import os
import json

path = r"C:\Users\shyam\.gemini\antigravity\brain\0b69a188-ffdf-4bb1-acb7-45e6ea5edd18\.system_generated\logs\transcript.jsonl"
with open(path, 'r', encoding='utf-8') as f:
    for line in f:
        try:
            obj = json.loads(line)
            if obj.get('step_index') == 2489:
                print("Found step 2489!")
                content = obj.get('content', '')
                with open('step_2489_content.txt', 'w', encoding='utf-8') as out:
                    out.write(content)
                print("Wrote content to step_2489_content.txt")
                break
        except Exception as e:
            pass
