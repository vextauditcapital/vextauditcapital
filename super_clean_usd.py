import os
import re
import sys

# Reconfigure stdout to utf-8 to prevent cp1252 print crashes on Windows
try:
    sys.stdout.reconfigure(encoding='utf-8')
except AttributeError:
    pass

def main():
    print("Starting comprehensive Vext Audit Capital cleanup and conversion to INR...")

    # 1. Update index.html
    if os.path.exists('index.html'):
        print("Modifying index.html...")
        with open('index.html', 'r', encoding='utf-8') as f:
            index_content = f.read()

        # Insert ISO 27001 card back into the layout
        target_iso = """  <span class="services-section-label fade-up">Global Compliance &amp; Cybersecurity</span>
  <div class="services-grid">
    
    <div class="service-card fade-up fade-up-delay-1">"""

        replacement_iso = """  <span class="services-section-label fade-up">Global Compliance &amp; Cybersecurity</span>
  <div class="services-grid">
    <div class="service-card fade-up">
      <div class="service-icon">🌐</div>
      <h3 class="service-title">ISO 27001 Gap Assessment</h3>
      <p class="service-desc">Examine your information security controls against the ISO/IEC 27001:2022 framework. Full gap register delivered.</p>
      <div class="service-price">₹1,14,152 / assessment</div>
      <a href="iso27001-gap-assessment.html" class="service-cta">Explore Details</a>
    </div>
    <div class="service-card fade-up fade-up-delay-1">"""

        if target_iso in index_content:
            index_content = index_content.replace(target_iso, replacement_iso)
            print("  - Restored ISO 27001 Gap Assessment card.")
        else:
            print("  - ISO 27001 card check skipped (not found in target structure).")

        # Now replace all other USD prices in index.html to INR
        index_replacements = {
            '<div class="service-price">$999 / assessment</div>': '<div class="service-price">₹95,063 / assessment</div>',
            '<div class="service-price">$799 / assessment</div>': '<div class="service-price">₹75,964 / assessment</div>',
            '<div class="service-price">$899 / assessment</div>': '<div class="service-price">₹85,519 / assessment</div>',
            '<div class="service-price">$599 / report</div>': '<div class="service-price">₹56,975 / report</div>',
            '<div class="service-price">$499 / assessment</div>': '<div class="service-price">₹47,432 / assessment</div>',
            '<div class="service-price">$799 / audit</div>': '<div class="service-price">₹75,964 / audit</div>',
            '<div class="service-price">$707 / assessment</div>': '<div class="service-price">₹67,310 / assessment</div>',
            '<div class="service-price">$99 / report</div>': '<div class="service-price">₹9,425 / report</div>',
            '<div class="service-price">$149 / analysis</div>': '<div class="service-price">₹14,185 / analysis</div>',
            '<div class="service-price">$1,022 / assessment</div>': '<div class="service-price">₹97,300 / assessment</div>',
            '<div class="service-price">$199 / month</div>': '<div class="service-price">₹18,932 / month</div>',
        }

        for old, new in index_replacements.items():
            if old in index_content:
                index_content = index_content.replace(old, new)

        # Save index.html
        with open('index.html', 'w', encoding='utf-8') as f:
            f.write(index_content)
        print("index.html complete.")

    # 2. Update onboard.html
    if os.path.exists('onboard.html'):
        print("Modifying onboard.html...")
        with open('onboard.html', 'r', encoding='utf-8') as f:
            onboard_content = f.read()

        # Update cards (lines 149 to 166)
        card_replacements = {
            '<div class="sc" data-svc="Information Security Gap Assessment" data-amt="1199" data-cur="USD" data-lnk="https://rzp.io/rzp/FWg51kt"><div class="sc-n">Information Security Gap Assessment</div><div class="sc-p">$1,199</div></div>':
            '<div class="sc" data-svc="Information Security Gap Assessment" data-amt="114152" data-cur="INR" data-lnk="PENDING"><div class="sc-n">Information Security Gap Assessment</div><div class="sc-p">₹1,14,152</div></div>',
            
            '<div class="sc" data-svc="SOC 2 Readiness Assessment" data-amt="999" data-cur="USD" data-lnk="https://rzp.io/rzp/LurO22V"><div class="sc-n">SOC 2 Readiness Assessment</div><div class="sc-p">$999</div></div>':
            '<div class="sc" data-svc="SOC 2 Readiness Assessment" data-amt="95063" data-cur="INR" data-lnk="PENDING"><div class="sc-n">SOC 2 Readiness Assessment</div><div class="sc-p">₹95,063</div></div>',
            
            '<div class="sc" data-svc="GDPR Compliance Assessment" data-amt="799" data-cur="USD" data-lnk="https://rzp.io/rzp/pMR4io3o"><div class="sc-n">GDPR Compliance Assessment</div><div class="sc-p">$799</div></div>':
            '<div class="sc" data-svc="GDPR Compliance Assessment" data-amt="75964" data-cur="INR" data-lnk="PENDING"><div class="sc-n">GDPR Compliance Assessment</div><div class="sc-p">₹75,964</div></div>',
            
            '<div class="sc" data-svc="HIPAA Compliance Assessment" data-amt="899" data-cur="USD" data-lnk="https://rzp.io/rzp/pEy3CgD"><div class="sc-n">HIPAA Compliance Assessment</div><div class="sc-p">$899</div></div>':
            '<div class="sc" data-svc="HIPAA Compliance Assessment" data-amt="85519" data-cur="INR" data-lnk="PENDING"><div class="sc-n">HIPAA Compliance Assessment</div><div class="sc-p">₹85,519</div></div>',
            
            '<div class="sc" data-svc="PCI-DSS Compliance Assessment" data-amt="999" data-cur="USD" data-lnk="https://rzp.io/rzp/vIX6zbtu"><div class="sc-n">PCI-DSS Compliance Assessment</div><div class="sc-p">$999</div></div>':
            '<div class="sc" data-svc="PCI-DSS Compliance Assessment" data-amt="95063" data-cur="INR" data-lnk="PENDING"><div class="sc-n">PCI-DSS Compliance Assessment</div><div class="sc-p">₹95,063</div></div>',
            
            '<div class="sc" data-svc="ESG Baseline Report" data-amt="599" data-cur="USD" data-lnk="https://rzp.io/rzp/peFsINs3"><div class="sc-n">ESG Baseline Report</div><div class="sc-p">$599</div></div>':
            '<div class="sc" data-svc="ESG Baseline Report" data-amt="56975" data-cur="INR" data-lnk="PENDING"><div class="sc-n">ESG Baseline Report</div><div class="sc-p">₹56,975</div></div>',
            
            '<div class="sc" data-svc="Vendor Risk Assessment" data-amt="499" data-cur="USD" data-lnk="https://rzp.io/rzp/mub5P0h"><div class="sc-n">Vendor Risk Assessment</div><div class="sc-p">$499</div></div>':
            '<div class="sc" data-svc="Vendor Risk Assessment" data-amt="47432" data-cur="INR" data-lnk="PENDING"><div class="sc-n">Vendor Risk Assessment</div><div class="sc-p">₹47,432</div></div>',
            
            '<div class="sc" data-svc="AML / KYC Policy Audit" data-amt="799" data-cur="USD" data-lnk="https://rzp.io/rzp/eabyeCw"><div class="sc-n">AML / KYC Policy Audit</div><div class="sc-p">$799</div></div>':
            '<div class="sc" data-svc="AML / KYC Policy Audit" data-amt="75964" data-cur="INR" data-lnk="PENDING"><div class="sc-n">AML / KYC Policy Audit</div><div class="sc-p">₹75,964</div></div>',
            
            '<div class="sc" data-svc="Process Intelligence" data-amt="707" data-cur="USD" data-lnk="https://rzp.io/rzp/fFcfaX9H"><div class="sc-n">Process Intelligence</div><div class="sc-p">$707</div></div>':
            '<div class="sc" data-svc="Process Intelligence" data-amt="67310" data-cur="INR" data-lnk="https://rzp.io/rzp/iY8ndF1"><div class="sc-n">Process Intelligence</div><div class="sc-p">₹67,310</div></div>',
            
            '<div class="sc" data-svc="Competitive Intelligence" data-amt="99" data-cur="USD" data-lnk="https://rzp.io/rzp/WUd8yfc"><div class="sc-n">Competitive Intelligence</div><div class="sc-p">$99</div></div>':
            '<div class="sc" data-svc="Competitive Intelligence" data-amt="9425" data-cur="INR" data-lnk="https://rzp.io/rzp/GwTyPEN"><div class="sc-n">Competitive Intelligence</div><div class="sc-p">₹9,425</div></div>',
            
            '<div class="sc" data-svc="Market Entry Analysis" data-amt="149" data-cur="USD" data-lnk="https://rzp.io/rzp/qkMdwMw"><div class="sc-n">Market Entry Analysis</div><div class="sc-p">$149</div></div>':
            '<div class="sc" data-svc="Market Entry Analysis" data-amt="14185" data-cur="INR" data-lnk="https://rzp.io/rzp/RfGnqkck"><div class="sc-n">Market Entry Analysis</div><div class="sc-p">₹14,185</div></div>',
            
            '<div class="sc" data-svc="Operational Risk Assessment" data-amt="1022" data-cur="USD" data-lnk="https://rzp.io/rzp/06Jx04T"><div class="sc-n">Operational Risk Assessment</div><div class="sc-p">$1,022</div></div>':
            '<div class="sc" data-svc="Operational Risk Assessment" data-amt="97300" data-cur="INR" data-lnk="https://rzp.io/rzp/TeVr6dJa"><div class="sc-n">Operational Risk Assessment</div><div class="sc-p">₹97,300</div></div>',
            
            '<div class="sc" data-svc="VextIntel Global Edition" data-amt="199" data-cur="USD" data-lnk="https://rzp.io/rzp/8Jf16CNt"><div class="sc-n">VextIntel Global Edition</div><div class="sc-p">$199 / month</div></div>':
            '<div class="sc" data-svc="VextIntel Global Edition" data-amt="18932" data-cur="INR" data-lnk="PENDING"><div class="sc-n">VextIntel Global Edition</div><div class="sc-p">₹18,932 / month</div></div>'
        }

        for old, new in card_replacements.items():
            if old in onboard_content:
                onboard_content = onboard_content.replace(old, new)
            else:
                # Try with normalized spaces
                norm_old = re.sub(r'\s+', ' ', old).strip()
                # Find matching HTML element by data-svc
                match_svc = re.search(r'data-svc="([^"]+)"', old)
                if match_svc:
                    svc_name = match_svc.group(1)
                    # replace the element with exact data-svc
                    pattern = r'<div class="sc"[^>]*data-svc="' + re.escape(svc_name) + r'"[^>]*>.*?</div>'
                    onboard_content = re.sub(pattern, new, onboard_content, flags=re.S)

        # Update the 10 finalized links of Indian services in HTML cards as well (GST, DPDP, FinOps, IT, Export, VextIntel Monthly)
        onboard_content = onboard_content.replace(
            'data-svc="GST Audit & Compliance" data-amt="25000" data-cur="INR" data-lnk="https://rzp.io/rzp/MyIHpEhi"',
            'data-svc="GST Audit & Compliance" data-amt="25000" data-cur="INR" data-lnk="https://rzp.io/rzp/c8Iadz3e"'
        )
        onboard_content = onboard_content.replace(
            'data-svc="DPDP Readiness Assessment" data-amt="40000" data-cur="INR" data-lnk="https://rzp.io/rzp/b75whbt"',
            'data-svc="DPDP Readiness Assessment" data-amt="40000" data-cur="INR" data-lnk="https://rzp.io/rzp/kbkHHpJU"'
        )
        onboard_content = onboard_content.replace(
            'data-svc="Financial Operations Audit" data-amt="30000" data-cur="INR" data-lnk="https://rzp.io/rzp/O94qCEOp"',
            'data-svc="Financial Operations Audit" data-amt="30000" data-cur="INR" data-lnk="https://rzp.io/rzp/jInJsXH9"'
        )
        onboard_content = onboard_content.replace(
            'data-svc="Export Compliance" data-amt="20000" data-cur="INR" data-lnk="https://rzp.io/rzp/KlLn2kw"',
            'data-svc="Export Compliance" data-amt="20000" data-cur="INR" data-lnk="https://rzp.io/rzp/d6lMSsm"'
        )
        onboard_content = onboard_content.replace(
            'data-svc="IT & Cybersecurity Audit" data-amt="50000" data-cur="INR" data-lnk="https://rzp.io/rzp/zHkk2GW"',
            'data-svc="IT & Cybersecurity Audit" data-amt="50000" data-cur="INR" data-lnk="https://rzp.io/rzp/tffBCbc3m"'
        )
        onboard_content = onboard_content.replace(
            'data-svc="VextIntel India Retainer" data-amt="15000" data-cur="INR" data-lnk="https://rzp.io/rzp/VvoQ8SpY"',
            'data-svc="VextIntel India Retainer" data-amt="15000" data-cur="INR" data-lnk="https://rzp.io/rzp/xfTGpOLS"'
        )

        # Set all remaining 20 cards to link "PENDING"
        onboard_content = onboard_content.replace('data-lnk="https://rzp.io/rzp/A98OOcD"', 'data-lnk="PENDING"') # TDS
        onboard_content = onboard_content.replace('data-lnk="https://rzp.io/rzp/VNz3svW"', 'data-lnk="PENDING"') # ROC
        onboard_content = onboard_content.replace('data-lnk="https://rzp.io/rzp/zcsYoXk"', 'data-lnk="PENDING"') # Payroll
        onboard_content = onboard_content.replace('data-lnk="https://rzp.io/rzp/fNT724qg"', 'data-lnk="PENDING"') # ITax
        onboard_content = onboard_content.replace('data-lnk="https://rzp.io/rzp/nwRy10qr"', 'data-lnk="PENDING"') # FEMA
        onboard_content = onboard_content.replace('data-lnk="https://rzp.io/rzp/RJ6gGCtO"', 'data-lnk="PENDING"') # TP
        onboard_content = onboard_content.replace('data-lnk="https://rzp.io/rzp/slAtbzHC"', 'data-lnk="PENDING"') # MSME
        onboard_content = onboard_content.replace('data-lnk="https://rzp.io/rzp/FN6U7dQ9"', 'data-lnk="PENDING"') # Startup
        onboard_content = onboard_content.replace('data-lnk="https://rzp.io/rzp/feAb7F1B"', 'data-lnk="PENDING"') # Full Bundle
        onboard_content = onboard_content.replace('data-lnk="https://rzp.io/rzp/gmVABp0"', 'data-lnk="PENDING"') # Annual subscription
        onboard_content = onboard_content.replace('data-lnk="https://rzp.io/rzp/oMrFyN3k"', 'data-lnk="PENDING"') # VextIntel Annual

        # Now replace the JS map block
        js_map_replacement = """  var map={
    process:['Process Intelligence','67310','https://rzp.io/rzp/iY8ndF1','INR'],
    competitive:['Competitive Intelligence','9425','https://rzp.io/rzp/GwTyPEN','INR'],
    'market-entry':['Market Entry Analysis','14185','https://rzp.io/rzp/RfGnqkck','INR'],
    'operational-risk':['Operational Risk Assessment','97300','https://rzp.io/rzp/TeVr6dJa','INR'],
    gst:['GST Audit & Compliance','25000','https://rzp.io/rzp/c8Iadz3e','INR'],
    dpdp:['DPDP Readiness Assessment','40000','https://rzp.io/rzp/kbkHHpJU','INR'],
    financial:['Financial Operations Audit','30000','https://rzp.io/rzp/jInJsXH9','INR'],
    it:['IT & Cybersecurity Audit','50000','https://rzp.io/rzp/tffBCbc3m','INR'],
    export:['Export Compliance','20000','https://rzp.io/rzp/d6lMSsm','INR'],
    bundle:['Full Audit Bundle','75000','PENDING','INR'],
    vextintel:['VextIntel India Retainer','15000','https://rzp.io/rzp/xfTGpOLS','INR'],
    'vextintel-annual':['VextIntel Annual','150000','PENDING','INR'],
    tds:['TDS Compliance Audit','20000','PENDING','INR'],
    roc:['ROC Annual Compliance Audit','18000','PENDING','INR'],
    payroll:['Payroll Compliance Audit','22000','PENDING','INR'],
    fema:['FEMA Compliance Audit','25000','PENDING','INR'],
    msme:['MSME Compliance Health Check','15000','PENDING','INR'],
    startup:['Startup India DPIIT Audit','18000','PENDING','INR'],
    'annual-subscription':['Annual Compliance Subscription','60000','PENDING','INR'],
    amlkyc:['AML / KYC Policy Audit','75964','PENDING','INR'],
    esg:['ESG Baseline Report','56975','PENDING','INR'],
    gdpr:['GDPR Compliance Assessment','75964','PENDING','INR'],
    hipaa:['HIPAA Compliance Assessment','85519','PENDING','INR'],
    iso27001:['Information Security Gap Assessment','114152','PENDING','INR'],
    pcidss:['PCI-DSS Compliance Assessment','95063','PENDING','INR'],
    soc2:['SOC 2 Readiness Assessment','95063','PENDING','INR'],
    transferpricing:['Transfer Pricing Documentation','75000','PENDING','INR'],
    vendor:['Vendor Risk Assessment','47432','PENDING','INR'],
    'vextintel-global':['VextIntel Global Edition','18932','PENDING','INR'],
    incometax:['Income Tax Compliance Audit','30000','PENDING','INR']
  };"""

        # Replace JS map using regex
        match = re.search(r'var\s+map\s*=\s*\{.*?\};', onboard_content, re.S)
        if match:
            onboard_content = onboard_content.replace(match.group(0), js_map_replacement)
            print("  - Updated JS map inside onboard.html.")
        else:
            print("  - JS map NOT found in onboard.html!")

        # Always make sure currency prefix is default 'Rs. ' or '₹'
        onboard_content = onboard_content.replace("var prefix = S.cur === 'USD' ? '$' : 'Rs. ';", "var prefix = 'Rs. ';")

        # Save onboard.html
        with open('onboard.html', 'w', encoding='utf-8') as f:
            f.write(onboard_content)
        print("onboard.html complete.")

    # 3. Update all individual subpage .html files
    subpages = [
        'ai-business-process-intelligence.html',
        'ai-competitive-intelligence.html',
        'ai-market-entry-analysis.html',
        'ai-operational-risk-assessment.html',
        'aml-kyc-policy-audit.html',
        'esg-baseline-report.html',
        'gdpr-compliance-assessment.html',
        'hipaa-compliance-assessment.html',
        'iso27001-gap-assessment.html',
        'pcidss-compliance-assessment.html',
        'soc2-readiness-assessment.html',
        'vendor-risk-assessment.html',
        'vextintel-global.html'
    ]

    subpage_prices = {
        'ai-business-process-intelligence.html': {
            'from': '$707',
            'to': '₹67,310',
            'matches': [
                ('$707 excluding taxes', '₹67,310 excluding taxes'),
                ('Begin Process Intelligence - $707', 'Begin Process Intelligence - ₹67,310'),
                ('Starting From</span><span class="svc-meta-val">$707', 'Starting From</span><span class="svc-meta-val">₹67,310'),
                ('class="price-amount">$707', 'class="price-amount">₹67,310')
            ]
        },
        'ai-competitive-intelligence.html': {
            'from': '$99',
            'to': '₹9,425',
            'matches': [
                ('class="hero-price">$99', 'class="hero-price">₹9,425'),
                ('Begin Competitive Intelligence - $99', 'Begin Competitive Intelligence - ₹9,425'),
                ('Starting From</span><span class="svc-meta-val">$99', 'Starting From</span><span class="svc-meta-val">₹9,425'),
                ('class="price-amount">$99', 'class="price-amount">₹9,425')
            ]
        },
        'ai-market-entry-analysis.html': {
            'from': '$149',
            'to': '₹14,185',
            'matches': [
                ('class="hero-price">$149', 'class="hero-price">₹14,185'),
                ('Begin Market Entry Analysis - $149', 'Begin Market Entry Analysis - ₹14,185'),
                ('Starting From</span><span class="svc-meta-val">$149', 'Starting From</span><span class="svc-meta-val">₹14,185'),
                ('class="price-amount">$149', 'class="price-amount">₹14,185')
            ]
        },
        'ai-operational-risk-assessment.html': {
            'from': '$1,022',
            'to': '₹97,300',
            'matches': [
                ('class="hero-price">$1,022', 'class="hero-price">₹97,300'),
                ('Begin Risk Assessment - $1,022', 'Begin Risk Assessment - ₹97,300'),
                ('Starting From</span><span class="svc-meta-val">$1,022', 'Starting From</span><span class="svc-meta-val">₹97,300'),
                ('class="price-amount">$1,022', 'class="price-amount">₹97,300')
            ]
        },
        'aml-kyc-policy-audit.html': {
            'from': '$799',
            'to': '₹75,964',
            'matches': [
                ('Starting From</span><span class="svc-meta-val">$799', 'Starting From</span><span class="svc-meta-val">₹75,964'),
                ('class="price-amount">$799', 'class="price-amount">₹75,964')
            ]
        },
        'esg-baseline-report.html': {
            'from': '$599',
            'to': '₹56,975',
            'matches': [
                ('Starting From</span><span class="svc-meta-val">$599', 'Starting From</span><span class="svc-meta-val">₹56,975'),
                ('class="price-amount">$599', 'class="price-amount">₹56,975')
            ]
        },
        'gdpr-compliance-assessment.html': {
            'from': '$799',
            'to': '₹75,964',
            'matches': [
                ('Starting From</span><span class="svc-meta-val">$799', 'Starting From</span><span class="svc-meta-val">₹75,964'),
                ('class="price-amount">$799', 'class="price-amount">₹75,964')
            ]
        },
        'hipaa-compliance-assessment.html': {
            'from': '$899',
            'to': '₹85,519',
            'matches': [
                ('Starting From</span><span class="svc-meta-val">$899', 'Starting From</span><span class="svc-meta-val">₹85,519'),
                ('class="price-amount">$899', 'class="price-amount">₹85,519')
            ]
        },
        'iso27001-gap-assessment.html': {
            'from': '$1,199',
            'to': '₹1,14,152',
            'matches': [
                ('Starting From</span><span class="svc-meta-val">$1,199', 'Starting From</span><span class="svc-meta-val">₹1,14,152'),
                ('class="price-amount">$1,199', 'class="price-amount">₹1,14,152')
            ]
        },
        'pcidss-compliance-assessment.html': {
            'from': '$999',
            'to': '₹95,063',
            'matches': [
                ('Starting From</span><span class="svc-meta-val">$999', 'Starting From</span><span class="svc-meta-val">₹95,063'),
                ('class="price-amount">$999', 'class="price-amount">₹95,063')
            ]
        },
        'soc2-readiness-assessment.html': {
            'from': '$999',
            'to': '₹95,063',
            'matches': [
                ('Starting From</span><span class="svc-meta-val">$999', 'Starting From</span><span class="svc-meta-val">₹95,063'),
                ('class="price-amount">$999', 'class="price-amount">₹95,063')
            ]
        },
        'vendor-risk-assessment.html': {
            'from': '$499',
            'to': '₹47,432',
            'matches': [
                ('Starting From</span><span class="svc-meta-val">$499', 'Starting From</span><span class="svc-meta-val">₹47,432'),
                ('class="price-amount">$499', 'class="price-amount">₹47,432')
            ]
        },
        'vextintel-global.html': {
            'from': '$199',
            'to': '₹18,932',
            'matches': [
                ('Starting From</span><span class="svc-meta-val">$199', 'Starting From</span><span class="svc-meta-val">₹18,932'),
                ('class="price-amount">$199', 'class="price-amount">₹18,932')
            ]
        }
    }

    # Global cross-page footer/related cards prices translation helper
    general_replacements = {
        '$1,199 / assessment': '₹1,14,152 / assessment',
        '$999 / assessment': '₹95,063 / assessment',
        '$799 / assessment': '₹75,964 / assessment',
        '$899 / assessment': '₹85,519 / assessment',
        '$599 / report': '₹56,975 / report',
        '$499 / assessment': '₹47,432 / assessment',
        '$799 / audit': '₹75,964 / audit',
        '$199 / month': '₹18,932 / month'
    }

    for fname in subpages:
        if os.path.exists(fname):
            print(f"Modifying subpage: {fname}...")
            with open(fname, 'r', encoding='utf-8') as f:
                content = f.read()

            # Apply specific card matches
            if fname in subpage_prices:
                for old, new in subpage_prices[fname]['matches']:
                    content = content.replace(old, new)
                    content = re.sub(re.escape(old).replace(r'\ ', r'\s*'), new, content)

            # Apply general cross-page footer replacements
            for old, new in general_replacements.items():
                content = content.replace(old, new)

            # Extra safety: replace any leftover meta-val patterns
            content = re.sub(r'Starting From</span><span class="svc-meta-val">\s*\$1,199', 'Starting From</span><span class="svc-meta-val">₹1,14,152', content)
            content = re.sub(r'Starting From</span><span class="svc-meta-val">\s*\$999', 'Starting From</span><span class="svc-meta-val">₹95,063', content)
            content = re.sub(r'Starting From</span><span class="svc-meta-val">\s*\$899', 'Starting From</span><span class="svc-meta-val">₹85,519', content)
            content = re.sub(r'Starting From</span><span class="svc-meta-val">\s*\$799', 'Starting From</span><span class="svc-meta-val">₹75,964', content)
            content = re.sub(r'Starting From</span><span class="svc-meta-val">\s*\$599', 'Starting From</span><span class="svc-meta-val">₹56,975', content)
            content = re.sub(r'Starting From</span><span class="svc-meta-val">\s*\$499', 'Starting From</span><span class="svc-meta-val">₹47,432', content)
            content = re.sub(r'Starting From</span><span class="svc-meta-val">\s*\$199', 'Starting From</span><span class="svc-meta-val">₹18,932', content)

            content = re.sub(r'class="price-amount">\s*\$1,199', 'class="price-amount">₹1,14,152', content)
            content = re.sub(r'class="price-amount">\s*\$999', 'class="price-amount">₹95,063', content)
            content = re.sub(r'class="price-amount">\s*\$899', 'class="price-amount">₹85,519', content)
            content = re.sub(r'class="price-amount">\s*\$799', 'class="price-amount">₹75,964', content)
            content = re.sub(r'class="price-amount">\s*\$599', 'class="price-amount">₹56,975', content)
            content = re.sub(r'class="price-amount">\s*\$499', 'class="price-amount">₹47,432', content)
            content = re.sub(r'class="price-amount">\s*\$199', 'class="price-amount">₹18,932', content)

            with open(fname, 'w', encoding='utf-8') as f:
                f.write(content)

    print("Cleanup and INR conversions complete!")

if __name__ == '__main__':
    main()
