import json

log_path = r"C:\Users\shyam\.gemini\antigravity\brain\0b69a188-ffdf-4bb1-acb7-45e6ea5edd18\.system_generated\logs\transcript.jsonl"

with open(log_path, "r", encoding="utf-8") as f:
    for line in f:
        try:
            obj = json.loads(line)
            if obj.get("type") == "USER_INPUT":
                content = obj.get("content", "")
                print(f"=== STEP {obj.get('step_index')} ===")
                print(content[:500])
                if len(content) > 500:
                    print("... [TRUNCATED]")
                print("="*40)
        except Exception as e:
            pass
