import logging
import json
from pydantic import BaseModel, Field
from agents.config import settings
from agents.utils.gemini_client import gemini_client

logger = logging.getLogger("VextVettingAgent")

# Outbound Cold Outreach Sequence Templates Registry
OUTBOUND_TEMPLATES = {
    "initial": (
        "Subject: Mapped Compliance Gaps for {company_name} - Vext Audit Capital\n\n"
        "Hi {contact_first_name},\n\n"
        "{custom_personalization_line}\n\n"
        "At Vext Audit Capital, we have pioneered the first 100% automated AI-based Audit Compliance platform. "
        "We mapped your industry profile against global and domestic regulatory requirements and identified that the "
        "\"{recommended_service_name}\" is currently a critical prerequisite for your business operations.\n\n"
        "By leveraging automated algorithms instead of traditional hourly consulting firms, we complete your "
        "entire regulatory audit in 3-5 days at a fixed, flat fee of {service_price}.\n\n"
        "Would you be open to a brief thread reply or reviewing your onboarding path at `/onboard?service={recommended_service_code}` to address these requirements?\n\n"
        "Best regards,\n\n"
        "AI Operations Director\n"
        "Vext Audit Capital\n"
        "vextaudit.com"
    ),
    "followup_1": (
        "Subject: Re: Mapped Compliance Gaps for {company_name}\n\n"
        "Hi {contact_first_name},\n\n"
        "Following up on my previous message regarding your \"{recommended_service_name}\" gap analysis. "
        "I wanted to share that we maintain complete pricing transparency on our platform-there are zero hourly billing rates or hidden fees. "
        "The flat rate for your firm's compliance is exactly {service_price}.\n\n"
        "Our AI engine is ready to ingest and parse your financial ledgers instantly at `/upload` once the checkout is initiated.\n\n"
        "You can view your pre-mapped checkout link and start onboarding instantly here: `/onboard?service={recommended_service_code}`\n\n"
        "Do you have any questions on this?\n\n"
        "Best regards,\n\n"
        "AI Operations Director\n"
        "Vext Audit Capital"
    ),
    "followup_2": (
        "Subject: Operational Checklist: \"{recommended_service_name}\" for {company_name}\n\n"
        "Hi {contact_first_name},\n\n"
        "To save you time, I had our AI parser generate a quick 3-point checklist of what is required to pass your next audit successfully:\n\n"
        "1. Active ledger consistency checks and automated matching.\n"
        "2. Comprehensive statutory reporting mapping under the latest regulatory thresholds.\n"
        "3. Secure, encrypted storage verification for privacy and operational auditing.\n"
        "\n"
        "Our automated engine executes all these checks within hours. You can initiate the process in under 2 minutes at `/onboard?service={recommended_service_code}`.\n\n"
        "Should we initiate the Statement of Work (SOW) draft for your review?\n\n"
        "Best regards,\n\n"
        "AI Operations Director\n"
        "Vext Audit Capital"
    ),
    "followup_3": (
        "Subject: Closing your compliance file - {company_name}\n\n"
        "Hi {contact_first_name},\n\n"
        "I haven't heard back regarding the \"{recommended_service_name}\" gaps we mapped for {company_name}. "
        "I assume that audit compliance is either handled or not a primary focus for this quarter.\n\n"
        "I will go ahead and close your temporary file in our system to keep our pipeline organized. "
        "If you ever need fast, 100% automated AI audit mapping in the future, you can always visit us directly at vextaudit.com.\n\n"
        "Thank you for your time, and I wish you continued growth.\n\n"
        "Best regards,\n\n"
        "AI Operations Director\n"
        "Vext Audit Capital"
    )
}

# Pricing map for recommended services to merge into templates
SERVICE_PRICE_MAP = {
    "gst": ("GST Audit & Compliance", "₹25,000", "gst-audit-compliance"),
    "dpdp": ("DPDP Readiness Assessment", "₹40,000", "dpdp-readiness-assessment"),
    "financial": ("Financial Operations Audit", "₹30,000", "financial-operations-audit"),
    "it": ("IT & Cybersecurity Audit", "₹50,000", "it-cybersecurity-audit"),
    "export": ("Export Compliance", "₹20,000", "export-compliance"),
    "vextintel": ("VextIntel Monthly Retainer", "₹15,000/month", "vextintel-monthly-retainer"),
    "fema": ("FEMA Compliance Audit", "₹25,000", "fema-compliance-audit"),
    "payroll": ("Payroll Compliance Audit", "₹22,000", "payroll-compliance-audit"),
    "dpiit": ("Startup DPIIT Audit", "₹18,000", "startup-dpiit-compliance-audit"),
    "soc2": ("SOC 2 Readiness Assessment", "₹20,848", "soc2-readiness-assessment")
}

class VextVettingAgent:
    """
    Dedicated AI Quality & Relevance Agent (VextVetter Agent).
    Cross-checks every lead to determine relevance of Vext Audit Capital's services and drafts hyper-personalized outbound sequences.
    """
    def __init__(self):
        # Vetting Agent System Instructions for Gemini
        self.system_prompt = (
            "You are the autonomous AI Vetting & Personalization Agent of Vext Audit Capital.\n"
            "Your job is to read metadata about a target prospect's company (name, sector, estimated revenue, country, role) "
            "and cross-check the extreme relevance of our compliance services to them.\n\n"
            "Core Operations:\n"
            "1. Select the single most relevant service from: [GST, DPDP, Financial, IT/Cybersecurity, Export/FEMA, Startup DPIIT, SOC 2, Payroll].\n"
            "2. Formulate a hyper-personalized, ultra-specific opening sentence (custom_personalization_line) that PROVES you understand their business context. "
            "Focus on active business updates, regulatory pain points, or geographic relevance. "
            "Ensure the sentence is brief, strictly professional, and completely logical. Avoid fluff or generic templates like 'I hope this email finds you well'.\n"
            "3. Return the response in clean JSON format matching the keys: 'recommended_service_key' (lowercase shortcode) and 'custom_personalization_line'."
        )

    def cross_check_and_draft_campaign(self, lead: dict) -> dict:
        """
        Cross-checks the relevance of Vext Audit Capital services to the client's company,
        generates personalized context using Gemini 3.5 Flash, and prepares the 4-part email sequence.
        """
        lead_info_str = (
            f"Company: {lead.get('company_name')}\n"
            f"Sector/Industry: {lead.get('sector')}\n"
            f"Geography: {lead.get('geography')}\n"
            f"Annual Revenue (INR): {lead.get('annual_revenue_inr')}\n"
            f"Contact Role: {lead.get('contact_role')}\n"
            f"City: {lead.get('city', 'India')}"
        )
        
        # Call Gemini Client to get recommendation & custom personalization opening sentence
        try:
            raw_response = gemini_client.generate_response(
                role="support", # maps to support helper
                context=self.system_prompt,
                user_message=lead_info_str
            )
            
            # Clean JSON markdown blocks if Gemini wrapped it
            raw_response = raw_response.replace("```json", "").replace("```", "").strip()
            parsed = json.loads(raw_response)
            
            svc_key = parsed.get("recommended_service_key", "gst").lower()
            personalization = parsed.get("custom_personalization_line", "")
        except Exception as e:
            # Fallback heuristic mapping if API fails to maintain 100% uptime
            logger.warning(f"Gemini vetting failed, falling back to heuristics: {e}")
            sector = lead.get("sector", "").lower()
            geo = lead.get("geography", "").lower()
            company_name = lead.get("company_name", "")
            
            if "saas" in sector or "tech" in sector:
                svc_key = "dpdp" if geo == "india" else "soc2"
                personalization = f"I noticed that {company_name} operates in the software/tech space, which means aligning with the latest data privacy directives like the DPDP Act of India is a critical operational priority this quarter."
            elif "export" in sector or "trade" in sector:
                svc_key = "export"
                personalization = f"Since {company_name} drives active cross-border transactions, keeping your foreign remittance and export incentive documentations aligned with RBI's FEMA directives is highly important."
            else:
                svc_key = "gst"
                personalization = f"I noticed your active corporate operations at {company_name}. Ensuring that your monthly GST filings and ledger synchronizations are fully audited is essential under the latest tax guidelines."
                
        # Resolve the recommended service details
        svc_details = SERVICE_PRICE_MAP.get(svc_key, SERVICE_PRICE_MAP["gst"])
        svc_name, svc_price, svc_code = svc_details
        
        first_name = lead.get("name", "there").split()[0]
        
        # Merge values into the 4 email sequences
        sequence = {}
        for campaign_step, template in OUTBOUND_TEMPLATES.items():
            sequence[campaign_step] = template.format(
                company_name=lead.get("company_name"),
                contact_first_name=first_name,
                custom_personalization_line=personalization,
                recommended_service_name=svc_name,
                recommended_service_code=svc_code,
                service_price=svc_price
            )
            
        return {
            "lead_email": lead.get("email"),
            "recommended_service_key": svc_key,
            "recommended_service_name": svc_name,
            "custom_personalization_line": personalization,
            "campaign_sequence": sequence
        }

# Instantiate shared vetting agent
vetting_agent = VextVettingAgent()
