with open("index.html", "r", encoding="utf-8") as f:
    content = f.read()

lines = content.splitlines()
results = []
for i, line in enumerate(lines):
    if any(term in line for term in ["TDS Compliance Audit", "FEMA Compliance Audit", "ROC Annual Compliance", "Payroll Compliance Audit", "Annual Compliance Subscription", "MSME Compliance Health Check", "Startup India DPIIT Audit", "Process Intelligence", "Competitive Intelligence", "Market Entry Analysis", "Operational Risk Assessment"]):
        results.append(f"Line {i+1}: {line}")
        # Print 10 lines before and after
        for j in range(max(0, i-5), min(len(lines), i+15)):
            results.append(f"  {j+1}: {lines[j]}")
        results.append("-" * 50)

with open("index_cards_output.txt", "w", encoding="utf-8") as f_out:
    f_out.write("\n".join(results))
print("Done writing to index_cards_output.txt")
