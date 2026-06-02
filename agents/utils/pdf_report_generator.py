import os
import logging
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

logger = logging.getLogger("VextPDFReportGenerator")

REPORTS_DIR = r"C:\Users\shyam\.gemini\antigravity\scratch\reports"
LOGO_PATH = r"C:\Users\shyam\.gemini\antigravity\scratch\VEXT-AUDIT-CAPITAL-LOGO.jpg"

def draw_report_background(canvas, doc):
    """Draws a premium luxury Cream background color matching the VEXT logo."""
    canvas.saveState()
    canvas.setFillColor(colors.HexColor('#F1E9DC'))
    canvas.rect(0, 0, doc.pagesize[0], doc.pagesize[1], fill=1, stroke=0)
    canvas.restoreState()

class VextPDFReportGenerator:
    """
    Autonomous Publication-Quality PDF Report Compiler.
    Transforms structured compliance audits into stunning, professional PDF documents.
    Enforces premium brand aesthetics (Burgundy, Luxury Cream, and Gold color palette)
    and renders prominent legal safety disclaimers on the final page.
    """
    def __init__(self):
        self.reports_dir = REPORTS_DIR
        self.logo_path = LOGO_PATH
        
        if not os.path.exists(self.reports_dir):
            os.makedirs(self.reports_dir)

    def generate_report_pdf(self, report_data: dict) -> str:
        """
        Compiles the verified audit report dictionary into a professional B2B PDF.
        Returns the absolute path of the generated PDF.
        """
        meta = report_data["audit_meta"]
        results = report_data["audit_results"]
        
        client_name = meta["client_name"]
        service_name = meta["service_name"]
        timestamp_str = datetime.fromisoformat(meta["timestamp_utc"]).strftime("%d %b %Y %H:%M:%S UTC")
        doc_hash = meta["document_hash_sha256"]
        crypto_sig = meta["cryptographic_signature"]
        score = results["overall_compliance_score"]
        status = results["status"]
        
        pdf_filename = f"AUDIT-{client_name.replace(' ', '_')}-{meta['service_code'].upper()}-{datetime.utcnow().strftime('%Y%m%d')}.pdf"
        pdf_path = os.path.join(self.reports_dir, pdf_filename)
        
        # Setup document layout
        doc = SimpleDocTemplate(
            pdf_path,
            pagesize=letter,
            rightMargin=40, leftMargin=40,
            topMargin=40, bottomMargin=40
        )
        
        story = []
        styles = getSampleStyleSheet()
        
        # Define premium Typography styles
        burgundy = colors.HexColor('#581C23')
        burgundy_dark = colors.HexColor('#3B0E14')
        charcoal = colors.HexColor('#0F172A')
        muted_slate = colors.HexColor('#475569')
        gold = colors.HexColor('#D4AF37')
        cream_dark = colors.HexColor('#CBBFA4')
        
        title_style = ParagraphStyle(
            'ReportTitle',
            parent=styles['Heading1'],
            fontName='Helvetica-Bold',
            fontSize=22,
            textColor=burgundy,
            spaceAfter=4,
            leading=26
        )
        subtitle_style = ParagraphStyle(
            'ReportSubtitle',
            parent=styles['Heading3'],
            fontName='Helvetica',
            fontSize=11,
            textColor=muted_slate,
            spaceAfter=15,
            leading=14
        )
        meta_label_style = ParagraphStyle(
            'MetaLabel',
            parent=styles['Normal'],
            fontName='Helvetica-Bold',
            fontSize=9,
            textColor=charcoal,
            leading=12
        )
        meta_val_style = ParagraphStyle(
            'MetaVal',
            parent=styles['Normal'],
            fontName='Helvetica',
            fontSize=9,
            textColor=muted_slate,
            leading=12
        )
        section_style = ParagraphStyle(
            'SectionHeader',
            parent=styles['Heading2'],
            fontName='Helvetica-Bold',
            fontSize=13,
            textColor=burgundy_dark,
            spaceBefore=15,
            spaceAfter=8,
            leading=16
        )
        body_style = ParagraphStyle(
            'ReportBody',
            parent=styles['Normal'],
            fontName='Helvetica',
            fontSize=9,
            textColor=charcoal,
            leading=14
        )
        finding_item_style = ParagraphStyle(
            'FindingItem',
            parent=styles['Normal'],
            fontName='Helvetica',
            fontSize=9,
            textColor=charcoal,
            leading=13,
            leftIndent=15,
            firstLineIndent=-10,
            spaceAfter=5
        )
        gap_item_style = ParagraphStyle(
            'GapItem',
            parent=styles['Normal'],
            fontName='Helvetica-Bold',
            fontSize=9,
            textColor=colors.HexColor('#991B1B'), # Bold crimson alert for gaps
            leading=13,
            leftIndent=15,
            firstLineIndent=-10,
            spaceAfter=5
        )
        remediation_item_style = ParagraphStyle(
            'RemediationItem',
            parent=styles['Normal'],
            fontName='Helvetica',
            fontSize=9,
            textColor=colors.HexColor('#065F46'), # High-contrast deep emerald for fixes
            leading=13,
            leftIndent=15,
            firstLineIndent=-10,
            spaceAfter=5
        )
        disclaimer_header_style = ParagraphStyle(
            'DisclaimerHeader',
            parent=styles['Normal'],
            fontName='Helvetica-Bold',
            fontSize=9,
            textColor=burgundy,
            spaceAfter=4,
            leading=11
        )
        disclaimer_body_style = ParagraphStyle(
            'DisclaimerBody',
            parent=styles['Normal'],
            fontName='Helvetica-Oblique',
            fontSize=8,
            textColor=muted_slate,
            leading=11
        )

        # 1. Header (Branding & Title)
        logo_text = f"<b>{service_name.upper()}</b>"
        header_table_data = [
            [Paragraph(logo_text, ParagraphStyle('HeaderTxt', parent=title_style, fontSize=14, spaceAfter=0)), 
             Paragraph("<b>VEXT AUDIT CAPITAL</b><br/><font size='7' color='#475569'>AI COMPLIANCE DIAGNOSTICS</font>", ParagraphStyle('BrandTxt', parent=meta_label_style, alignment=2, leading=9))]
        ]
        header_table = Table(header_table_data, colWidths=[4.2*inch, 2.8*inch])
        header_table.setStyle(TableStyle([
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ]))
        story.append(header_table)
        
        # Decorative double accent divider
        divider = Table([[""]], colWidths=[7.0*inch])
        divider.setStyle(TableStyle([
            ('LINEABOVE', (0,0), (-1,-1), 2.0, burgundy),
            ('TOPPADDING', (0,0), (-1,-1), 0),
            ('BOTTOMPADDING', (0,0), (-1,-1), 0),
        ]))
        story.append(divider)
        story.append(Spacer(1, 10))

        # 2. Main Title and Intro
        story.append(Paragraph("Compliance Assessment Report", title_style))
        story.append(Paragraph(f"Client-specific automated pre-scan advisory findings and diagnostics map.", subtitle_style))

        # 3. Metadate Block Table
        meta_table_data = [
            [Paragraph("CLIENT NAME:", meta_label_style), Paragraph(client_name, meta_val_style),
             Paragraph("ASSESSMENT DATE:", meta_label_style), Paragraph(timestamp_str, meta_val_style)],
            [Paragraph("SERVICE LINE:", meta_label_style), Paragraph(service_name, meta_val_style),
             Paragraph("VERIFIER AGENT:", meta_label_style), Paragraph(meta["verifier"], meta_val_style)],
            [Paragraph("SOURCE DOCUMENT:", meta_label_style), Paragraph(meta["document_file"], meta_val_style),
             Paragraph("LEDGER CHECKSUM:", meta_label_style), Paragraph(doc_hash[:16] + "...", meta_val_style)]
        ]
        meta_table = Table(meta_table_data, colWidths=[1.4*inch, 2.1*inch, 1.4*inch, 2.1*inch])
        meta_table.setStyle(TableStyle([
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('BOTTOMPADDING', (0,0), (-1,-1), 5),
            ('TOPPADDING', (0,0), (-1,-1), 5),
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#EADFC9')), # Rich matching warm layout background
            ('BOX', (0,0), (-1,-1), 0.5, cream_dark),
            ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E3D7C0')),
        ]))
        story.append(meta_table)
        story.append(Spacer(1, 15))

        # 4. Overall Score & Compliance Status Callout
        score_bg = colors.HexColor('#FEE2E2') if score < 80 else colors.HexColor('#D1FAE5')
        score_text_color = colors.HexColor('#991B1B') if score < 80 else colors.HexColor('#065F46')
        
        score_card_data = [
            [
                Paragraph(f"<font size='10'><b>DIAGNOSTIC STATUS:</b></font><br/><font size='14' color='{score_text_color.hexval()}'><b>{status.replace('_', ' ')}</b></font>", body_style),
                Paragraph(f"<font size='10'><b>OVERALL COMPLIANCE SCORE:</b></font><br/><font size='26' color='{score_text_color.hexval()}'><b>{score}%</b></font>", ParagraphStyle('ScoreAlign', parent=right_align_style if 'right_align_style' in globals() else body_style, alignment=2))
            ]
        ]
        score_table = Table(score_card_data, colWidths=[4.0*inch, 3.0*inch])
        score_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), score_bg),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('BOX', (0,0), (-1,-1), 1.0, score_text_color),
            ('BOTTOMPADDING', (0,0), (-1,-1), 10),
            ('TOPPADDING', (0,0), (-1,-1), 10),
        ]))
        story.append(score_table)
        story.append(Spacer(1, 15))

        # 5. Verified Findings Section
        story.append(Paragraph("1. Verified Diagnostic Findings", section_style))
        if results["verified_findings"]:
            for f in results["verified_findings"]:
                story.append(Paragraph(f"• {f}", finding_item_style))
        else:
            story.append(Paragraph("No major structural anomalies or compliance findings identified in source ledger scanning.", body_style))
        story.append(Spacer(1, 10))

        # 6. Gaps Detected Section
        story.append(Paragraph("2. Compliance & Regulatory Gaps Identified", section_style))
        if results["gaps_detected"]:
            for g in results["gaps_detected"]:
                story.append(Paragraph(f"⚠ {g}", gap_item_style))
        else:
            story.append(Paragraph("<b>No active regulatory or structural compliance gaps identified.</b> Operations appear to align with baseline checks.", remediation_item_style))
        story.append(Spacer(1, 10))

        # 7. Remediation Plan Section
        story.append(Paragraph("3. Recommended Advisory Remediation Plan", section_style))
        if results["remediation_plan"]:
            for r in results["remediation_plan"]:
                story.append(Paragraph(f"✔ {r}", remediation_item_style))
        else:
            story.append(Paragraph("No active remediation necessary. Maintain baseline internal auditing schedules.", body_style))
        story.append(Spacer(1, 20))

        # Force Disclaimer onto the last page or draw a clean separator block
        story.append(Spacer(1, 10))
        
        # 8. Cryptographic Signatures Block
        sig_data = [
            [
                Paragraph(f"<b>HMAC TRANSACTION SIGNATURE:</b><br/>{crypto_sig}", ParagraphStyle('SigTxt', parent=meta_val_style, fontSize=7, leading=9)),
                Paragraph("<b>VERIFICATION AUTHORITY:</b><br/>Vext Audit Capital Operations<br/><i>Digitally Signed (HMAC-SHA256)</i>", ParagraphStyle('SigAuth', parent=meta_label_style, fontSize=7, alignment=2, leading=9))
            ]
        ]
        sig_table = Table(sig_data, colWidths=[4.2*inch, 2.8*inch])
        sig_table.setStyle(TableStyle([
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('TOPPADDING', (0,0), (-1,-1), 8),
            ('LINEABOVE', (0,0), (-1,-1), 0.5, cream_dark)
        ]))
        story.append(sig_table)
        story.append(Spacer(1, 25))

        # 9. Brand Protection Legal Disclaimer Box
        disclaimer_text_header = "<b>CRITICAL LEGAL DISCLAIMER & LIMITATION OF LIABILITY</b>"
        disclaimer_text_body = (
            "This document is an automated diagnostic assessment compiled using proprietary artificial intelligence "
            "agents and mathematical heuristic rule engines. It is designed to act solely as a preliminary pre-scan advisory "
            "diagnostic to identify structural gaps before official audits are scheduled. It does not constitute certified legal, "
            "financial, or formal statutory tax counsel. Vext Audit Capital operates strictly as a diagnostics provider and does "
            "not guarantee 100% absolute accuracy or compliance immunity. The Firm disclaims all liability for regulatory audits, "
            "statutory enforcement actions, penalties, or compliance disputes resulting from the use of this data. Client is advised "
            "to cross-reconcile all findings with qualified professional counsel."
        )
        
        disclaimer_data = [
            [Paragraph(disclaimer_text_header, disclaimer_header_style)],
            [Paragraph(disclaimer_text_body, disclaimer_body_style)]
        ]
        disclaimer_table = Table(disclaimer_data, colWidths=[7.0*inch])
        disclaimer_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#FEE2E2')), # Highlight in very soft red to ensure visual alert
            ('BOX', (0,0), (-1,-1), 1.0, burgundy),
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('TOPPADDING', (0,0), (-1,-1), 10),
            ('BOTTOMPADDING', (0,0), (-1,-1), 10),
            ('LEFTPADDING', (0,0), (-1,-1), 12),
            ('RIGHTPADDING', (0,0), (-1,-1), 12)
        ]))
        story.append(disclaimer_table)

        # Build document with premium Cream background
        doc.build(story, onFirstPage=draw_report_background, onLaterPages=draw_report_background)
        logger.info(f"Compiled premium B2B Compliance PDF: {pdf_path}")
        return pdf_path


# Single shared instance
pdf_report_generator = VextPDFReportGenerator()

if __name__ == "__main__":
    # Self-test code
    logging.basicConfig(level=logging.INFO)
    test_data = {
        "audit_meta": {
            "client_name": "Acme Ventures",
            "client_email": "admin@acmeventures.io",
            "service_code": "gst",
            "service_name": "GST Audit & Compliance",
            "document_file": "ledger_sample.csv",
            "document_hash_sha256": "abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890",
            "timestamp_utc": datetime.utcnow().isoformat(),
            "cryptographic_signature": "hmac_signature_verified_ok",
            "verifier": "VextMasterVerifierAgent/1.0"
        },
        "audit_results": {
            "overall_compliance_score": 70,
            "status": "COMPLIANCE_GAP_IDENTIFIED",
            "verified_findings": ["Completed structural mapping of 142 invoice elements.", "Detected ledger transactions with domestic vendors."],
            "gaps_detected": ["Two transactions exceed Section 40A(3) cash guidelines (value > ₹10,000).", "Invalid GSTIN syntax formatting found on invoice line 43."],
            "remediation_plan": ["Approve expenditures exceeding ₹10,000 strictly via bank remittances.", "Re-verify vendor registration identifiers against the official central registry portal."]
        }
    }
    pdf_report_generator.generate_report_pdf(test_data)
