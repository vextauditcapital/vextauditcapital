import json

log_path = r"C:\Users\shyam\.gemini\antigravity\brain\0b69a188-ffdf-4bb1-acb7-45e6ea5edd18\.system_generated\logs\transcript.jsonl"

with open(log_path, "r", encoding="utf-8") as f:
    for line in f:
        try:
            obj = json.loads(line)
            content = obj.get("content", "")
            # check if there's any other step matching keywords
            if any(kw in content.lower() for kw in ["net profit", "revenue target", "fy 2026-2027", "dec 2026"]):
                print(f"=== STEP {obj.get('step_index')} ({obj.get('type')}) ===")
                print(content[:600])
                print("="*40)
        except Exception as e:
            pass
