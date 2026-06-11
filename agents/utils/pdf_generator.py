import io
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER
import datetime

def generate_bulletproof_sow(client_name: str, service_summary: str, price: str = "₹75,000") -> bytes:
    """
    Generates a crystal-clear, legally binding Statement of Work (SOW) PDF in memory.
    Returns the raw PDF bytes.
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=18)
    
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))
    styles.add(ParagraphStyle(name='CenterTitle', alignment=TA_CENTER, fontSize=16, spaceAfter=20, fontName="Helvetica-Bold"))
    styles.add(ParagraphStyle(name='SectionTitle', fontSize=12, spaceAfter=10, spaceBefore=15, fontName="Helvetica-Bold"))
    
    Story = []
    
    # Title
    Story.append(Paragraph("STATEMENT OF WORK AND BINDING AGREEMENT", styles['CenterTitle']))
    
    # Intro
    current_date = datetime.date.today().strftime("%d %B, %Y")
    intro_text = f"This Statement of Work (the \"SOW\") is effective as of {current_date} by and between Vext Audit Capital (\"Provider\") and {client_name} (\"Client\"). This document represents a binding legal agreement governing the provision of audit and compliance services."
    Story.append(Paragraph(intro_text, styles['Justify']))
    Story.append(Spacer(1, 12))
    
    # 1. Scope of Services
    Story.append(Paragraph("1. SCOPE OF SERVICES", styles['SectionTitle']))
    scope_text = f"Provider agrees to deliver the following services strictly as outlined below, with no exceptions or undocumented additions: <b>{service_summary}</b>. Any modifications to this scope must be executed in writing and explicitly signed by both parties."
    Story.append(Paragraph(scope_text, styles['Justify']))
    
    # 2. Compensation & Payment Terms
    Story.append(Paragraph("2. COMPENSATION AND PAYMENT TERMS", styles['SectionTitle']))
    payment_text = f"Client shall compensate Provider a fixed, non-refundable sum of <b>{price}</b>, exclusive of applicable taxes. Payment is strictly due upon the execution of this SOW or as specified via a legally enforceable digital invoice link. Work will not commence until full payment is captured and cleared."
    Story.append(Paragraph(payment_text, styles['Justify']))
    
    # 3. Confidentiality
    Story.append(Paragraph("3. ABSOLUTE CONFIDENTIALITY AND SECURITY", styles['SectionTitle']))
    conf_text = "All financial ledgers, proprietary documents, and personally identifiable information shared by the Client will be handled with strict adherence to ISO 27001, DPDP, and PCI-DSS compliance frameworks. The Provider guarantees zero unauthorized disclosure."
    Story.append(Paragraph(conf_text, styles['Justify']))

    # 4. Liability and Indemnification
    Story.append(Paragraph("4. LIMITATION OF LIABILITY", styles['SectionTitle']))
    liability_text = "To the maximum extent permitted by applicable law, the Provider's total liability under this SOW—regardless of the legal theory—shall be strictly limited to the total fees actually paid by the Client to the Provider under this specific SOW. The Provider explicitly disclaims any liability for indirect, incidental, punitive, or consequential damages."
    Story.append(Paragraph(liability_text, styles['Justify']))
    
    # 5. Signatures
    Story.append(Paragraph("5. EXECUTION", styles['SectionTitle']))
    Story.append(Paragraph("By appending their electronic signature below, the Client unequivocally agrees to all terms, conditions, scopes, and legal boundaries defined in this document. This digital signature holds full legal equivalence to a physical signature.", styles['Justify']))
    Story.append(Spacer(1, 40))
    
    # Using specific tags like {{Signature}} which Zoho Sign can automatically map to signature fields if configured,
    # or Zoho Sign can just place it at the end of the document.
    Story.append(Paragraph("Signature: ___________________________", styles['Normal']))
    Story.append(Spacer(1, 10))
    Story.append(Paragraph(f"Client Authorized Signatory: {client_name}", styles['Normal']))
    Story.append(Spacer(1, 10))
    Story.append(Paragraph(f"Date: ___________________________", styles['Normal']))
    
    doc.build(Story)
    pdf_bytes = buffer.getvalue()
    buffer.close()
    
    return pdf_bytes
