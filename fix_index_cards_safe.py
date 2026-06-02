import re

rupee = '\u20b9'

replacements = {
    'gst-audit-compliance.html': f'''        <div class="service-icon">⚖</div>
        <h3 class="service-title">GST Audit &amp; Compliance</h3>
        <p class="service-desc">Comprehensive GST health checks, return reconciliation, ITC audits, notice responses, and GSTR-9C preparation.</p>
        <div class="service-price">{rupee}25,000 / engagement</div>
        <a href="gst-audit-compliance.html" class="service-cta">Explore Details</a>''',

    'dpdp-readiness-assessment.html': f'''        <div class="service-icon">🔐</div>
        <h3 class="service-title">DPDP Readiness Assessment</h3>
        <p class="service-desc">Compliance assessment for India's Digital Personal Data Protection Act 2023. We audit data flows and consent forms.</p>
        <div class="service-price">{rupee}40,000 / assessment</div>
        <a href="dpdp-readiness-assessment.html" class="service-cta">Explore Details</a>''',

    'financial-operations-audit.html': f'''        <div class="service-icon">📊</div>
        <h3 class="service-title">Financial Operations Audit</h3>
        <p class="service-desc">Internal financial controls review, expense audit, vendor payment verification, and ledger reconciliation.</p>
        <div class="service-price">{rupee}30,000 / audit</div>
        <a href="financial-operations-audit.html" class="service-cta">Explore Details</a>''',

    'roc-annual-compliance-audit.html': f'''        <div class="service-icon">🏛</div>
        <h3 class="service-title">ROC / MCA Annual Compliance</h3>
        <p class="service-desc">Annual filing reviews, ROC compliance health checks, director KYC status, and charge registration verification.</p>
        <div class="service-price">{rupee}18,000 / review</div>
        <a href="roc-annual-compliance-audit.html" class="service-cta">Explore Details</a>''',

    'annual-compliance-subscription.html': f'''        <div class="service-icon">📅</div>
        <h3 class="service-title">Annual Compliance Subscription</h3>
        <p class="service-desc">Year-round legal management. Due dates tracked, filings monitored, and proactive alerts sent continuously.</p>
        <div class="service-price">{rupee}60,000 / year</div>
        <a href="annual-compliance-subscription.html" class="service-cta">Explore Details</a>''',

    'startup-dpiit-compliance-audit.html': f'''        <div class="service-icon">🚀</div>
        <h3 class="service-title">Startup DPIIT Compliance Audit</h3>
        <p class="service-desc">DPIIT recognition review, statutory benefit checks, angel tax exemption, and startup scheme audit trails.</p>
        <div class="service-price">{rupee}18,000 / audit</div>
        <a href="startup-dpiit-compliance-audit.html" class="service-cta">Explore Details</a>''',

    'pcidss-compliance-assessment.html': f'''        <div class="service-icon">💳</div>
        <h3 class="service-title">PCI-DSS Compliance Assessment</h3>
        <p class="service-desc">Cardholder data environment security review. Map network segments, storage policies, and card transmission logs.</p>
        <div class="service-price"> / assessment</div>
        <a href="pcidss-compliance-assessment.html" class="service-cta">Explore Details</a>''',

    'ai-business-process-intelligence.html': f'''        <div class="service-icon">⚙</div>
        <h3 class="service-title">Process Intelligence</h3>
        <p class="service-desc">Deep-dive operational process analysis. We map workflows, identify inefficiencies, and flag compliance gaps.</p>
        <div class="service-price"> / assessment</div>
        <a href="ai-business-process-intelligence.html" class="service-cta">Explore Details</a>''',

    'ai-competitive-intelligence.html': f'''        <div class="service-icon">📈</div>
        <h3 class="service-title">Competitive Intelligence</h3>
        <p class="service-desc">Structured competitive landscape analysis. Regulatory positioning, advantage scans, and regulatory moats.</p>
        <div class="service-price"> / report</div>
        <a href="ai-competitive-intelligence.html" class="service-cta">Explore Details</a>''',

    'ai-market-entry-analysis.html': f'''        <div class="service-icon">🗺</div>
        <h3 class="service-title">Market Entry Analysis</h3>
        <p class="service-desc">Regulatory and compliance risk analysis for entering new international or regional markets. Licensing mapped.</p>
        <div class="service-price"> / analysis</div>
        <a href="ai-market-entry-analysis.html" class="service-cta">Explore Details</a>''',

    'ai-operational-risk-assessment.html': f'''        <div class="service-icon">⚠</div>
        <h3 class="service-title">Operational Risk Assessment</h3>
        <p class="service-desc">Enterprise-grade operational risk review. Controls, vendor compliance, IT vulnerability, and continuity gaps mapped.</p>
        <div class="service-price">,022 / assessment</div>
        <a href="ai-operational-risk-assessment.html" class="service-cta">Explore Details</a>''',

    'vextintel-global.html': f'''        <div class="service-icon">🌍</div>
        <h3 class="service-title">VextIntel Global Edition</h3>
        <p class="service-desc">Global continuous regulatory digest. Multi-jurisdiction tax modifications, cross-border data rules, and advisory.</p>
        <div class="service-price"> / month</div>
        <a href="vextintel-global.html" class="service-cta">Explore Details</a>'''
}

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Parse the file service card by service card
def process_card(match):
    card_content = match.group(0)
    
    # Check if this is the ISO 27001 card, and remove it completely if so
    if 'iso27001-gap-assessment.html' in card_content:
        return ''
        
    for href, new_inner in replacements.items():
        if f'href="{href}"' in card_content:
            # Reconstruct the card retaining its opening tag
            open_tag = re.match(r'<div class="service-card[^>]*>', card_content).group(0)
            return f"{open_tag}\n{new_inner}\n      </div>"
    
    return card_content

content = re.sub(r'<div class="service-card[^>]*>.*?</a>\s*</div>', process_card, content, flags=re.DOTALL)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Index updated safely.")