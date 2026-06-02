import os
import re

dir_path = '.'

# 1. Update onboard.html's javascript map
onboard_path = os.path.join(dir_path, 'onboard.html')
with open(onboard_path, 'r', encoding='utf-8') as f:
    onboard_content = f.read()

# Define the comprehensive JS map
comprehensive_map = """  var map={
  gst:['GST Audit & Compliance','25000','https://rzp.io/rzp/c8fadz3e'],
  dpdp:['DPDP Readiness Assessment','40000','https://rzp.io/rzp/kbIHpjU'],
  financial:['Financial Operations Audit','30000','https://rzp.io/rzp/jmJsVf9'],
  it:['IT & Cybersecurity Audit','50000','https://rzp.io/rzp/ffBOb3m'],
  export:['Export Compliance','20000','https://rzp.io/rzp/d6lMSsm'],
  bundle:['Full Audit Bundle','75000','https://rzp.io/rzp/9AMfMA3'],
  vextintel:['VextIntel India Retainer','15000','https://rzp.io/rzp/xFrQp0LS'],
  'vextintel-annual':['VextIntel Annual','150000','https://rzp.io/rzp/f4Njslv'],
  tds:['TDS Compliance Audit','20000','https://rzp.io/rzp/0sb2WvK'],
  roc:['ROC Annual Compliance Audit','18000','https://rzp.io/rzp/93UPUVP8'],
  payroll:['Payroll Compliance Audit','22000','https://rzp.io/rzp/vkOc0Y4U'],
  fema:['FEMA Compliance Audit','25000','https://rzp.io/rzp/vDEsdOBV'],
  msme:['MSME Compliance Health Check','15000','https://rzp.io/rzp/X9O3urP'],
  startup:['Startup India DPIIT Audit','18000','https://rzp.io/rzp/sFNXWkt'],
  'annual-subscription':['Annual Compliance Subscription','60000','https://rzp.io/rzp/xvfP2ffr'],
  amlkyc:['AML / KYC Policy Audit','75964','PENDING'],
  esg:['ESG Baseline Report','56975','PENDING'],
  gdpr:['GDPR Compliance Assessment','75964','PENDING'],
  hipaa:['HIPAA Compliance Assessment','85519','PENDING'],
  iso27001:['Information Security Gap Assessment','114152','PENDING'],
  pcidss:['PCI-DSS Compliance Assessment','95063','PENDING'],
  soc2:['SOC 2 Readiness Assessment','95063','PENDING'],
  transferpricing:['Transfer Pricing Documentation','75000','PENDING'],
  vendor:['Vendor Risk Assessment','47432','PENDING'],
  'vextintel-global':['VextIntel Global Edition','18932','PENDING'],
  incometax:['Income Tax Compliance Audit','30000','PENDING']
  };"""

# Locate old map
map_pattern = r'(\s*)var map=\{\s*gst:\[[\s\S]*?\}\s*;\s*\}'
# Or let's search for var map={ ... }; in a more robust way
pattern_regex = re.compile(r'var map=\{[\s\S]*?\s*};')

if pattern_regex.search(onboard_content):
    onboard_content = pattern_regex.sub(comprehensive_map, onboard_content)
    with open(onboard_path, 'w', encoding='utf-8') as f:
        f.write(onboard_content)
    print("onboard.html JS map updated successfully.")
else:
    print("ERROR: Could not find var map in onboard.html!")

# 2. Update the 4 global service pages
global_pages_info = {
    'ai-business-process-intelligence.html': {
        'link': 'https://rzp.io/rzp/keoObhk2',
        'text': 'Begin Process Intelligence'
    },
    'ai-competitive-intelligence.html': {
        'link': 'https://rzp.io/rzp/DCuZCCJ',
        'text': 'Begin Competitive Intelligence'
    },
    'ai-market-entry-analysis.html': {
        'link': 'https://rzp.io/rzp/rEiI8hlx',
        'text': 'Begin Market Entry Analysis'
    },
    'ai-operational-risk-assessment.html': {
        'link': 'https://rzp.io/rzp/4bCDrHY',
        'text': 'Begin Risk Assessment'
    }
}

for fname, info in global_pages_info.items():
    fpath = os.path.join(dir_path, fname)
    if os.path.exists(fpath):
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Replace href="/#contact" in btn-primary with the direct Razorpay checkout link
        # Look for <a href="/#contact" class="btn-primary">Begin ... </a> or similar
        # Let's do a regex replacement that matches <a href="/#contact" class="btn-primary">
        # and replaces it with <a href="LINK" class="btn-primary" target="_blank">
        # Let's make it robust to also match target="_blank" if it's already there
        btn_pattern = re.compile(r'href="/#contact"(\s+class="btn-primary")')
        new_href = f'href="{info["link"]}"\\1 target="_blank"'
        
        new_content = btn_pattern.sub(new_href, content)
        
        # Let's also check if there is a nav-cta on the page that we want to point to the direct checkout link or keep as /#contact. 
        # Usually nav-cta is "Begin Now" at line 86. Bypassing onboard and going straight to purchase is best for direct checkout.
        # Let's check if we want to replace the nav-cta href too:
        nav_pattern = re.compile(r'href="/#contact"(\s+class="nav-cta")')
        new_nav_href = f'href="{info["link"]}"\\1 target="_blank"'
        new_content = nav_pattern.sub(new_nav_href, new_content)
        
        if new_content != content:
            with open(fpath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"{fname} CTAs successfully updated to Razorpay links.")
        else:
            print(f"WARNING: No CTA changes made in {fname}!")
    else:
        print(f"ERROR: {fname} does not exist!")

print("All updates completed successfully.")
