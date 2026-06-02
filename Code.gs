// ============================================================
// VEXT AUDIT CAPITAL — GOOGLE APPS SCRIPT AUTOMATION
// File: Code.gs (Created by Antigravity)
// ============================================================

// ─── CONFIGURATION ──────────────────────────────────────────
const CONFIG = {
  SHEET_ID: '1Xj2RaD-TuP8ieDn8JKhy77alYKYWTM4S3ejnVTL8Q1k',
  SHEETS: {
    CRM: 'CRM Master',
    LOG: 'Automation Log',
    RELATIONSHIPS: 'Relationships',
    RETAINERS: 'Retainers'
  },
  EMAIL: {
    SUPPORT: 'support@vextaudit.com',
    CEO: 'ceo@vextaudit.com',
    NOREPLY: 'noreply@vextaudit.com'
  },
  RAZORPAY: {
    KEY_ID: 'rzp_live_YOUR_KEY_ID',
    WEBHOOK_SECRET: 'aweS7hK5_nrAL7W'
  },
  ANTHROPIC_API_KEY: 'YOUR_ANTHROPIC_API_KEY',
  VAPI_PHONE: 'vextaudit.com/onboard.html',
  WEBSITE: 'https://vextaudit.com',
  APOLLO_API_KEY: 'YOUR_APOLLO_API_KEY',
  APOLLO_SEQUENCE_ID: 'YOUR_APOLLO_SEQUENCE_ID',
  APOLLO_EMAIL_ACCOUNT_ID: 'YOUR_APOLLO_EMAIL_ACCOUNT_ID',
  COL: {
    TIMESTAMP: 1, REF_NO: 2, STATUS: 3, FULL_NAME: 4, DESIGNATION: 5,
    EMAIL: 6, PHONE: 7, COMPANY: 8, COUNTRY: 9, GST_NO: 10,
    INDUSTRY: 11, SOURCE: 12, SERVICE: 13, AMOUNT: 14, PAYMENT: 15,
    PAYMENT_STATUS: 16, PAYMENT_DATE: 17, RAZORPAY_ID: 18,
    ENGAGEMENT_STATUS: 19, ADVISOR: 20, SOW_SENT: 21, SOW_SIGNED: 22,
    DOCS_RECEIVED: 23, WORK_STARTED: 24, DELIVERY_DATE: 25,
    REPORT_SENT: 26, SUPPORT_EXPIRY: 27, BALANCE_DUE: 28,
    BALANCE_PAID: 29, MESSAGE: 30, NOTES: 31
  }
};

// ─── UTILITIES ───────────────────────────────────────────────
function getSheet(name) {
  return SpreadsheetApp.openById(CONFIG.SHEET_ID).getSheetByName(name);
}

function logAction(refNo, clientName, email, agent, action, status, notes) {
  const sheet = getSheet(CONFIG.SHEETS.LOG);
  if (!sheet) return;
  sheet.appendRow([new Date(), refNo, clientName, email, agent, action, status, notes]);
}

function generateRefNo() {
  return 'VAC-' + new Date().getFullYear() + '-' + Math.floor(Math.random() * 90000 + 10000);
}

function callAnthropicAPI(prompt) {
  const url = 'https://api.anthropic.com/v1/messages';
  const payload = {
    model: 'claude-sonnet-4-20250514',
    max_tokens: 1000,
    messages: [{ role: 'user', content: prompt }]
  };
  const options = {
    method: 'post',
    contentType: 'application/json',
    headers: {
      'x-api-key': CONFIG.ANTHROPIC_API_KEY,
      'anthropic-version': '2023-06-01'
    },
    payload: JSON.stringify(payload),
    muteHttpExceptions: true
  };
  try {
    const response = UrlFetchApp.fetch(url, options);
    const data = JSON.parse(response.getContentText());
    return data.content[0].text;
  } catch (e) {
    Logger.log('Anthropic API error: ' + e.message);
    return null;
  }
}

// ─── RAZORPAY WEBHOOK SIGNATURE VERIFICATION ─────────────────
function verifyRazorpaySignature(rawBody, receivedSignature) {
  try {
    if (!receivedSignature) {
      Logger.log('SECURITY: No Razorpay signature header received. Rejecting.');
      return false;
    }
    var secret = CONFIG.RAZORPAY.WEBHOOK_SECRET;
    if (!secret) {
      Logger.log('SECURITY WARNING: WEBHOOK_SECRET not set. Allowing through.');
      return true;
    }
    var computed = Utilities.computeHmacSha256Signature(
      rawBody, secret, Utilities.Charset.UTF_8
    );
    var hexComputed = computed.map(function(b) {
      return ('0' + (b & 0xFF).toString(16)).slice(-2);
    }).join('');
    var isValid = hexComputed === receivedSignature;
    if (!isValid) {
      Logger.log('SECURITY ALERT: Invalid Razorpay signature.');
      Logger.log('Received: ' + receivedSignature);
      Logger.log('Computed: ' + hexComputed);
    }
    return isValid;
  } catch (err) {
    Logger.log('Signature verification error: ' + err.message);
    return false;
  }
}

// ─── WEBHOOK HANDLER ─────────────────────────────────────────
function doPost(e) {
  try {
    var data;
    var rawBody = "";
    
    // Parse incoming payload robustly (handles raw json and url-encoded bodies)
    if (e && e.postData) {
      rawBody = e.postData.contents || "";
      if (e.postData.type === "application/json" || (e.postData.type && e.postData.type.indexOf("text/plain") !== -1)) {
        try {
          data = JSON.parse(rawBody);
        } catch(ex) {
          Logger.log("Failed to parse JSON body: " + ex.message);
        }
      }
    }
    
    if (!data && e && e.parameter) {
      data = e.parameter;
    }
    
    if (!data) {
      Logger.log("No payload data received.");
      return ContentService.createTextOutput("NO_DATA").setMimeType(ContentService.MimeType.TEXT);
    }

    // INTERCEPT WEB3FORMS WEBHOOK FIRST
    var accessKey = data.access_key || (data.data && data.data.access_key) || (data.params && data.params.access_key) || "";
    if (accessKey === "83cc3e63-fbee-43e4-ba81-a074039de80b") {
      return handleWeb3FormsWebhook(data);
    }

    // Razorpay payment webhook
    if (data.event === 'payment.captured') {
      var sig = '';
      try { sig = e.parameter['x-razorpay-signature'] || ''; } catch(ex) { sig = ''; }
      if (!verifyRazorpaySignature(rawBody, sig)) {
        Logger.log('REJECTED: Invalid Razorpay signature.');
        return ContentService.createTextOutput('Unauthorized')
          .setMimeType(ContentService.MimeType.TEXT);
      }
      handlePaymentConfirmed(data.payload.payment.entity);
      return ContentService.createTextOutput('OK');
    }

    // Contact form submission
    if (data.action === 'contactForm' || data.source === 'contact_form' || data.source === 'Website Contact Form') {
      handleContactFormSubmission(data);
      return ContentService.createTextOutput('OK').setMimeType(ContentService.MimeType.TEXT);
    }

    // Onboard intake
    if (data.source === 'onboard_intake') {
      handleOnboardIntake(data);
      return ContentService.createTextOutput('OK').setMimeType(ContentService.MimeType.TEXT);
    }

    // Document upload
    if (data.source === 'document_upload') {
      handleDocumentUpload(data);
      return ContentService.createTextOutput('OK');
    }

    if (data.source === 'document_upload_complete') {
      handleUploadComplete(data);
      return ContentService.createTextOutput('OK');
    }

    return ContentService.createTextOutput('UNHANDLED');

  } catch (err) {
    Logger.log('doPost error: ' + err.message);
    return ContentService.createTextOutput('ERROR: ' + err.message);
  }
}

function doGet(e) {
  const action = e.parameter.action;
  if (action === 'health') return ContentService.createTextOutput('VAC Automation OK');
  return ContentService.createTextOutput('VAC Automation Running');
}

// ============================================================
// AGENT 1 — CONTACT FORM LEAD CAPTURE
// ============================================================
function handleContactFormSubmission(data) {
  const sheet = getSheet(CONFIG.SHEETS.CRM);
  const refNo = generateRefNo();
  const now   = new Date();

  sheet.appendRow([
    now, refNo, 'Lead',
    data.fullName || data.name || '',
    data.designation || '',
    data.email || '',
    data.phone || '',
    data.company || '',
    data.country || 'Unknown',
    data.gst || '',
    data.industry || '',
    data.source || 'Website',
    data.service || '',
    data.amount || '',
    '', 'New', '', '', 'Awaiting Proposal', 'Divya S',
    'No', 'No', 'No', 'No', '', 'No', '', '', '', data.message || '', ''
  ]);

  logAction(refNo, data.fullName || data.name, data.email, 'Agent 1', 'Lead Captured', 'Success', 'Contact form submission');
  qualifyAndRouteLead(refNo, {
    name: data.fullName || data.name,
    email: data.email,
    company: data.company,
    service: data.service,
    message: data.message,
    country: data.country
  });
  sendAutoAcknowledgement(data.fullName || data.name, data.email, data.service);
}

function handleOnboardIntake(data) {
  const sheet    = getSheet(CONFIG.SHEETS.CRM);
  const refNo    = generateRefNo();
  const now      = new Date();
  const existing = sheet.getDataRange().getValues();

  for (var i = 1; i < existing.length; i++) {
    if (existing[i][CONFIG.COL.EMAIL - 1] === data.email &&
        existing[i][CONFIG.COL.SERVICE - 1] === data.svc) {
      Logger.log('Onboard intake: duplicate skipped for ' + data.email);
      return;
    }
  }

  sheet.appendRow([
    now, refNo, 'Lead',
    data.name || '', data.desig || '', data.email || '',
    data.phone || '', data.company || '', data.country || '',
    data.gst || '', data.industry || '',
    data.source || 'Onboard Page',
    data.svc || '', data.amt || '',
    '', 'Pending Payment', '', '', 'Awaiting Payment', 'Divya S',
    'No', 'No', 'No', 'No', '', 'No', '', '', '', data.msg || '', ''
  ]);

  if (data.dpdp_consent === 'yes') storeRelationshipData(refNo, data);

  logAction(refNo, data.name, data.email, 'Agent 1', 'Onboard Intake Captured', 'Success', data.svc);
  sendAutoAcknowledgement(data.name, data.email, data.svc);
}

function storeRelationshipData(refNo, data) {
  try {
    var sheet = getSheet(CONFIG.SHEETS.RELATIONSHIPS);
    if (!sheet) return;
    sheet.appendRow([
      new Date(), refNo, data.name, data.email, data.company,
      data.bday || '', data.anni || '',
      data.spouse || '', data.sbday || '',
      data.father || '', data.fbday || '',
      data.mother || '', data.mbday || '',
      JSON.stringify(data.children || []), 'yes'
    ]);
  } catch (e) {
    Logger.log('Relationship data error: ' + e.message);
  }
}

// ============================================================
// AGENT 2 — PAYMENT CONFIRMED + SOW DELIVERY
// ============================================================
function handlePaymentConfirmed(payment) {
  const sheet   = getSheet(CONFIG.SHEETS.CRM);
  const refNo   = generateRefNo();
  const name    = payment.notes && payment.notes.name    ? payment.notes.name    : '';
  const email   = payment.email   || '';
  const company = payment.notes && payment.notes.company ? payment.notes.company : '';
  const service = payment.notes && payment.notes.service ? payment.notes.service : '';
  const amount  = payment.amount / 100;

  sheet.appendRow([
    new Date(), refNo, 'Client',
    name, '', email, payment.contact || '',
    company, 'India', '', '', 'Razorpay',
    service, amount, payment.method, 'captured',
    new Date(payment.created_at * 1000), payment.id,
    'Awaiting SOW', 'Divya S',
    'No', 'No', 'No', 'No',
    new Date(Date.now() + 7  * 24 * 60 * 60 * 1000), 'No',
    new Date(Date.now() + 37 * 24 * 60 * 60 * 1000),
    '', '', '', ''
  ]);

  sendPaymentConfirmationEmail(name, email, service, amount, payment.id);
  sendCEOPaymentAlert(name, email, company, service, amount, payment.id, payment.method);

  Utilities.sleep(3000);
  var zohoResult = sendSOWForSigning(name, email, service, company);

  if (zohoResult) {
    logAction(refNo, name, email, 'Agent 2', 'SOW Sent via Zoho Sign', 'Success', 'Service: ' + service);
    var rows = sheet.getDataRange().getValues();
    for (var i = 1; i < rows.length; i++) {
      if (rows[i][CONFIG.COL.REF_NO - 1] === refNo) {
        sheet.getRange(i + 1, CONFIG.COL.SOW_SENT).setValue('Yes');
        sheet.getRange(i + 1, CONFIG.COL.ENGAGEMENT_STATUS).setValue('SOW Sent for Signature');
        break;
      }
    }
  } else {
    Logger.log('Zoho Sign failed for ' + email + '. Falling back to plain text SOW.');
    generateAndSendSOW(refNo, name, email, company, service, amount);
    logAction(refNo, name, email, 'Agent 2', 'SOW Sent (fallback)', 'Warning', 'Zoho Sign failed. Plain SOW sent.');
  }

  Utilities.sleep(2000);
  agent7_DocumentCollection(name, email, service);

  logAction(refNo, name, email, 'Agent 2', 'Payment Confirmed + SOW Delivered', 'Success', 'Rs.' + amount + ' | ' + service);
}

// ============================================================
// AGENT 3 — LEAD QUALIFIER + ROUTER
// ============================================================
function agent3_LeadQualifier() {
  const sheet = getSheet(CONFIG.SHEETS.CRM);
  const data  = sheet.getDataRange().getValues();

  for (let i = 1; i < data.length; i++) {
    const row    = data[i];
    const status = row[CONFIG.COL.STATUS - 1];
    const eng    = row[CONFIG.COL.ENGAGEMENT_STATUS - 1];
    const email  = row[CONFIG.COL.EMAIL - 1];

    if (status === 'Lead' && eng === 'Awaiting Proposal' && email) {
      qualifyAndRouteLead(row[CONFIG.COL.REF_NO - 1], {
        name:    row[CONFIG.COL.FULL_NAME - 1],
        email:   email,
        company: row[CONFIG.COL.COMPANY - 1],
        service: row[CONFIG.COL.SERVICE - 1],
        message: row[CONFIG.COL.MESSAGE - 1],
        country: row[CONFIG.COL.COUNTRY - 1]
      });
      sheet.getRange(i + 1, CONFIG.COL.ENGAGEMENT_STATUS).setValue('Qualification Sent');
    }
  }
}

function qualifyAndRouteLead(refNo, data) {
  if (!data.email) return;
  let score = 0;
  const msg     = (data.message || '').toLowerCase();
  const service = (data.service || '').toLowerCase();

  if (msg.includes('urgent') || msg.includes('asap') || msg.includes('notice'))         score += 30;
  if (msg.includes('budget') || msg.includes('ready') || msg.includes('immediately'))   score += 20;
  if (msg.includes('penalty') || msg.includes('audit'))                                  score += 25;
  if (service.includes('bundle') || service.includes('it') || service.includes('dpdp')) score += 15;
  if (['UK','UAE','Singapore','United States','Australia'].includes(data.country))       score += 10;

  if (score >= 40) {
    GmailApp.sendEmail(CONFIG.EMAIL.CEO,
      'HOT LEAD: ' + data.name + ' — ' + data.company + ' — Score: ' + score,
      'HOT LEAD\n\nName: ' + data.name + '\nCompany: ' + data.company +
      '\nEmail: ' + data.email + '\nService: ' + data.service +
      '\nScore: ' + score + '/100\nMessage: ' + data.message +
      '\n\nREPLY WITHIN 30 MINUTES.'
    );
  }
  agent5_GenerateProposal(refNo, data);
}

// ============================================================
// AGENT 4 — SUPPORT TICKET + SLA MONITOR
// ============================================================
function agent4_SupportTicketMonitor() {
  const threads = GmailApp.search(
    'to:support@vextaudit.com is:unread -from:vextaudit.com -from:ceo@vextaudit.com -from:noreply -from:mailer-daemon -from:google',
    0, 20
  );

  threads.forEach(thread => {
    const messages = thread.getMessages();
    const latest   = messages[messages.length - 1];
    if (latest.isUnread()) {
      const ticketId    = 'TKT-' + Date.now();
      const senderEmail = latest.getFrom().match(/<(.+)>/)?.[1] || latest.getFrom();
      const subject     = latest.getSubject();

      GmailApp.sendEmail(senderEmail,
        'Re: ' + subject + ' [' + ticketId + ']',
        'Dear Client,\n\nThank you for reaching out to Vext Audit Capital.\n\n' +
        'Your ticket has been raised: ' + ticketId +
        '\n\nWe will respond within 2 business hours, guaranteed.\n\n' +
        'For urgent matters, visit: https://vextaudit.com/onboard.html\n\n' +
        'Best,\nDivya S\nVext Audit Capital\nsupport@vextaudit.com',
        { from: CONFIG.EMAIL.SUPPORT }
      );

      GmailApp.sendEmail(CONFIG.EMAIL.CEO,
        'New Support Ticket: ' + ticketId + ' — ' + senderEmail,
        'Ticket: ' + ticketId + '\nFrom: ' + senderEmail + '\nSubject: ' + subject +
        '\nSLA: 2 hours from ' + new Date().toLocaleString('en-IN', { timeZone: 'Asia/Kolkata' })
      );

      logAction('', '', senderEmail, 'Agent 4', 'Support Ticket Created', 'Success', ticketId);
      latest.markRead();
    }
  });

  // SLA breach warning at 1h45m
  const oldThreads = GmailApp.search('to:support@vextaudit.com is:read label:inbox', 0, 50);
  oldThreads.forEach(thread => {
    const age = (Date.now() - thread.getLastMessageDate().getTime()) / 60000;
    if (age > 105 && age < 120) {
      GmailApp.sendEmail(CONFIG.EMAIL.CEO,
        'SLA BREACH WARNING — ' + thread.getFirstMessageSubject(),
        'This support email has not been responded to in 1h45m.\nSubject: ' +
        thread.getFirstMessageSubject() + '\n\nRespond immediately to meet 2-hour SLA.'
      );
    }
  });
}

// ============================================================
// AGENT 5 — PROPOSAL GENERATOR
// ============================================================
function agent5_GenerateProposal(refNo, leadData) {
  if (!leadData.email) return;

  const aiProposal = callAnthropicAPI(
    'Generate a professional B2B sales proposal email for Vext Audit Capital. ' +
    'Client: ' + leadData.name + ' at ' + leadData.company + '. ' +
    'Service requested: ' + leadData.service + '. ' +
    'Their message: ' + (leadData.message || 'not provided') + '. ' +
    'Keep it under 200 words. Professional tone. ' +
    'End with: Ready to begin? Visit: https://vextaudit.com/onboard.html - fixed price, 5 business days, no call needed. ' +
    'Sign off as Shyam Sankar, CEO, Vext Audit Capital. Plain text only. No markdown. No phone number.'
  );

  const proposalBody = aiProposal || getDefaultProposalBody(leadData);

  GmailApp.sendEmail(leadData.email,
    'Your Compliance Assessment Proposal — Vext Audit Capital',
    proposalBody,
    { from: CONFIG.EMAIL.SUPPORT, name: 'Divya S | Vext Audit Capital', replyTo: CONFIG.EMAIL.SUPPORT }
  );

  scheduleFollowUps(refNo, leadData);
  logAction(refNo, leadData.name, leadData.email, 'Agent 5', 'Proposal Sent', 'Success', leadData.service);
}

function getDefaultProposalBody(data) {
  return 'Dear ' + (data.name || 'there') + ',\n\nThank you for your interest in Vext Audit Capital.\n\n' +
    'Based on your enquiry about ' + (data.service || 'our compliance services') + ', we are ready to begin immediately.\n\n' +
    'Our AI-powered audit delivers results in 5 business days at a fixed price, no retainer, no surprises.\n\n' +
    'Ready to begin? Visit: https://vextaudit.com/onboard.html - fixed price, 5 business days, no call needed.\n\n' +
    'This proposal is valid for 72 hours.\n\n' +
    'Best regards,\nShyam Sankar\nCEO, Vext Audit Capital\n' + CONFIG.WEBSITE;
}

// ============================================================
// AGENT 6 — FOLLOW-UP SEQUENCE
// ============================================================
function agent6_FollowUpSequence() {
  const sheet = getSheet(CONFIG.SHEETS.CRM);
  const data  = sheet.getDataRange().getValues();
  const now   = Date.now();

  for (let i = 1; i < data.length; i++) {
    const row       = data[i];
    const status    = row[CONFIG.COL.STATUS - 1];
    const email     = row[CONFIG.COL.EMAIL - 1];
    const name      = row[CONFIG.COL.FULL_NAME - 1];
    const engStatus = row[CONFIG.COL.ENGAGEMENT_STATUS - 1];
    const timestamp = row[CONFIG.COL.TIMESTAMP - 1];

    if (!email || status !== 'Lead') continue;

    const ageHours = (now - new Date(timestamp).getTime()) / 3600000;

    if (ageHours >= 24 && ageHours < 25 && engStatus === 'Proposal Sent') {
      sendFollowUpEmail(name, email, 1, row[CONFIG.COL.SERVICE - 1], row[CONFIG.COL.COMPANY - 1]);
      sheet.getRange(i + 1, CONFIG.COL.NOTES).setValue('Follow-up 1 sent: ' + new Date().toISOString());
    }
    if (ageHours >= 48 && ageHours < 49 && engStatus === 'Proposal Sent') {
      sendFollowUpEmail(name, email, 2, row[CONFIG.COL.SERVICE - 1], row[CONFIG.COL.COMPANY - 1]);
      sheet.getRange(i + 1, CONFIG.COL.NOTES).setValue('Follow-up 2 sent: ' + new Date().toISOString());
    }
    if (ageHours >= 72 && ageHours < 73 && engStatus === 'Proposal Sent') {
      sendFollowUpEmail(name, email, 3, row[CONFIG.COL.SERVICE - 1], row[CONFIG.COL.COMPANY - 1]);
      sheet.getRange(i + 1, CONFIG.COL.ENGAGEMENT_STATUS).setValue('Proposal Expired');
    }
  }
}

function sendFollowUpEmail(name, email, followUpNum, service, company) {
  const subjects = [
    'Following up — any questions about your compliance assessment?',
    'Limited availability this week — ' + (company || 'your company'),
    'Final note — your compliance proposal expires today'
  ];
  const bodies = [
    'Hi ' + (name || 'there') + ',\n\nJust checking in on the proposal we sent for ' +
    (service || 'your compliance assessment') + '.\n\nAny questions? Reply to this email and we will respond within 2 hours.\n\n' +
    'Ready to begin? Visit: https://vextaudit.com/onboard.html\n\nBest,\nDivya S | Vext Audit Capital',

    'Hi ' + (name || 'there') + ',\n\nWe have limited audit slots available this week. Your proposal for ' +
    (service || 'compliance assessment') + ' is still reserved.\n\n' +
    'Secure your slot: https://vextaudit.com/onboard.html - fixed price, 5 business days, no call needed.\n\nBest,\nDivya S | Vext Audit Capital',

    'Hi ' + (name || 'there') + ',\n\nThis is our final note. Your compliance assessment proposal expires today.\n\n' +
    'When you are ready: https://vextaudit.com\n\nBest,\nDivya S | Vext Audit Capital'
  ];

  GmailApp.sendEmail(email, subjects[followUpNum - 1], bodies[followUpNum - 1], {
    from: CONFIG.EMAIL.SUPPORT,
    name: 'Divya S | Vext Audit Capital'
  });
}

function scheduleFollowUps(refNo, leadData) {
  const sheet = getSheet(CONFIG.SHEETS.CRM);
  const data  = sheet.getDataRange().getValues();
  for (let i = 1; i < data.length; i++) {
    if (data[i][CONFIG.COL.REF_NO - 1] === refNo) {
      sheet.getRange(i + 1, CONFIG.COL.ENGAGEMENT_STATUS).setValue('Proposal Sent');
      break;
    }
  }
}

// ============================================================
// AGENT 7 — DOCUMENT COLLECTION
// ============================================================
function agent7_DocumentCollection(name, email, service) {
  const docLists = {
    'GST Audit':            ['GST registration certificate', 'Last 12 months GSTR-1 and GSTR-3B', 'Purchase and sales registers', 'Bank statements (last 12 months)', 'ITC claimed summary'],
    'DPDP':                 ['Data flow diagram', 'Privacy policy document', 'Consent collection mechanism details', 'List of data processors and vendors', 'Current IT infrastructure overview'],
    'Financial Operations': ['Last 2 years audited financials', 'Current year management accounts', 'Vendor payment records', 'Expense vouchers (last 6 months)', 'Bank reconciliation statements'],
    'IT & Cybersecurity':   ['Network architecture diagram', 'IT asset inventory', 'Current security policies', 'Last penetration test report if any', 'User access control list'],
    'Export Compliance':    ['IEC certificate', 'Last 12 months export invoices', 'FEMA remittance records', 'Shipping bills and drawback claims', 'DGFT licence copies if applicable']
  };

  let docs = docLists['GST Audit'];
  for (const key of Object.keys(docLists)) {
    if (service && service.toLowerCase().includes(key.toLowerCase())) {
      docs = docLists[key];
      break;
    }
  }

  const docList = docs.map((d, i) => (i + 1) + '. ' + d).join('\n');

  GmailApp.sendEmail(email,
    'Document Checklist — Your Vext Audit Capital Engagement',
    'Dear ' + name + ',\n\nThank you for your payment. To begin your ' + service +
    ', please share the following documents:\n\n' + docList +
    '\n\nPlease email these to ' + CONFIG.EMAIL.SUPPORT + ' or reply to this email.\n\n' +
    'Once received, we begin work immediately. Delivery in 5 business days.\n\n' +
    'Questions? Email us: ' + CONFIG.EMAIL.SUPPORT + '\n\n' +
    'Best,\nDivya S | Vext Audit Capital',
    { from: CONFIG.EMAIL.SUPPORT, name: 'Divya S | Vext Audit Capital' }
  );

  logAction('', name, email, 'Agent 7', 'Document Checklist Sent', 'Success', service);
}

// ============================================================
// AGENT 8 — REPORT DELIVERY
// ============================================================
function agent8_ReportDelivery(name, email, service, reportLink) {
  GmailApp.sendEmail(email,
    'Your ' + service + ' Report is Ready — Vext Audit Capital',
    'Dear ' + name + ',\n\nYour ' + service + ' report has been completed.\n\n' +
    'Your 30-day post-delivery support period begins today.\n\n' +
    '- All clarification queries answered within 2 hours\n' +
    '- Implementation guidance included at no charge\n' +
    '- Direct access to your named advisor\n\n' +
    'Contact us: ' + CONFIG.EMAIL.SUPPORT + '\n\n' +
    'Thank you for trusting Vext Audit Capital.\n\nBest,\nDivya S | Vext Audit Capital\n' + CONFIG.WEBSITE,
    { from: CONFIG.EMAIL.SUPPORT, name: 'Divya S | Vext Audit Capital' }
  );
  logAction('', name, email, 'Agent 8', 'Report Delivered', 'Success', service);
}

// ============================================================
// AGENT 9 — CLIENT ONBOARDING
// ============================================================
function agent9_ClientOnboarding() {
  const sheet = getSheet(CONFIG.SHEETS.CRM);
  const data  = sheet.getDataRange().getValues();

  for (let i = 1; i < data.length; i++) {
    const row       = data[i];
    const status    = row[CONFIG.COL.STATUS - 1];
    const email     = row[CONFIG.COL.EMAIL - 1];
    const name      = row[CONFIG.COL.FULL_NAME - 1];
    const engStatus = row[CONFIG.COL.ENGAGEMENT_STATUS - 1];
    const service   = row[CONFIG.COL.SERVICE - 1];

    if (status === 'Client' && engStatus === 'Awaiting SOW' && email) {
      GmailApp.sendEmail(email,
        'Welcome to Vext Audit Capital — Your Engagement Begins',
        'Dear ' + name + ',\n\nWelcome to Vext Audit Capital. Your engagement is confirmed.\n\n' +
        'Your dedicated advisor is Divya S.\n\nWhat happens next:\n' +
        '1. Statement of Work arrives within 2 hours\n' +
        '2. Document checklist follows immediately\n' +
        '3. Work begins upon document receipt\n' +
        '4. Delivery in 5 business days\n' +
        '5. 30 days post-delivery support included\n\n' +
        'For anything urgent: ' + CONFIG.EMAIL.SUPPORT + '\n\n' +
        'Prudentia · Integritas · Fidelitas\n\nDivya S | Vext Audit Capital',
        { from: CONFIG.EMAIL.SUPPORT, name: 'Divya S | Vext Audit Capital' }
      );

      agent7_DocumentCollection(name, email, service);
      sheet.getRange(i + 1, CONFIG.COL.ENGAGEMENT_STATUS).setValue('Onboarded');
      sheet.getRange(i + 1, CONFIG.COL.ADVISOR).setValue('Divya S');
      logAction(row[CONFIG.COL.REF_NO - 1], name, email, 'Agent 9', 'Client Onboarded', 'Success', service);
    }
  }
}

// ============================================================
// AGENT 10 — RETAINER + RENEWAL MONITOR
// ============================================================
function agent10_RetainerMonitor() {
  const sheet = getSheet(CONFIG.SHEETS.RETAINERS);
  if (!sheet) return;
  const data = sheet.getDataRange().getValues();
  const now  = new Date();

  for (let i = 1; i < data.length; i++) {
    const row           = data[i];
    const email         = row[3];
    const name          = row[2];
    const renewalDate   = new Date(row[10]);
    const daysToRenewal = Math.round((renewalDate - now) / 86400000);
    const plan          = row[7];
    const amount        = row[8];

    if (!email) continue;

    if (daysToRenewal === 7) {
      GmailApp.sendEmail(email,
        'VextIntel Renewal in 7 Days — ' + name,
        'Dear ' + name + ',\n\nYour VextIntel ' + plan + ' retainer renews on ' +
        renewalDate.toDateString() + '.\n\nAmount due: Rs.' + amount +
        '\n\nPayment link: ' + CONFIG.WEBSITE + '/onboard?service=vextintel\n\n' +
        'Questions? Email: ' + CONFIG.EMAIL.SUPPORT + '\n\nBest,\nDivya S | Vext Audit Capital',
        { from: CONFIG.EMAIL.SUPPORT }
      );
    }

    if (daysToRenewal === 0) {
      GmailApp.sendEmail(CONFIG.EMAIL.CEO,
        'Retainer Renewal Due Today: ' + name + ' — Rs.' + amount,
        'Client: ' + name + '\nEmail: ' + email + '\nPlan: ' + plan + '\nAmount: Rs.' + amount
      );
    }
  }
}

// ─── EMAIL HELPERS ────────────────────────────────────────────
function sendAutoAcknowledgement(name, email, service) {
  if (!email) return;
  GmailApp.sendEmail(email,
    'We received your enquiry — Vext Audit Capital',
    'Dear ' + (name || 'there') + ',\n\nThank you for contacting Vext Audit Capital.\n\n' +
    'We have received your enquiry about ' + (service || 'our services') + '.\n\n' +
    'A member of our team will respond within 2 business hours with a detailed proposal.\n\n' +
    'Ready to begin immediately? Visit: https://vextaudit.com/onboard.html - fixed price, 5 business days, no call needed.\n\n' +
    'Best,\nDivya S\nVext Audit Capital\n' + CONFIG.WEBSITE,
    { from: CONFIG.EMAIL.SUPPORT, name: 'Divya S | Vext Audit Capital' }
  );
}

function sendPaymentConfirmationEmail(name, email, service, amount, paymentId) {
  if (!email) return;
  GmailApp.sendEmail(email,
    'Payment Confirmed — Vext Audit Capital Engagement #' + paymentId,
    'Dear ' + name + ',\n\nYour payment of Rs.' + amount + ' for ' + service + ' has been confirmed.\n\n' +
    'Payment ID: ' + paymentId + '\nAmount: Rs.' + amount + '\nStatus: Confirmed\n\n' +
    'What happens next:\n' +
    '1. Statement of Work sent within 60 seconds for e-signature\n' +
    '2. Document checklist follows immediately\n' +
    '3. Work begins upon document receipt\n' +
    '4. Delivery in 5 business days\n\n' +
    'Questions: ' + CONFIG.EMAIL.SUPPORT + '\n\nThank you for trusting Vext Audit Capital.\n\nDivya S | Vext Audit Capital',
    { from: CONFIG.EMAIL.SUPPORT, name: 'Divya S | Vext Audit Capital' }
  );
}

function sendCEOPaymentAlert(name, email, company, service, amount, paymentId, method) {
  GmailApp.sendEmail(CONFIG.EMAIL.CEO,
    'New Payment: ' + name + ' — Rs.' + amount,
    'PAYMENT RECEIVED\n\nClient: ' + name + '\nEmail: ' + email +
    '\nCompany: ' + company + '\nService: ' + service +
    '\nAmount: Rs.' + amount + '\nPayment ID: ' + paymentId +
    '\nMethod: ' + method + '\n\nSOW being sent via Zoho Sign automatically.'
  );
}

function generateAndSendSOW(refNo, name, email, company, service, amount) {
  const sow = callAnthropicAPI(
    'Generate a professional Statement of Work for Vext Audit Capital. ' +
    'Client: ' + name + ' at ' + company + '. Service: ' + service + '. Amount: Rs.' + amount + '. ' +
    'Include: scope, deliverables, timeline (5 business days), payment terms, confidentiality. ' +
    'Under 400 words. Professional tone. No markdown.'
  );

  const sowBody = sow ||
    'Dear ' + name + ',\n\nPlease find your Statement of Work for ' + service + ' below.\n\n' +
    'Engagement fee: Rs.' + amount + '\nDelivery: 5 business days from document receipt\n\n' +
    'To confirm, reply to this email.\n\nBest,\nDivya S | Vext Audit Capital';

  GmailApp.sendEmail(email,
    'Statement of Work — ' + service + ' | Ref: ' + refNo,
    sowBody,
    { from: CONFIG.EMAIL.SUPPORT, name: 'Divya S | Vext Audit Capital', replyTo: CONFIG.EMAIL.SUPPORT }
  );

  logAction(refNo, name, email, 'Agent 2', 'SOW Sent (plain text fallback)', 'Success', service);
}

// ─── DOCUMENT UPLOAD HANDLERS ─────────────────────────────────
function handleDocumentUpload(data) {
  Logger.log('Document upload received: ' + JSON.stringify(data));
}

function handleUploadComplete(data) {
  Logger.log('Upload complete: ' + JSON.stringify(data));
  if (data.email) {
    GmailApp.sendEmail(CONFIG.EMAIL.CEO,
      'Documents Received: ' + data.email,
      'Client documents uploaded.\nEmail: ' + data.email + '\nFiles: ' + (data.files || 'unknown')
    );
  }
}

// ============================================================
// MASTER TRIGGER SETUP
// Run this ONCE after deploying all files.
// Covers Code.gs agents + all 4 new lead gen agents.
// ============================================================
function setupAllTriggers() {
  // Delete ALL existing triggers cleanly
  ScriptApp.getProjectTriggers().forEach(t => ScriptApp.deleteTrigger(t));

  // ── Core automation agents ──
  ScriptApp.newTrigger('agent3_LeadQualifier')
    .timeBased().everyMinutes(5).create();

  ScriptApp.newTrigger('agent4_SupportTicketMonitor')
    .timeBased().everyMinutes(15).create();

  ScriptApp.newTrigger('agent6_FollowUpSequence')
    .timeBased().everyHours(6).create();

  ScriptApp.newTrigger('agent9_ClientOnboarding')
    .timeBased().everyMinutes(10).create();

  ScriptApp.newTrigger('agent10_RetainerMonitor')
    .timeBased().atHour(9).everyDays(1).inTimezone('Asia/Kolkata').create();

  // ── Lead gen agents - 6 keys, staggered 30 min apart ──
  // PG1: 8:00 AM IST = 2:30 AM UTC
  ScriptApp.newTrigger('runPureGoogleAgent').timeBased().everyDays(1).atHour(2).create();
  // PG2: 8:30 AM IST = 3:00 AM UTC
  ScriptApp.newTrigger('runPureGoogle2').timeBased().everyDays(1).atHour(3).create();
  // PG3: 9:00 AM IST = 3:30 AM UTC
  ScriptApp.newTrigger('runPureGoogle3').timeBased().everyDays(1).atHour(3).create();
  // PG4: 9:30 AM IST = 4:00 AM UTC
  ScriptApp.newTrigger('runPureGoogle4').timeBased().everyDays(1).atHour(4).create();
  // PG5: 10:00 AM IST = 4:30 AM UTC
  ScriptApp.newTrigger('runPureGoogle5').timeBased().everyDays(1).atHour(4).create();
  // PG6: 10:30 AM IST = 5:00 AM UTC
  ScriptApp.newTrigger('runPureGoogle6').timeBased().everyDays(1).atHour(5).create();

  // ── DirectOutreach: 9:00 AM IST = 3:30 AM UTC ──
  ScriptApp.newTrigger('sendDirectOutreach').timeBased().everyDays(1).atHour(4).create();

  // ── CEO Agent: every 6 hours ──
  ScriptApp.newTrigger('runCEOAgent').timeBased().everyHours(6).create();

  Logger.log('ALL TRIGGERS SET:');
  Logger.log('Every 5 min  - Lead Qualifier');
  Logger.log('Every 15 min - Support Ticket Monitor');
  Logger.log('Every 6 hrs  - Follow-up Sequence');
  Logger.log('Every 6 hrs  - CEO Briefing Agent');
  Logger.log('Every 10 min - Client Onboarding');
  Logger.log('09:00 IST    - Retainer Monitor');
  Logger.log('08:00 IST    - PG1 General ICP');
  Logger.log('08:30 IST    - PG2 Funded Startups DPDP');
  Logger.log('09:00 IST    - PG3 Export Manufacturers');
  Logger.log('09:30 IST    - PG4 IT/SaaS Bangalore');
  Logger.log('10:00 IST    - PG5 Global Indian Companies');
  Logger.log('10:30 IST    - PG6 MSME Manufacturing');
  Logger.log('09:30 IST    - DirectOutreach Email Sends');

  try {
    GmailApp.sendEmail(CONFIG.EMAIL.CEO,
      '[VAC] All automation triggers armed',
      'All triggers set and running.\n\nLead gen: 08:30, 09:30, 10:30 IST daily\nOutreach: 09:30 IST daily\nCore agents: running continuously\n\nSystem is live.',
      {name: 'VAC Automation'}
    );
  } catch(e) {}
}

// ─── HEALTH CHECK ─────────────────────────────────────────────
function healthCheck() {
  Logger.log('VAC Automation Health Check');
  Logger.log('Sheet ID: '           + CONFIG.SHEET_ID);
  Logger.log('CRM sheet: '          + (getSheet(CONFIG.SHEETS.CRM)  ? 'OK' : 'NOT FOUND'));
  Logger.log('Log sheet: '          + (getSheet(CONFIG.SHEETS.LOG)  ? 'OK' : 'NOT FOUND'));
  Logger.log('Webhook secret set: ' + (CONFIG.RAZORPAY.WEBHOOK_SECRET ? 'YES' : 'NO'));
  Logger.log('Anthropic key set: '  + (CONFIG.ANTHROPIC_API_KEY ? 'YES' : 'NO'));
  Logger.log('Apollo key set: '     + (CONFIG.APOLLO_API_KEY ? 'YES' : 'NO'));
  Logger.log('Health check complete.');
}
