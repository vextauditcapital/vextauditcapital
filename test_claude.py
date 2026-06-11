import os
import json
from agents.utils.rule_engine import rule_engine

# Dummy GST ledger data (CSV format)
dummy_ledger = """Invoice_ID,GSTIN,Debit,Credit,Tax_Rate
INV-001,27AAPFU0939F1Z5,1000.00,1000.00,18
INV-002,27AAPFU0939F1Z5,500.00,450.00,18
INV-003,INVALIDGSTIN123,2000.00,2000.00,12"""

print("Running test against the Rule Engine and Claude API...\n")

try:
    result = rule_engine.analyze_gst_ledger_structure(dummy_ledger)
    print(json.dumps(result, indent=2))
except Exception as e:
    print(f"Test failed with error: {e}")
