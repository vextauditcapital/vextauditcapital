import os
import re

FILES_TO_UNIFY = {
    'gst-audit-compliance.html': {
        'title': 'GST Audit & Compliance',
        'cat': 'India Core Services',
        'price': '₹25,000 / engagement',
        'amount': '₹25,000',
        'period': '/ engagement - fixed fee'
    },
    'dpdp-readiness-assessment.html': {
        'title': 'DPDP Readiness Assessment',
        'cat': 'India Core Services',
        'price': '₹40,000 / assessment',
        'amount': '₹40,000',
        'period': '/ assessment - fixed fee'
    },
    'financial-operations-audit.html': {
        'title': 'Financial Operations Audit',
        'cat': 'India Core Services',
        'price': '₹30,000 / audit',
        'amount': '₹30,000',
        'period': '/ audit - fixed fee'
    },
    'it-cybersecurity-audit.html': {
        'title': 'IT & Cybersecurity Audit',
        'cat': 'India Core Services',
        'price': '₹50,000 / assessment',
        'amount': '₹50,000',
        'period': '/ assessment - fixed fee'
    },
    'export-compliance.html': {
        'title': 'Export Compliance',
        'cat': 'India Core Services',
        'price': '₹20,000 / review',
        'amount': '₹20,000',
        'period': '/ review - fixed fee'
    },
    'vextintel-monthly-retainer.html': {
        'title': 'VextIntel Monthly Retainer',
        'cat': 'Recurring Intelligence',
        'price': '₹15,000 / month',
        'amount': '₹15,000',
        'period': '/ month - cancel anytime'
    }
}

def extract_content(filename):
    with open(filename, 'r', encoding='utf-8', errors='ignore') as f:
        html = f.read()
    
    sub = ''
    sub_match = re.search(r'<p class="hero-sub">(.*?)</p>', html, re.S)
    if sub_match: sub = sub_match.group(1).strip()
    
    overview_h2 = ''
    h2_match = re.search(r'<h2 class="sec-h2">(.*?)</h2>', html, re.S)
    if h2_match: overview_h2 = h2_match.group(1).strip()
    
    overview_p = []
    promise_match = re.search(r'<section class="promise-section">.*?</section>', html, re.S)
    if promise_match:
        ps = re.findall(r'<p>(.*?)</p>', promise_match.group(0), re.S)
        overview_p = [p.strip() for p in ps]
        
    audit_items = []
    del_grid = re.search(r'<div class="del-grid">(.*?)</div>\s*</section>', html, re.S)
    if del_grid:
        cards = re.findall(r'<div class="del-card">.*?<div class="del-title">(.*?)</div><div class="del-body">(.*?)</div></div>', del_grid.group(1), re.S)
        for t, d in cards:
            audit_items.append({'title': t.strip(), 'desc': d.strip()})
            
    del_items = []
    str_grid = re.search(r'<div class="str-grid">(.*?)</div>\s*</section>', html, re.S)
    if str_grid:
        cards = re.findall(r'<div class="str-item">.*?<div class="str-title">(.*?)</div><div class="str-body">(.*?)</div></div></div>', str_grid.group(1), re.S)
        for t, d in cards:
            del_items.append({'title': t.strip(), 'desc': d.strip()})

    return {
        'sub': sub,
        'overview_h2': overview_h2,
        'overview_p': overview_p,
        'audit_items': audit_items,
        'del_items': del_items
    }

def build_new_page(template, config, content, filename):
    page = template
    
    # Simple replaces for strings
    page = re.sub(r'<title>.*?</title>', f'<title>{config["title"]} | Vext Audit Capital</title>', page, count=1, flags=re.S)
    page = re.sub(r'<span style="color:var\(--gold\);opacity:0\.8;">.*?</span>', f'<span style="color:var(--gold);opacity:0.8;">{config["title"]}</span>', page, count=1)
    page = re.sub(r'<div class="svc-cat-badge">.*?</div>', f'<div class="svc-cat-badge">{config["cat"]}</div>', page, count=1)
    
    # Fix the main H1. For GST Audit & Compliance, split by space into 2 lines for aesthetics
    words = config['title'].split()
    h1_top = " ".join(words[:-1]) if len(words) > 1 else config['title']
    h1_bot = words[-1] if len(words) > 1 else ""
    page = re.sub(r'<h1>.*?<br/><span>.*?</span></h1>', f'<h1>{h1_top}<br/><span>{h1_bot}</span></h1>', page, count=1, flags=re.S)
    
    page = re.sub(r'<p class="svc-hero-sub">.*?</p>', f'<p class="svc-hero-sub">{content["sub"]}</p>', page, count=1, flags=re.S)
    
    page = re.sub(r'<span class="svc-meta-val">.*? / review</span>', f'<span class="svc-meta-val">{config["price"]}</span>', page, count=1)
    
    page = re.sub(r'<h2 class="fade-up">.*?<br/><span>.*?</span></h2>', f'<h2 class="fade-up">{content["overview_h2"]}</h2>', page, count=1, flags=re.S)
    
    # Paragraphs replacement
    p_tags = ''.join([f'<p class="fade-up">{p}</p>\n' for p in content['overview_p']])
    # We will replace the two paragraphs in the template (and the risk block) with our new paragraphs
    pattern_p = r'<p class="fade-up">Every company registered.*?</p>\s*<p class="fade-up">Our ROC Annual.*?</p>\s*<div class="risk-block fade-up">.*?</div>'
    page = re.sub(pattern_p, p_tags, page, flags=re.S)
    
    # Audit Grid replacement
    icons = ['🛡', '📊', '🔍', '⚖', '📡', '💡']
    audit_html = ''
    for i, item in enumerate(content['audit_items']):
        icon = icons[i % len(icons)]
        audit_html += f'<div class="audit-item"><div class="audit-item-icon">{icon}</div><div class="audit-item-title">{item["title"]}</div><div class="audit-item-desc">{item["desc"]}</div></div>\n'
    page = re.sub(r'<div class="audit-grid fade-up">.*?</div>', f'<div class="audit-grid fade-up">\n{audit_html}</div>', page, flags=re.S, count=1)
    
    # Del List replacement
    del_html = ''
    for item in content['del_items']:
        del_html += f'<div class="del-item"><div class="del-dot"></div><div class="del-text"><strong>{item["title"]}</strong> - {item["desc"]}</div></div>\n'
    page = re.sub(r'<div class="del-list fade-up">.*?</div>', f'<div class="del-list fade-up">\n{del_html}</div>', page, flags=re.S, count=1)
    
    # Sidebar
    page = re.sub(r'<div class="price-amount">.*?</div>', f'<div class="price-amount">{config["amount"]}</div>', page, count=1)
    page = re.sub(r'<span class="price-period">.*?</span>', f'<span class="price-period">{config["period"]}</span>', page, count=1)
    
    # Features list in sidebar
    features_html = ''
    for item in content['audit_items'][:6]:
        features_html += f'<li>{item["title"]}</li>\n'
    if not features_html:
        features_html = '<li>Comprehensive Audit</li>'
    page = re.sub(r'<ul class="sidebar-features">.*?</ul>', f'<ul class="sidebar-features">\n{features_html}</ul>', page, flags=re.S, count=1)
    
    # Button link
    service_id = filename.split('-')[0]
    page = re.sub(r'<a href="onboard\.html\?service=.*?" class="btn-primary">', f'<a href="onboard.html?service={service_id}" class="btn-primary">', page)
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(page)

def run():
    with open('roc-annual-compliance-audit.html', 'r', encoding='utf-8') as f:
        template = f.read()
        
    for filename, config in FILES_TO_UNIFY.items():
        if os.path.exists(filename):
            print(f"Unifying {filename}...")
            content = extract_content(filename)
            build_new_page(template, config, content, filename)

run()
