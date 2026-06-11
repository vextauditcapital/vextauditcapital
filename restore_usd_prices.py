import os
import sys
import re

try:
    sys.stdout.reconfigure(encoding='utf-8')
except AttributeError:
    pass

def main():
    print("Starting restoration of USD prices...")

    # 1. Update onboard.html
    if os.path.exists('onboard.html'):
        print("Modifying onboard.html...")
        with open('onboard.html', 'r', encoding='utf-8') as f:
            onboard_content = f.read()

        card_replacements = {
            # Information Security Gap Assessment
            '<div class="sc" data-svc="Information Security Gap Assessment" data-amt="114152" data-cur="INR" data-lnk="PENDING"><div class="sc-n">Information Security Gap Assessment</div><div class="sc-p">₹1,14,152</div></div>':
            '<div class="sc" data-svc="Information Security Gap Assessment" data-amt="1199" data-cur="USD" data-lnk="PENDING"><div class="sc-n">Information Security Gap Assessment</div><div class="sc-p">$1,199</div></div>',
            
            # SOC 2
            '<div class="sc" data-svc="SOC 2 Readiness Assessment" data-amt="95063" data-cur="INR" data-lnk="PENDING"><div class="sc-n">SOC 2 Readiness Assessment</div><div class="sc-p">₹95,063</div></div>':
            '<div class="sc" data-svc="SOC 2 Readiness Assessment" data-amt="999" data-cur="USD" data-lnk="PENDING"><div class="sc-n">SOC 2 Readiness Assessment</div><div class="sc-p">$999</div></div>',
            
            # GDPR
            '<div class="sc" data-svc="GDPR Compliance Assessment" data-amt="75964" data-cur="INR" data-lnk="PENDING"><div class="sc-n">GDPR Compliance Assessment</div><div class="sc-p">₹75,964</div></div>':
            '<div class="sc" data-svc="GDPR Compliance Assessment" data-amt="799" data-cur="USD" data-lnk="PENDING"><div class="sc-n">GDPR Compliance Assessment</div><div class="sc-p">$799</div></div>',
            
            # HIPAA
            '<div class="sc" data-svc="HIPAA Compliance Assessment" data-amt="85519" data-cur="INR" data-lnk="PENDING"><div class="sc-n">HIPAA Compliance Assessment</div><div class="sc-p">₹85,519</div></div>':
            '<div class="sc" data-svc="HIPAA Compliance Assessment" data-amt="899" data-cur="USD" data-lnk="PENDING"><div class="sc-n">HIPAA Compliance Assessment</div><div class="sc-p">$899</div></div>',
            
            # PCI-DSS
            '<div class="sc" data-svc="PCI-DSS Compliance Assessment" data-amt="95063" data-cur="INR" data-lnk="PENDING"><div class="sc-n">PCI-DSS Compliance Assessment</div><div class="sc-p">₹95,063</div></div>':
            '<div class="sc" data-svc="PCI-DSS Compliance Assessment" data-amt="999" data-cur="USD" data-lnk="PENDING"><div class="sc-n">PCI-DSS Compliance Assessment</div><div class="sc-p">$999</div></div>',
            
            # ESG
            '<div class="sc" data-svc="ESG Baseline Report" data-amt="56975" data-cur="INR" data-lnk="PENDING"><div class="sc-n">ESG Baseline Report</div><div class="sc-p">₹56,975</div></div>':
            '<div class="sc" data-svc="ESG Baseline Report" data-amt="599" data-cur="USD" data-lnk="PENDING"><div class="sc-n">ESG Baseline Report</div><div class="sc-p">$599</div></div>',
            
            # Vendor Risk
            '<div class="sc" data-svc="Vendor Risk Assessment" data-amt="47432" data-cur="INR" data-lnk="PENDING"><div class="sc-n">Vendor Risk Assessment</div><div class="sc-p">₹47,432</div></div>':
            '<div class="sc" data-svc="Vendor Risk Assessment" data-amt="499" data-cur="USD" data-lnk="PENDING"><div class="sc-n">Vendor Risk Assessment</div><div class="sc-p">$499</div></div>',
            
            # AML / KYC
            '<div class="sc" data-svc="AML / KYC Policy Audit" data-amt="75964" data-cur="INR" data-lnk="PENDING"><div class="sc-n">AML / KYC Policy Audit</div><div class="sc-p">₹75,964</div></div>':
            '<div class="sc" data-svc="AML / KYC Policy Audit" data-amt="799" data-cur="USD" data-lnk="PENDING"><div class="sc-n">AML / KYC Policy Audit</div><div class="sc-p">$799</div></div>',
            
            # Process Intelligence
            '<div class="sc" data-svc="Process Intelligence" data-amt="67310" data-cur="INR" data-lnk="https://rzp.io/rzp/iY8ndF1"><div class="sc-n">Process Intelligence</div><div class="sc-p">₹67,310</div></div>':
            '<div class="sc" data-svc="Process Intelligence" data-amt="707" data-cur="USD" data-lnk="https://rzp.io/rzp/iY8ndF1"><div class="sc-n">Process Intelligence</div><div class="sc-p">$707</div></div>',
            
            # Competitive Intelligence
            '<div class="sc" data-svc="Competitive Intelligence" data-amt="9425" data-cur="INR" data-lnk="https://rzp.io/rzp/GwTyPEN"><div class="sc-n">Competitive Intelligence</div><div class="sc-p">₹9,425</div></div>':
            '<div class="sc" data-svc="Competitive Intelligence" data-amt="99" data-cur="USD" data-lnk="https://rzp.io/rzp/GwTyPEN"><div class="sc-n">Competitive Intelligence</div><div class="sc-p">$99</div></div>',
            
            # Market Entry
            '<div class="sc" data-svc="Market Entry Analysis" data-amt="14185" data-cur="INR" data-lnk="https://rzp.io/rzp/RfGnqkck"><div class="sc-n">Market Entry Analysis</div><div class="sc-p">₹14,185</div></div>':
            '<div class="sc" data-svc="Market Entry Analysis" data-amt="149" data-cur="USD" data-lnk="https://rzp.io/rzp/RfGnqkck"><div class="sc-n">Market Entry Analysis</div><div class="sc-p">$149</div></div>',
            
            # Operational Risk
            '<div class="sc" data-svc="Operational Risk Assessment" data-amt="97300" data-cur="INR" data-lnk="https://rzp.io/rzp/TeVr6dJa"><div class="sc-n">Operational Risk Assessment</div><div class="sc-p">₹97,300</div></div>':
            '<div class="sc" data-svc="Operational Risk Assessment" data-amt="1022" data-cur="USD" data-lnk="https://rzp.io/rzp/TeVr6dJa"><div class="sc-n">Operational Risk Assessment</div><div class="sc-p">$1,022</div></div>',
            
            # VextIntel Global Edition
            '<div class="sc" data-svc="VextIntel Global Edition" data-amt="18932" data-cur="INR" data-lnk="PENDING"><div class="sc-n">VextIntel Global Edition</div><div class="sc-p">₹18,932 / month</div></div>':
            '<div class="sc" data-svc="VextIntel Global Edition" data-amt="199" data-cur="USD" data-lnk="PENDING"><div class="sc-n">VextIntel Global Edition</div><div class="sc-p">$199 / month</div></div>'
        }

        for old, new in card_replacements.items():
            if old in onboard_content:
                onboard_content = onboard_content.replace(old, new)
                print(f"  - Replaced card for: {old.split('data-svc=\"')[1].split('\"')[0]}")
            else:
                # Let's search with regex as fallback
                svc_match = re.search(r'data-svc="([^"]+)"', old)
                if svc_match:
                    svc_name = svc_match.group(1)
                    pattern = r'<div class="sc"[^>]*data-svc="' + re.escape(svc_name) + r'"[^>]*>.*?</div>'
                    if re.search(pattern, onboard_content, re.S):
                        onboard_content = re.sub(pattern, new, onboard_content, flags=re.S)
                        print(f"  - Replaced card for: {svc_name} (via pattern)")

        # Update JS map back to original USD
        js_map_replacement = """  var map={
    process:['Process Intelligence','707','https://rzp.io/rzp/iY8ndF1','USD'],
    competitive:['Competitive Intelligence','99','https://rzp.io/rzp/GwTyPEN','USD'],
    'market-entry':['Market Entry Analysis','149','https://rzp.io/rzp/RfGnqkck','USD'],
    'operational-risk':['Operational Risk Assessment','1022','https://rzp.io/rzp/TeVr6dJa','USD'],
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
    amlkyc:['AML / KYC Policy Audit','799','PENDING','USD'],
    esg:['ESG Baseline Report','599','PENDING','USD'],
    gdpr:['GDPR Compliance Assessment','799','PENDING','USD'],
    hipaa:['HIPAA Compliance Assessment','899','PENDING','USD'],
    iso27001:['Information Security Gap Assessment','1199','PENDING','USD'],
    pcidss:['PCI-DSS Compliance Assessment','999','PENDING','USD'],
    soc2:['SOC 2 Readiness Assessment','999','PENDING','USD'],
    transferpricing:['Transfer Pricing Documentation','75000','PENDING','INR'],
    vendor:['Vendor Risk Assessment','499','PENDING','USD'],
    'vextintel-global':['VextIntel Global Edition','199','PENDING','USD'],
    incometax:['Income Tax Compliance Audit','30000','PENDING','INR']
  };"""

        match = re.search(r'var\s+map\s*=\s*\{.*?\};', onboard_content, re.S)
        if match:
            onboard_content = onboard_content.replace(match.group(0), js_map_replacement)
            print("  - Restored JS map inside onboard.html to match original USD prices.")
        else:
            print("  - JS map NOT found in onboard.html!")

        # Update fillSum function to beautifully display original price, 18% GST, and total
        new_fillsum = """function fillSum(){
 var amt = parseFloat(S.amt);
 var cur = S.cur || 'INR';
 var prefix = cur === 'USD' ? '$' : '₹';
 var locale = cur === 'USD' ? 'en-US' : 'en-IN';
 
 var baseStr = prefix + amt.toLocaleString(locale, {minimumFractionDigits: cur==='USD'?2:0, maximumFractionDigits: cur==='USD'?2:0});
 var gstVal = Math.round(amt * 0.18 * 100) / 100;
 var gstStr = prefix + gstVal.toLocaleString(locale, {minimumFractionDigits: cur==='USD'?2:0, maximumFractionDigits: cur==='USD'?2:0});
 var totVal = amt + gstVal;
 var totStr = prefix + totVal.toLocaleString(locale, {minimumFractionDigits: cur==='USD'?2:0, maximumFractionDigits: cur==='USD'?2:0});
 
 g('ss').textContent = S.svc;
 g('sa').innerHTML = `
   <div style="display:flex; flex-direction:column; gap:4px; align-items:flex-end; text-align:right;">
     <div style="font-size:13px; opacity:0.85;">Base Price: <strong style="color:var(--cream);">${baseStr}</strong></div>
     <div style="font-size:13px; opacity:0.85;">GST (18%): <strong style="color:var(--cream);">${gstStr}</strong></div>
     <div style="font-size:15px; margin-top:4px; border-top:1px solid rgba(197,160,89,0.2); padding-top:4px; color:var(--gold);">Total (Incl. GST): <strong>${totStr}</strong></div>
   </div>
 `;
 g('sn').textContent = g('fn').value;
 g('sc2').textContent = g('fc').value;
 g('se').textContent = g('fe').value;
 g('sph').textContent = g('fp').value;
 g('sco').textContent = g('fco').value;
}"""

        # Replace fillSum
        onboard_content = re.sub(r'function fillSum\(.*?\)\{.*?\}', new_fillsum, onboard_content, flags=re.S)
        print("  - Updated fillSum in onboard.html to display base, 18% GST, and total.")

        # Update prefix logic so that Step 4 works dynamically with prefix variable
        onboard_content = onboard_content.replace(
            "g('sa').textContent=prefix+amt.toLocaleString(S.cur==='USD'?'en-US':'en-IN');",
            "" # Removed since fillSum handles the innerHTML now
        )

        with open('onboard.html', 'w', encoding='utf-8') as f:
            f.write(onboard_content)

    # 2. Update index.html
    if os.path.exists('index.html'):
        print("Modifying index.html...")
        with open('index.html', 'r', encoding='utf-8') as f:
            index_content = f.read()

        index_replacements = {
            '₹1,14,152 / assessment': '$1,199 / assessment',
            '₹95,063 / assessment': '$999 / assessment',
            '₹75,964 / assessment': '$799 / assessment',
            '₹85,519 / assessment': '$899 / assessment',
            '₹56,975 / report': '$599 / report',
            '₹47,432 / assessment': '$499 / assessment',
            '₹75,964 / audit': '$799 / audit',
            '₹67,310 / assessment': '$707 / assessment',
            '₹9,425 / report': '$99 / report',
            '₹14,185 / analysis': '$149 / analysis',
            '₹97,300 / assessment': '$1,022 / assessment',
            '₹18,932 / month': '$199 / month',
        }

        for old, new in index_replacements.items():
            if old in index_content:
                index_content = index_content.replace(old, new)
                print(f"  - index.html: replaced {old} with {new}")

        with open('index.html', 'w', encoding='utf-8') as f:
            f.write(index_content)

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

    subpage_reversions = {
        'ai-business-process-intelligence.html': [
            ('₹67,310 excluding taxes', '$707 excluding taxes'),
            ('Begin Process Intelligence - ₹67,310', 'Begin Process Intelligence - $707'),
            ('Starting From</span><span class="svc-meta-val">₹67,310', 'Starting From</span><span class="svc-meta-val">$707'),
            ('class="price-amount">₹67,310', 'class="price-amount">$707')
        ],
        'ai-competitive-intelligence.html': [
            ('class="hero-price">₹9,425', 'class="hero-price">$99'),
            ('Begin Competitive Intelligence - ₹9,425', 'Begin Competitive Intelligence - $99'),
            ('Starting From</span><span class="svc-meta-val">₹9,425', 'Starting From</span><span class="svc-meta-val">$99'),
            ('class="price-amount">₹9,425', 'class="price-amount">$99')
        ],
        'ai-market-entry-analysis.html': [
            ('class="hero-price">₹14,185', 'class="hero-price">$149'),
            ('Begin Market Entry Analysis - ₹14,185', 'Begin Market Entry Analysis - $149'),
            ('Starting From</span><span class="svc-meta-val">₹14,185', 'Starting From</span><span class="svc-meta-val">$149'),
            ('class="price-amount">₹14,185', 'class="price-amount">$149')
        ],
        'ai-operational-risk-assessment.html': [
            ('class="hero-price">₹97,300', 'class="hero-price">$1,022'),
            ('Begin Risk Assessment - ₹97,300', 'Begin Risk Assessment - $1,022'),
            ('Starting From</span><span class="svc-meta-val">₹97,300', 'Starting From</span><span class="svc-meta-val">$1,022'),
            ('class="price-amount">₹97,300', 'class="price-amount">$1,022')
        ],
        'aml-kyc-policy-audit.html': [
            ('Starting From</span><span class="svc-meta-val">₹75,964', 'Starting From</span><span class="svc-meta-val">$799'),
            ('class="price-amount">₹75,964', 'class="price-amount">$799')
        ],
        'esg-baseline-report.html': [
            ('Starting From</span><span class="svc-meta-val">₹56,975', 'Starting From</span><span class="svc-meta-val">$599'),
            ('class="price-amount">₹56,975', 'class="price-amount">$599')
        ],
        'gdpr-compliance-assessment.html': [
            ('Starting From</span><span class="svc-meta-val">₹75,964', 'Starting From</span><span class="svc-meta-val">$799'),
            ('class="price-amount">₹75,964', 'class="price-amount">$799')
        ],
        'hipaa-compliance-assessment.html': [
            ('Starting From</span><span class="svc-meta-val">₹85,519', 'Starting From</span><span class="svc-meta-val">$899'),
            ('class="price-amount">₹85,519', 'class="price-amount">$899')
        ],
        'iso27001-gap-assessment.html': [
            ('Starting From</span><span class="svc-meta-val">₹1,14,152', 'Starting From</span><span class="svc-meta-val">$1,199'),
            ('class="price-amount">₹1,14,152', 'class="price-amount">$1,199')
        ],
        'pcidss-compliance-assessment.html': [
            ('Starting From</span><span class="svc-meta-val">₹95,063', 'Starting From</span><span class="svc-meta-val">$999'),
            ('class="price-amount">₹95,063', 'class="price-amount">$999')
        ],
        'soc2-readiness-assessment.html': [
            ('Starting From</span><span class="svc-meta-val">₹95,063', 'Starting From</span><span class="svc-meta-val">$999'),
            ('class="price-amount">₹95,063', 'class="price-amount">$999')
        ],
        'vendor-risk-assessment.html': [
            ('Starting From</span><span class="svc-meta-val">₹47,432', 'Starting From</span><span class="svc-meta-val">$499'),
            ('class="price-amount">₹47,432', 'class="price-amount">$499')
        ],
        'vextintel-global.html': [
            ('Starting From</span><span class="svc-meta-val">₹18,932', 'Starting From</span><span class="svc-meta-val">$199'),
            ('class="price-amount">₹18,932', 'class="price-amount">$199')
        ]
    }

    general_subpage_reversions = {
        '₹1,14,152 / assessment': '$1,199 / assessment',
        '₹95,063 / assessment': '$999 / assessment',
        '₹75,964 / assessment': '$799 / assessment',
        '₹85,519 / assessment': '$899 / assessment',
        '₹56,975 / report': '$599 / report',
        '₹47,432 / assessment': '$499 / assessment',
        '₹75,964 / audit': '$799 / audit',
        '₹18,932 / month': '$199 / month',
    }

    for fname in subpages:
        if os.path.exists(fname):
            print(f"Reverting subpage: {fname}...")
            with open(fname, 'r', encoding='utf-8') as f:
                content = f.read()

            # Apply specific card matches
            if fname in subpage_reversions:
                for old, new in subpage_reversions[fname]:
                    content = content.replace(old, new)

            # Apply general cross-page footer replacements
            for old, new in general_subpage_reversions.items():
                content = content.replace(old, new)

            with open(fname, 'w', encoding='utf-8') as f:
                f.write(content)

    print("Restoration of USD prices completed successfully!")

if __name__ == '__main__':
    main()
