with open("index.html", "r", encoding="utf-8") as f:
    content = f.read()

lines = content.splitlines()
with open("index_sections.txt", "w", encoding="utf-8") as out:
    for i in range(500, min(len(lines), 710)):
        out.write(f"{i+1}: {lines[i]}\n")

print("Done writing index_sections.txt")
