import io
import os
import datetime
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER, TA_RIGHT, TA_LEFT
from reportlab.lib import colors
from reportlab.lib.colors import HexColor
from reportlab.pdfgen import canvas

# Brand Colors
BRAND_DEEP_BURGUNDY = HexColor("#2C0808")
BRAND_MID_BURGUNDY = HexColor("#4A0E0E")
BRAND_GOLD = HexColor("#B8966B")
BRAND_CREAM = HexColor("#FBE5DE")

# Brand Fonts (Using standard fonts as fallback. To use TTFs, register them via ttfonts)
# For production with exact fonts:
# from reportlab.pdfbase import pdfmetrics
# from reportlab.pdfbase.ttfonts import TTFont
# pdfmetrics.registerFont(TTFont('Cinzel', 'agents/utils/fonts/Cinzel-Regular.ttf'))
# pdfmetrics.registerFont(TTFont('Cormorant', 'agents/utils/fonts/CormorantGaramond-Regular.ttf'))
# pdfmetrics.registerFont(TTFont('Jost', 'agents/utils/fonts/Jost-Regular.ttf'))

FONT_DISPLAY = "Helvetica-Bold" # Fallback for Cinzel
FONT_BODY = "Times-Roman" # Fallback for Cormorant
FONT_UI = "Helvetica" # Fallback for Jost
FONT_UI_BOLD = "Helvetica-Bold"

def generate_brand_invoice_pdf(client_details: dict, invoice_no: str, service_desc: str, amount: str) -> bytes:
    """
    Generates a branded invoice matching the provided sample format.
    Removes bank details as requested (using Razorpay).
    """
    buffer = io.BytesIO()
    # Adding bottom margin for footer
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40)
    
    def add_background(canvas_obj, _):
        canvas_obj.saveState()
        canvas_obj.setFillColor(BRAND_CREAM)
        canvas_obj.rect(0, 0, letter[0], letter[1], fill=1, stroke=0)
        canvas_obj.restoreState()

    elements = []
    
    # 1. Header (Logo on Left, Brand Name Center)
    logo_path = "VEXT-AUDIT-CAPITAL-LOGO.jpg"
    logo = Image(logo_path, width=80, height=80) if os.path.exists(logo_path) else Paragraph("LOGO", ParagraphStyle(name='temp', fontName=FONT_DISPLAY))
    
    header_data = [
        [logo, Paragraph("<font size='24' color='#4A0E0E'><b>Vext Audit Capital</b></font><br/><font size='10' color='#4A0E0E'>www.vextaudit.com</font>", ParagraphStyle(name='Header', alignment=TA_CENTER, fontName=FONT_DISPLAY))]
    ]
    header_table = Table(header_data, colWidths=[100, 400])
    header_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    elements.append(header_table)
    elements.append(Spacer(1, 40))

    # 2. Company Details & Invoice Info
    current_date = datetime.date.today().strftime("%d-%b-%Y")
    
    comp_details = f"<font size='10' color='#4A0E0E'><b>Vext Audit Capital</b><br/>SkyDasher Tech LLP,<br/>3/195-G, Nehru Nagar-3<br/>Kangayampalayam,<br/>Coimbatore 641401.<br/>Tamil Nadu, India.</font>"
    inv_details = f"<font size='20' color='#4A0E0E'><b>INVOICE</b></font><br/><font size='10' color='#4A0E0E'><b>Retail Invoice No: {invoice_no}</b></font><br/><br/><font size='10' color='#4A0E0E'><b>Invoice Date</b> &nbsp;&nbsp; {current_date}<br/><b>GSTIN:</b> 33AFIFS2899N1Z5</font>"

    info_data = [
        [Paragraph(comp_details, ParagraphStyle(name='L', fontName=FONT_UI)), Paragraph(inv_details, ParagraphStyle(name='R', alignment=TA_RIGHT, fontName=FONT_UI))]
    ]
    info_table = Table(info_data, colWidths=[250, 250])
    elements.append(info_table)
    elements.append(Spacer(1, 40))

    # 3. Bill To
    bill_to_text = f"<font size='10' color='#4A0E0E'><b>Bill To</b><br/>{client_details.get('name', '')}<br/>{client_details.get('company', '')}<br/>{client_details.get('address', '')}<br/>{client_details.get('location', '')}</font>"
    client_inv_details = f"<font size='10' color='#4A0E0E'><b>Invoice Date</b> &nbsp;&nbsp; {current_date}<br/><b>GSTIN:</b> {client_details.get('gstin', 'Not Provided')}</font>"
    
    bill_data = [
        [Paragraph(bill_to_text, ParagraphStyle(name='L', fontName=FONT_UI)), Paragraph(client_inv_details, ParagraphStyle(name='R', alignment=TA_RIGHT, fontName=FONT_UI))]
    ]
    bill_table = Table(bill_data, colWidths=[250, 250])
    elements.append(bill_table)
    elements.append(Spacer(1, 30))

    # 4. Separator Line
    elements.append(Table([['']], colWidths=[500], style=[('LINEABOVE', (0,0), (-1,-1), 1, BRAND_MID_BURGUNDY)]))
    elements.append(Spacer(1, 10))

    # 5. Service Description
    item_header = [
        Paragraph("<b>Service Description</b>", ParagraphStyle(name='IH', fontName=FONT_UI_BOLD, textColor=BRAND_MID_BURGUNDY)),
        Paragraph("<b>Rate</b>", ParagraphStyle(name='IH', fontName=FONT_UI_BOLD, textColor=BRAND_MID_BURGUNDY, alignment=TA_CENTER)),
        Paragraph("<b>Total</b>", ParagraphStyle(name='IH', fontName=FONT_UI_BOLD, textColor=BRAND_MID_BURGUNDY, alignment=TA_RIGHT))
    ]
    
    # Strip currency symbol for pure calculation if possible, assuming amount is a string like "150000"
    try:
        clean_amount = float(amount.replace(',', '').replace('₹', '').replace(' INR', '').strip())
    except:
        clean_amount = 0.0

    gst_amount = clean_amount * 0.18
    total_amount = clean_amount + gst_amount

    item_row = [
        Paragraph(service_desc, ParagraphStyle(name='IR', fontName=FONT_UI, textColor=BRAND_MID_BURGUNDY)),
        Paragraph(f"₹ {clean_amount:,.2f}", ParagraphStyle(name='IR', fontName=FONT_UI, textColor=BRAND_MID_BURGUNDY, alignment=TA_CENTER)),
        Paragraph(f"₹ {clean_amount:,.2f}", ParagraphStyle(name='IR', fontName=FONT_UI, textColor=BRAND_MID_BURGUNDY, alignment=TA_RIGHT))
    ]

    service_table = Table([item_header, item_row], colWidths=[300, 100, 100])
    # Add huge space to push totals to bottom
    elements.append(service_table)
    elements.append(Spacer(1, 150))
    
    # Bottom Line
    elements.append(Table([['']], colWidths=[500], style=[('LINEABOVE', (0,0), (-1,-1), 1, BRAND_MID_BURGUNDY)]))
    elements.append(Spacer(1, 10))

    # 6. Totals & Payment (No bank details)
    payment_info = "<font size='10' color='#4A0E0E'><b>Payment Method:</b> Razorpay Gateway</font>"
    
    totals_data = [
        [Paragraph(payment_info, ParagraphStyle(name='L', fontName=FONT_UI)), Paragraph("<b>SUB TOTAL<br/>(Tax Inclusive)</b>", ParagraphStyle(name='R', alignment=TA_RIGHT, fontName=FONT_UI, textColor=BRAND_MID_BURGUNDY)), Paragraph(f"₹ {clean_amount:,.2f}", ParagraphStyle(name='R', alignment=TA_RIGHT, fontName=FONT_UI, textColor=BRAND_MID_BURGUNDY))],
        ['', Paragraph("<b>GST 18%</b>", ParagraphStyle(name='R', alignment=TA_RIGHT, fontName=FONT_UI, textColor=BRAND_MID_BURGUNDY)), Paragraph(f"₹ {gst_amount:,.2f}", ParagraphStyle(name='R', alignment=TA_RIGHT, fontName=FONT_UI, textColor=BRAND_MID_BURGUNDY))],
        ['', Paragraph("<b>TOTAL</b>", ParagraphStyle(name='R', alignment=TA_RIGHT, fontName=FONT_UI, textColor=BRAND_MID_BURGUNDY)), Paragraph(f"₹ {total_amount:,.2f}", ParagraphStyle(name='R', alignment=TA_RIGHT, fontName=FONT_UI, textColor=BRAND_MID_BURGUNDY))],
    ]
    
    totals_table = Table(totals_data, colWidths=[260, 120, 120])
    elements.append(totals_table)

    doc.build(elements, onFirstPage=add_background, onLaterPages=add_background)
    pdf_bytes = buffer.getvalue()
    buffer.close()
    return pdf_bytes


def generate_brand_deliverable_pdf(client_name: str, report_content: str) -> bytes:
    """
    Generates the final audit deliverable report.
    Cream background. First/Last page logo full opacity. Internal pages watermark 30%.
    'Confidential document' text across all pages.
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=50, leftMargin=50, topMargin=50, bottomMargin=50)

    logo_path = "VEXT-AUDIT-CAPITAL-LOGO.jpg"

    def draw_background_and_watermark(canvas_obj, doc_obj):
        canvas_obj.saveState()
        # Cream Background
        canvas_obj.setFillColor(BRAND_CREAM)
        canvas_obj.rect(0, 0, letter[0], letter[1], fill=1, stroke=0)
        
        # Confidential Text (Rotated Watermark)
        canvas_obj.setFont(FONT_UI_BOLD, 40)
        canvas_obj.setFillColor(BRAND_MID_BURGUNDY, alpha=0.1) # 10% opacity for text
        canvas_obj.translate(letter[0]/2, letter[1]/2)
        canvas_obj.rotate(45)
        canvas_obj.drawCentredString(0, 0, "CONFIDENTIAL DOCUMENT")
        canvas_obj.rotate(-45)
        canvas_obj.translate(-letter[0]/2, -letter[1]/2)

        # Logo handling based on page number
        if os.path.exists(logo_path):
            total_pages = getattr(doc_obj, 'page', 1)
            # Internal pages get watermark logo
            canvas_obj.setFillAlpha(0.3)
            canvas_obj.drawImage(logo_path, (letter[0]-200)/2, (letter[1]-200)/2, width=200, height=200, mask='auto')

        canvas_obj.restoreState()

    def cover_and_last_page(canvas_obj, doc_obj):
        canvas_obj.saveState()
        # Cream Background
        canvas_obj.setFillColor(BRAND_CREAM)
        canvas_obj.rect(0, 0, letter[0], letter[1], fill=1, stroke=0)
        
        # Full Opacity Logo positioned higher up
        if os.path.exists(logo_path):
            canvas_obj.drawImage(logo_path, (letter[0]-150)/2, letter[1]-280, width=150, height=150, mask='auto')
        
        canvas_obj.restoreState()

    elements = []
    
    # Title Page
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(name='Title', alignment=TA_CENTER, fontName=FONT_DISPLAY, fontSize=24, textColor=BRAND_DEEP_BURGUNDY, spaceBefore=350, spaceAfter=20)
    sub_style = ParagraphStyle(name='Sub', alignment=TA_CENTER, fontName=FONT_BODY, fontSize=14, textColor=BRAND_MID_BURGUNDY)
    
    elements.append(Paragraph("STATUTORY COMPLIANCE REPORT", title_style))
    elements.append(Paragraph(f"Prepared Confidentially For: {client_name}", sub_style))
    elements.append(Paragraph(f"Date: {datetime.date.today().strftime('%d %B, %Y')}", sub_style))
    elements.append(PageBreak())

    # Report Content
    body_style = ParagraphStyle(name='Body', fontName=FONT_BODY, fontSize=11, textColor=BRAND_DEEP_BURGUNDY, spaceAfter=12, leading=16)
    
    for line in report_content.split('\n'):
        if line.strip():
            elements.append(Paragraph(line.strip(), body_style))
            
    elements.append(PageBreak())
    
    # Last Page
    end_style = ParagraphStyle(name='End', alignment=TA_CENTER, fontName=FONT_DISPLAY, fontSize=18, textColor=BRAND_DEEP_BURGUNDY, spaceBefore=300)
    elements.append(Paragraph("END OF REPORT", end_style))

    # We use build with dynamic page templates but SimpleDocTemplate is easier with onLaterPages
    doc.build(elements, onFirstPage=cover_and_last_page, onLaterPages=draw_background_and_watermark)
    
    pdf_bytes = buffer.getvalue()
    buffer.close()
    return pdf_bytes
