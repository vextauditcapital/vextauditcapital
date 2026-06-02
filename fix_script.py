import os
import re

def fix_index():
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # Clean up accidental injection
    html = re.sub(r'\},\{AllowMultiple:false,EndLine:435,ReplacementContent:\n', '', html)

    # Re-insert deleted Operational Risk Assessment
    if 'Operational Risk Assessment' not in html:
        op_risk = '''    <div class="service-card fade-up fade-up-delay-3">
        <div class="service-icon">⚠</div>
        <h3 class="service-title">Operational Risk Assessment</h3>
        <p class="service-desc">Enterprise-grade operational risk review. Controls, vendor compliance, IT vulnerability, and continuity gaps mapped.</p>
        <div class="service-price">$1,022 / assessment</div>
        <a href="ai-operational-risk-assessment.html" class="service-cta">Explore Details</a>
      </div>
'''
        html = html.replace('  </div>\n\n  <span class="services-section-label fade-up">Recurring Intelligence', op_risk + '  </div>\n\n  <span class="services-section-label fade-up">Recurring Intelligence')

    # Fix other missing / wrong prices in index.html
    html = html.replace('<div class="service-price"> / report</div>', '<div class="service-price">$99 / report</div>')
    html = html.replace('<div class="service-price"> / analysis</div>', '<div class="service-price">$149 / analysis</div>')
    html = html.replace('<div class="service-price"> / month</div>', '<div class="service-price">$199 / month</div>')
    
    # PCI-DSS is supposed to be $999 (was incorrectly replaced as $799 because GDPR is $799)
    # Let's fix PCI-DSS
    html = re.sub(r'<div class="service-price">\s*(/ assessment|\$799 / assessment)\s*</div>\s*<a href="pcidss-compliance-assessment.html"', '<div class="service-price">$999 / assessment</div>\n        <a href="pcidss-compliance-assessment.html"', html)

    # Make sure ISO 27001 is fixed if it exists
    # Wait, ISO is not in index.html, it's called Information Security Gap Assessment? Let's verify.
    
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("Fixed index.html")

def fix_subpages():
    # Fix PCIDSS 404
    if os.path.exists('pci-dss-compliance-assessment.html') and not os.path.exists('pcidss-compliance-assessment.html'):
        os.rename('pci-dss-compliance-assessment.html', 'pcidss-compliance-assessment.html')
        print("Renamed PCIDSS file to fix 404")
    
    # Fix ROC
    if os.path.exists('roc-annual-compliance-audit.html'):
        with open('roc-annual-compliance-audit.html', 'r', encoding='utf-8') as f:
            roc = f.read()
        roc = roc.replace('Complete review of MCA annual filings, statutory registers, board minutes, director KYC validity, and compliance triggers under the Companies Act 2013.', 'Annual filing reviews, ROC compliance health checks, director KYC status, and charge registration verification.')
        with open('roc-annual-compliance-audit.html', 'w', encoding='utf-8') as f:
            f.write(roc)

    # Fix Startup DPIIT
    if os.path.exists('startup-dpiit-compliance-audit.html'):
        with open('startup-dpiit-compliance-audit.html', 'r', encoding='utf-8') as f:
            startup = f.read()
        startup = startup.replace('DPIIT recognition validity check, annual compliance requirements, and Section 80-IAC tax exemption eligibility. Keep your recognition intact and your tax benefits protected.', 'DPIIT recognition review, statutory benefit checks, angel tax exemption, and startup scheme audit trails.')
        startup = startup.replace('₹18,000 / assessment', '₹18,000 / audit')
        with open('startup-dpiit-compliance-audit.html', 'w', encoding='utf-8') as f:
            f.write(startup)
            
    # Fix ISO 27001
    if os.path.exists('iso27001-gap-assessment.html'):
        with open('iso27001-gap-assessment.html', 'r', encoding='utf-8') as f:
            iso = f.read()
        iso = iso.replace('₹1,14,152', '$1,199')
        # It's probably already $1,199 based on grep but let's just make sure.
        with open('iso27001-gap-assessment.html', 'w', encoding='utf-8') as f:
            f.write(iso)

    # Fix AI Business Process
    if os.path.exists('ai-business-process-intelligence.html'):
        with open('ai-business-process-intelligence.html', 'r', encoding='utf-8') as f:
            ai_bp = f.read()
        ai_bp = re.sub(r'<span class="svc-meta-val">.*? / assessment</span>', '<span class="svc-meta-val">$707 / assessment</span>', ai_bp)
        ai_bp = re.sub(r'<div class="price-amount">.*?</div>', '<div class="price-amount">$707</div>', ai_bp)
        with open('ai-business-process-intelligence.html', 'w', encoding='utf-8') as f:
            f.write(ai_bp)

    # Fix Competitive Intelligence
    if os.path.exists('ai-competitive-intelligence.html'):
        with open('ai-competitive-intelligence.html', 'r', encoding='utf-8') as f:
            ai_ci = f.read()
        ai_ci = re.sub(r'<span class="svc-meta-val">.*? / report</span>', '<span class="svc-meta-val">$99 / report</span>', ai_ci)
        ai_ci = re.sub(r'<div class="price-amount">.*?</div>', '<div class="price-amount">$99</div>', ai_ci)
        with open('ai-competitive-intelligence.html', 'w', encoding='utf-8') as f:
            f.write(ai_ci)

    # Fix Market Entry Analysis
    if os.path.exists('ai-market-entry-analysis.html'):
        with open('ai-market-entry-analysis.html', 'r', encoding='utf-8') as f:
            ai_mea = f.read()
        ai_mea = re.sub(r'<span class="svc-meta-val">.*? / analysis</span>', '<span class="svc-meta-val">$149 / analysis</span>', ai_mea)
        ai_mea = re.sub(r'<div class="price-amount">.*?</div>', '<div class="price-amount">$149</div>', ai_mea)
        with open('ai-market-entry-analysis.html', 'w', encoding='utf-8') as f:
            f.write(ai_mea)

    # Fix Operational Risk Assessment
    if os.path.exists('ai-operational-risk-assessment.html'):
        with open('ai-operational-risk-assessment.html', 'r', encoding='utf-8') as f:
            ai_ora = f.read()
        ai_ora = re.sub(r'<span class="svc-meta-val">.*? / assessment</span>', '<span class="svc-meta-val">$1,022 / assessment</span>', ai_ora)
        ai_ora = re.sub(r'<div class="price-amount">.*?</div>', '<div class="price-amount">$1,022</div>', ai_ora)
        with open('ai-operational-risk-assessment.html', 'w', encoding='utf-8') as f:
            f.write(ai_ora)

    # Fix VextIntel Global Edition
    if os.path.exists('vextintel-global.html'):
        with open('vextintel-global.html', 'r', encoding='utf-8') as f:
            vg = f.read()
        vg = re.sub(r'<span class="svc-meta-val">.*? / month</span>', '<span class="svc-meta-val">$199 / month</span>', vg)
        vg = re.sub(r'<div class="price-amount">.*?</div>', '<div class="price-amount">$199</div>', vg)
        with open('vextintel-global.html', 'w', encoding='utf-8') as f:
            f.write(vg)

fix_index()
fix_subpages()
print("All pages fixed.")
