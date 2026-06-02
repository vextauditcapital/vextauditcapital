import os
import json

path = r"C:\Users\shyam\.gemini\antigravity\brain\0b69a188-ffdf-4bb1-acb7-45e6ea5edd18\.system_generated\logs\transcript.jsonl"
if not os.path.exists(path):
    print(f"Log file not found at {path}")
else:
    print("Searching log file for Razorpay table...")
    with open(path, 'r', encoding='utf-8') as f:
        for idx, line in enumerate(f):
            try:
                obj = json.loads(line)
                content = obj.get('content', '')
                if 'GST Audit & Compliance' in content and 'Total B2B Price' in content:
                    print(f"Found matching message/step at line {idx+1}!")
                    # Print the entire content of this match
                    print(content)
                    print("=" * 80)
            except Exception as e:
                pass
