import glob
import re

rupee = '\u20b9'

table = {
    'GST Audit & Compliance': f'{rupee}25,000',
    'TDS Compliance Audit': f'{rupee}20,000',
    'ROC Annual Compliance Audit': f'{rupee}18,000',
    'Payroll Compliance Audit': f'{rupee}22,000',
    'Income Tax Compliance Audit': f'{rupee}30,000',
    'FEMA Compliance Audit': f'{rupee}25,000',
    'DPDP Readiness Assessment': f'{rupee}40,000',
    'Financial Operations Audit': f'{rupee}30,000',
    'Export Compliance': f'{rupee}20,000',
    'Transfer Pricing Documentation': f'{rupee}75,000',
    'MSME Compliance Health Check': f'{rupee}15,000',
    'Startup India DPIIT Audit': f'{rupee}18,000',
    'IT & Cybersecurity Audit': f'{rupee}50,000',
    'Full Audit Bundle': f'{rupee}75,000',
    'Information Security Gap Assessment': '$1,199',
    'SOC 2 Readiness Assessment': '$999',
    'GDPR Compliance Assessment': '$799',
    'HIPAA Compliance Assessment': '$899',
    'PCI-DSS Compliance Assessment': '$999',
    'ESG Baseline Report': '$599',
    'Vendor Risk Assessment': '$499',
    'AML / KYC Policy Audit': '$799',
    'Process Intelligence': '$707',
    'Competitive Intelligence': '$99',
    'Market Entry Analysis': '$149',
    'Operational Risk Assessment': '$1,022',
    'VextIntel India Retainer': f'{rupee}15,000',
    'VextIntel Global Edition': '$199',
    'Annual Compliance Subscription': f'{rupee}60,000',
    'VextIntel Annual (India)': f'{rupee}1,50,000',
    'VextIntel Annual': f'{rupee}1,50,000'
}

html_files = glob.glob('*.html')

for filepath in html_files:
    if filepath in ['onboard.html', 'index.html', 'iso27001-gap-assessment.html']:
        continue
        
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    matched_name = None
    for name in table:
        if name == 'Full Audit Bundle': continue
        if name == 'Startup India DPIIT Audit' and 'startup' in filepath.lower():
            matched_name = name
            break
        name_clean = re.sub(r'[^a-zA-Z0-9 ]', '', name).lower().strip()
        title_match = re.search(r'<title>(.*?)</title>', content, re.IGNORECASE)
        if title_match:
            title_clean = re.sub(r'[^a-zA-Z0-9 ]', '', title_match.group(1)).lower()
            if name_clean in title_clean:
                matched_name = name
                break
                
    if not matched_name:
        if 'process' in filepath.lower(): matched_name = 'Process Intelligence'
        elif 'competitive' in filepath.lower(): matched_name = 'Competitive Intelligence'
        elif 'market' in filepath.lower(): matched_name = 'Market Entry Analysis'
        elif 'operational' in filepath.lower(): matched_name = 'Operational Risk Assessment'
        elif 'startup' in filepath.lower(): matched_name = 'Startup India DPIIT Audit'

    if matched_name:
        price = table[matched_name]
        
        # In hero price (for AI services) they specifically requested 'excluding taxes' for 
        if 'ai-business-process-intelligence' in filepath:
            content = re.sub(r'<div class="hero-price">.*?</div>', f'<div class="hero-price">{price} excluding taxes</div>', content)
        else:
            content = re.sub(r'<div class="hero-price">.*?</div>', f'<div class="hero-price">{price}</div>', content)
        
        def replace_meta(m):
            text = m.group(0)
            suffix = ''
            if '/ month' in text: suffix = ' / month'
            elif '/ year' in text: suffix = ' / year'
            elif '/ assessment' in text: suffix = ' / assessment'
            elif '/ analysis' in text: suffix = ' / analysis'
            elif '/ report' in text: suffix = ' / report'
            elif '/ engagement' in text: suffix = ' / engagement'
            elif '/ audit' in text: suffix = ' / audit'
            elif '/ review' in text: suffix = ' / review'
            
            return f'<span class="svc-meta-val">{price}{suffix}</span>'
            
        content = re.sub(r'<span class="svc-meta-val">.*?</span>', replace_meta, content, count=1)
        
        def replace_btn(m):
            txt = m.group(2)
            if ' \u2014 ' in txt:
                txt = re.sub(r' \u2014 .*', f' \u2014 {price}', txt)
            elif ' - ' in txt:
                txt = re.sub(r' - .*', f' - {price}', txt)
            return f'<a href="{m.group(1)}" class="btn-primary">{txt}</a>'
        content = re.sub(r'<a href="([^"]+)" class="btn-primary">(.*?)</a>', replace_btn, content)
        
        content = re.sub(r'<div class="price-amount">.*?</div>', f'<div class="price-amount">{price}</div>', content)

    # replace related services grid prices
    def replace_rel_price(match):
        rel_title = match.group(1).strip()
        rel_price = match.group(2)
        
        found_price = None
        for k, v in table.items():
            if rel_title.lower() == k.lower():
                found_price = v
                break
        
        if not found_price:
            for k, v in table.items():
                if rel_title.lower() in k.lower() or k.lower() in rel_title.lower():
                    found_price = v
                    break
                
        if found_price:
            suffix = ''
            if '/ month' in rel_price: suffix = ' / month'
            elif '/ assessment' in rel_price: suffix = ' / assessment'
            elif '/ year' in rel_price: suffix = ' / year'
            elif '/ analysis' in rel_price: suffix = ' / analysis'
            elif '/ report' in rel_price: suffix = ' / report'
            elif '/ engagement' in rel_price: suffix = ' / engagement'
            elif '/ audit' in rel_price: suffix = ' / audit'
            elif '/ review' in rel_price: suffix = ' / review'
            elif '/ check' in rel_price: suffix = ' / check'
            
            return f'<div class="rel-title">{rel_title}</div><div class="rel-price">{found_price}{suffix}</div>'
        return match.group(0)
        
    content = re.sub(r'<div class="rel-title">(.*?)</div><div class="rel-price">(.*?)</div>', replace_rel_price, content)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

print("Subpages cleaned.")