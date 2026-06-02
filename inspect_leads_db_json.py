import json
import os

path = r"C:\Users\shyam\.gemini\antigravity\scratch\agents\leads_database.json"
if os.path.exists(path):
    with open(path, 'r', encoding='utf-8') as f:
        try:
            data = json.load(f)
            verified = data.get("verified_leads", [])
            if isinstance(verified, list):
                print(f"verified_leads is a list of size {len(verified)}")
                if len(verified) > 0:
                    print(f"Sample item structure:\n{json.dumps(verified[0], indent=2)[:800]}")
            elif isinstance(verified, dict):
                print(f"verified_leads is a dictionary with {len(verified)} keys")
                keys = list(verified.keys())
                print(f"Sample keys: {keys[:5]}")
                print(f"Sample value structure:\n{json.dumps(verified[keys[0]], indent=2)[:800]}")
        except Exception as e:
            print(f"Error: {e}")
