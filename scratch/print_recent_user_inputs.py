import json

log_path = r"C:\Users\shyam\.gemini\antigravity\brain\0b69a188-ffdf-4bb1-acb7-45e6ea5edd18\.system_generated\logs\transcript.jsonl"

user_inputs = []
with open(log_path, "r", encoding="utf-8") as f:
    for line in f:
        try:
            obj = json.loads(line)
            if obj.get("type") == "USER_INPUT":
                user_inputs.append((obj.get("step_index"), obj.get("content", "")))
        except Exception as e:
            pass

print(f"Total user inputs found: {len(user_inputs)}")
for idx, content in user_inputs[-15:]:
    print(f"\n=== STEP {idx} ===")
    print(content)
    print("="*50)
