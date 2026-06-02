with open("index.html", "r", encoding="utf-8") as f:
    content = f.read()

# Replace the first "How We Work" steps (lines 432-458)
target_steps = """  <div class="process-steps">
    <div class="step fade-up">
      <div class="step-circle">I</div>
      <div class="step-title">Select</div>
      <div class="step-desc">Choose your service at vextaudit.com/onboard.html. Fixed price shown upfront.</div>
    </div>
    <div class="step fade-up fade-up-delay-1">
      <div class="step-circle">II</div>
      <div class="step-title">Pay</div>
      <div class="step-desc">Secure payment via Razorpay. SOW sent to your email within 60 seconds.</div>
    </div>
    <div class="step fade-up fade-up-delay-2">
      <div class="step-circle">III</div>
      <div class="step-title">Submit</div>
      <div class="step-desc">Upload your documents. Our AI pipeline and specialists begin work immediately.</div>
    </div>
    <div class="step fade-up fade-up-delay-3">
      <div class="step-circle">IV</div>
      <div class="step-title">Report</div>
      <div class="step-desc">Plain-language findings with priority-ranked action items in 5 business days.</div>
    </div>
    <div class="step fade-up fade-up-delay-4">
      <div class="step-circle">V</div>
      <div class="step-title">Support</div>
      <div class="step-desc">30-day post-engagement support included. Remediation queries at no charge.</div>
    </div>
  </div>"""

replacement_steps = """  <div class="process-steps">
    <div class="step fade-up">
      <div class="step-circle">I</div>
      <div class="step-title">Intake &amp; Pay</div>
      <div class="step-desc">Select your service on onboard.html, fill your details, and complete secure payment via Razorpay.</div>
    </div>
    <div class="step fade-up fade-up-delay-1">
      <div class="step-circle">II</div>
      <div class="step-title">Welcome &amp; Receipt</div>
      <div class="step-desc">Receive your advisor's welcome letter and secure transaction receipt instantly in your inbox.</div>
    </div>
    <div class="step fade-up fade-up-delay-2">
      <div class="step-circle">III</div>
      <div class="step-title">Tax Invoice</div>
      <div class="step-desc">Get a legally compliant B2B tax invoice featuring our corporate logo and GSTIN for your records.</div>
    </div>
    <div class="step fade-up fade-up-delay-3">
      <div class="step-circle">IV</div>
      <div class="step-title">Zoho Sign SOW</div>
      <div class="step-desc">Review and sign your digital Statement of Work (SOW) sent via Zoho Sign to define project scope.</div>
    </div>
    <div class="step fade-up fade-up-delay-4">
      <div class="step-circle">V</div>
      <div class="step-title">Commencement</div>
      <div class="step-desc">Document collection and our expert-backed AI compliance audit begin immediately after SOW signature.</div>
    </div>
  </div>"""

if target_steps in content:
    content = content.replace(target_steps, replacement_steps)
    print("First 'How We Work' block replaced successfully!")
else:
    print("WARNING: First 'How We Work' block target NOT found! Let's check why.")

# Replace the second "How It Works" block (lines 583-602)
target_how_it_works = """        <div style="font-family:var(--ff-display);font-size:11px;letter-spacing:0.22em;text-transform:uppercase;color:var(--gold);opacity:0.6;margin-bottom:20px;">How It Works</div>
        <div style="display:flex;flex-direction:column;gap:18px;">
          <div style="display:flex;gap:16px;align-items:flex-start;">
            <div style="font-family:var(--ff-display);font-size:18px;color:var(--gold);opacity:0.4;min-width:28px;line-height:1.2;">01</div>
            <div style="font-family:var(--ff-body);font-size:16px;color:var(--cream);opacity:0.72;line-height:1.7;">Select your service and complete payment at <a href="/onboard" style="color:var(--gold);text-decoration:none;">vextaudit.com/onboard.html</a></div>
          </div>
          <div style="display:flex;gap:16px;align-items:flex-start;">
            <div style="font-family:var(--ff-display);font-size:18px;color:var(--gold);opacity:0.4;min-width:28px;line-height:1.2;">02</div>
            <div style="font-family:var(--ff-body);font-size:16px;color:var(--cream);opacity:0.72;line-height:1.7;">Statement of Work sent to your email within 60 seconds automatically.</div>
          </div>
          <div style="display:flex;gap:16px;align-items:flex-start;">
            <div style="font-family:var(--ff-display);font-size:18px;color:var(--gold);opacity:0.4;min-width:28px;line-height:1.2;">03</div>
            <div style="font-family:var(--ff-body);font-size:16px;color:var(--cream);opacity:0.72;line-height:1.7;">Upload documents. Work begins immediately. Report in 5 business days.</div>
          </div>
          <div style="display:flex;gap:16px;align-items:flex-start;">
            <div style="font-family:var(--ff-display);font-size:18px;color:var(--gold);opacity:0.4;min-width:28px;line-height:1.2;">04</div>
            <div style="font-family:var(--ff-body);font-size:16px;color:var(--cream);opacity:0.72;line-height:1.7;">30 days of free post-delivery support. Your advisor reachable at any time.</div>
          </div>
        </div>"""

replacement_how_it_works = """        <div style="font-family:var(--ff-display);font-size:11px;letter-spacing:0.22em;text-transform:uppercase;color:var(--gold);opacity:0.6;margin-bottom:20px;">How It Works</div>
        <div style="display:flex;flex-direction:column;gap:18px;">
          <div style="display:flex;gap:16px;align-items:flex-start;">
            <div style="font-family:var(--ff-display);font-size:18px;color:var(--gold);opacity:0.4;min-width:28px;line-height:1.2;">01</div>
            <div style="font-family:var(--ff-body);font-size:16px;color:var(--cream);opacity:0.72;line-height:1.7;">Select your service and complete secure intake details at <a href="/onboard" style="color:var(--gold);text-decoration:none;">vextaudit.com/onboard.html</a>.</div>
          </div>
          <div style="display:flex;gap:16px;align-items:flex-start;">
            <div style="font-family:var(--ff-display);font-size:18px;color:var(--gold);opacity:0.4;min-width:28px;line-height:1.2;">02</div>
            <div style="font-family:var(--ff-body);font-size:16px;color:var(--cream);opacity:0.72;line-height:1.7;">Advisor's welcome letter and payment transaction confirmation receipt sent instantly.</div>
          </div>
          <div style="display:flex;gap:16px;align-items:flex-start;">
            <div style="font-family:var(--ff-display);font-size:18px;color:var(--gold);opacity:0.4;min-width:28px;line-height:1.2;">03</div>
            <div style="font-family:var(--ff-body);font-size:16px;color:var(--cream);opacity:0.72;line-height:1.7;">Legally compliant B2B tax invoice featuring corporate logo and GSTIN delivered.</div>
          </div>
          <div style="display:flex;gap:16px;align-items:flex-start;">
            <div style="font-family:var(--ff-display);font-size:18px;color:var(--gold);opacity:0.4;min-width:28px;line-height:1.2;">04</div>
            <div style="font-family:var(--ff-body);font-size:16px;color:var(--cream);opacity:0.72;line-height:1.7;">Statement of Work (SOW) sent via Zoho Sign for digital signature and execution.</div>
          </div>
          <div style="display:flex;gap:16px;align-items:flex-start;">
            <div style="font-family:var(--ff-display);font-size:18px;color:var(--gold);opacity:0.4;min-width:28px;line-height:1.2;">05</div>
            <div style="font-family:var(--ff-body);font-size:16px;color:var(--cream);opacity:0.72;line-height:1.7;">Process commencement and expert-backed AI compliance diagnostics begin <strong>only after</strong> SOW signature is secured.</div>
          </div>
        </div>"""

if target_how_it_works in content:
    content = content.replace(target_how_it_works, replacement_how_it_works)
    print("Second 'How It Works' block replaced successfully!")
else:
    print("WARNING: Second 'How It Works' block target NOT found!")

with open("index.html", "w", encoding="utf-8") as f:
    f.write(content)
