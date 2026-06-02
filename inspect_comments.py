import re

with open("index.html", "r", encoding="utf-8") as f:
    text = f.read()

# Find all HTML comments
comments = re.findall(r'<!--(.*?)-->', text, re.DOTALL)
print(f"Total HTML comments found: {len(comments)}")
for idx, comment in enumerate(comments):
    clean_comment = comment.strip()
    if len(clean_comment) > 0:
        # Check if the comment contains any service card names or similar
        print(f"Comment {idx+1} (length {len(clean_comment)}):")
        print("\n".join(clean_comment.splitlines()[:10]))
        if len(clean_comment.splitlines()) > 10:
            print("...")
        print("-" * 40)
