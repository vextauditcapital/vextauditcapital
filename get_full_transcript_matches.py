import os
import json

path = r"C:\Users\shyam\.gemini\antigravity\brain\0b69a188-ffdf-4bb1-acb7-45e6ea5edd18\.system_generated\logs\transcript.jsonl"
if not os.path.exists(path):
    print(f"Log file not found at {path}")
else:
    print("Searching log file...")
    matches = []
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            try:
                obj = json.loads(line)
                content = obj.get('content', '')
                if 'GST Audit' in content and 'MyIHpEhi' in content:
                    matches.append((obj.get('step_index', 0), obj.get('type', ''), content))
            except Exception as e:
                pass
    
    print(f"Found {len(matches)} matches")
    for step_idx, m_type, m_content in matches:
        print(f"Step: {step_idx} | Type: {m_type}")
        # let's look for markdown table format in the content
        if '|' in m_content and 'GST Audit' in m_content:
            print("FOUND MARKDOWN TABLE:")
            # Print lines that look like a table
            for l in m_content.split('\n'):
                if '|' in l or 'Audit' in l or 'rzp.io' in l:
                    print(l[:150])
            print("="*40)
