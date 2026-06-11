import os
from agents.utils.pdf_generator import generate_brand_invoice_pdf, generate_brand_deliverable_pdf

# 1. Generate Sample Invoice
client_details = {
    "name": "Arun Kumar,",
    "company": "TechVision India Pvt Ltd,",
    "address": "123 Innovation Park, Block B,",
    "location": "Bengaluru, 560100.",
    "gstin": "29AABCT1234E1Z1"
}

invoice_bytes = generate_brand_invoice_pdf(
    client_details=client_details,
    invoice_no="VAC-2026-1045",
    service_desc="Complete GST Statutory Audit & DPDP Readiness Package",
    amount="150000"
)

with open("SAMPLE_INVOICE.pdf", "wb") as f:
    f.write(invoice_bytes)

# 2. Generate Sample Deliverable
sample_report_content = """
EXECUTIVE SUMMARY
This report details the findings of the GST and DPDP statutory audit conducted for TechVision India Pvt Ltd.

GST COMPLIANCE FINDINGS
1. Outward supply reconciliation matches GSTR-1 and GSTR-3B with 0% variance.
2. Input Tax Credit (ITC) claimed under Section 16 is fully supported by valid tax invoices.
3. E-invoicing mandate under Rule 48(4) is being correctly followed for B2B transactions.

DPDP READINESS
1. Data Fiduciary obligations are met regarding consent management.
2. Gap detected: Privacy notice needs updating to reflect new data retention periods.
"""

deliverable_bytes = generate_brand_deliverable_pdf(
    client_name="TechVision India Pvt Ltd",
    report_content=sample_report_content
)

with open("SAMPLE_DELIVERABLE.pdf", "wb") as f:
    f.write(deliverable_bytes)

print("Generated SAMPLE_INVOICE.pdf and SAMPLE_DELIVERABLE.pdf successfully.")
