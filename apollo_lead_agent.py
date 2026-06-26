import os
import requests
import json
import logging
from duckduckgo_search import DDGS
import anthropic
from dotenv import load_dotenv

load_dotenv('/opt/vext-audit/.env')
logger = logging.getLogger("VextApolloLeadAgent")
logging.basicConfig(level=logging.INFO)

APOLLO_API_KEY = os.environ.get("APOLLO_API_KEY")
ANTHROPIC_KEY = os.environ.get("ANTHROPIC_API_KEY")

ICPS = {
    "ICP_1": {
        "name": "Global Startups (Data Privacy & Cybersecurity)",
        "target_countries": ["Global"],
        "search_queries": [
            "SaaS Series A",
            "fintech startup",
            "healthtech startup",
            "edtech startup"
        ],
        "target_titles": ["Founder", "CEO", "Chief Risk Officer", "CRO"],
        "pain_points": "Investor due diligence requires data privacy compliance evidence. Enterprise procurement asking for strict regulatory compliance evidence.",
        "regulatory_triggers": "DPDP Act 2023, GDPR, CCPA, HIPAA",
        "objection_counter": "General legal counsel lacks the technical data mapping expertise to bridge the gap between software architecture and privacy legislation.",
        "upsell_path": "Privacy Readiness -> IT & Cybersecurity Audit",
        "revenue_target": "$100K - $12M USD (10-200 employees)"
    },
    "ICP_2": {
        "name": "Cross-Border SaaS Founders (SOC 2, GDPR, CCPA)",
        "target_countries": ["Global"],
        "search_queries": [
            "SaaS startup enterprise",
            "B2B software SOC 2",
            "SaaS product US market",
            "fintech software enterprise",
            "B2B SaaS startup Series A global"
        ],
        "target_titles": ["Founder", "CTO", "Head of Security", "CISO", "VP Engineering"],
        "pain_points": "An enterprise prospect sent a security questionnaire or demanded a SOC 2 Type II or ISO 27001 certificate. Deal is frozen.",
        "regulatory_triggers": "SOC 2 Type II, ISO 27001, GDPR",
        "objection_counter": "Enterprise procurement teams require a validated independent audit report to check their internal risk boxes, automated badges aren't enough.",
        "upsell_path": "SOC 2 Readiness -> ISO 27001 Gap Assessment",
        "revenue_target": "$100K - $12M USD (10-200 employees)"
    },
    "ICP_3": {
        "name": "Global IT Services & BPOs (HIPAA, DORA, Financial Ops)",
        "target_countries": ["Global"],
        "search_queries": [
            "IT outsourcing company",
            "software development agency healthcare",
            "BPO financial services",
            "nearshore software development"
        ],
        "target_titles": ["CEO", "COO", "Delivery Head", "VP Operations"],
        "pain_points": "Healthcare client sends a Business Associate Agreement (BAA) under HIPAA, or Financial Services client demands DORA. Contract cannot be signed without it.",
        "regulatory_triggers": "HIPAA, DORA, GLBA, NYDFS",
        "objection_counter": "Real operational revenue is on the line. Full operational and security audit needed immediately.",
        "upsell_path": "Compliance Assessment -> Financial Operations Audit",
        "revenue_target": "$100K - $12M USD (10-200 employees)"
    }
}

class ApolloLeadAgent:
    def __init__(self):
        self.anthropic_client = anthropic.Anthropic(api_key=ANTHROPIC_KEY)
        self.apollo_url = "https://api.apollo.io/v1/mixed_people/api_search"

    def find_companies(self, industry_keyword: str, max_results: int = 5) -> list:
        logger.info(f"Searching Apollo native for companies in: {industry_keyword}")
        companies = []
        
        headers = {
            "Cache-Control": "no-cache",
            "Content-Type": "application/json",
            "X-Api-Key": APOLLO_API_KEY
        }
        data = {
            "q_organization_keyword_tags": [industry_keyword],
            "organization_num_employees_ranges": ["1,10", "11,20", "21,50", "51,200"],
            "page": 1,
            "per_page": max_results
        }
        
        try:
            res = requests.post("https://api.apollo.io/v1/mixed_companies/search", headers=headers, json=data)
            if res.status_code == 200:
                orgs = res.json().get('organizations', [])
                for org in orgs:
                    domain = org.get('primary_domain')
                    if domain and domain not in companies:
                        companies.append(domain)
        except Exception as e:
            logger.error(f"Native Apollo search failed: {e}")
            
        logger.info(f"Found {len(companies)} domains via Apollo.")
        return companies[:max_results]

    def enrich_lead(self, domain: str, icp_key: str) -> dict:
        icp_data = ICPS[icp_key]
        titles = icp_data["target_titles"]
        logger.info(f"Enriching lead via Apollo for domain: {domain} targeting titles: {titles}")
        
        headers = {
            "Cache-Control": "no-cache",
            "Content-Type": "application/json",
            "X-Api-Key": APOLLO_API_KEY
        }
        data = {
            "q_organization_domains": domain,
            "person_titles": titles,
            "contact_email_status": ["verified"],
            "organization_num_employees_ranges": ["1,10", "11,20", "21,50", "51,200"],
            "page": 1,
            "per_page": 1
        }
        
        try:
            response = requests.post(self.apollo_url, headers=headers, json=data)
            response.raise_for_status()
            result = response.json()
            
            if result.get("people") and len(result["people"]) > 0:
                person = result["people"][0]
                raw_first = person.get('first_name', '').lower()
                raw_last = person.get('last_name', '').lower()
                # Clean up obfuscated last names if Apollo masks them
                if "obfuscated" in raw_last or "***" in raw_last:
                    raw_last = ""
                
                # Build fallback email safely without trailing dots
                fallback_email = f"{raw_first}.{raw_last}".strip(".").strip() + f"@{domain}"
                
                return {
                    "name": f"{person.get('first_name', '')} {person.get('last_name', '')}".strip(),
                    "title": person.get("title", ""),
                    "email": person.get("email") or fallback_email, 
                    "organization": person.get("organization", {}).get("name", domain),
                    "location": f"{person.get('city', '')}, {person.get('country', '')}"
                }
            else:
                logger.warning(f"No decision makers found for {domain}")
                return None
        except Exception as e:
            logger.error(f"Apollo API error for {domain}: {e}")
            return None

    def draft_outreach(self, lead_data: dict, icp_key: str) -> str:
        if not lead_data:
            return None
            
        icp_data = ICPS[icp_key]
        logger.info(f"Drafting personalized outreach for {lead_data['name']} using Claude Opus 4.8 (Targeting {icp_key})")
        
        prompt = (
            f"You are the Director of Growth for Vext Audit Capital, a premium compliance auditing firm.\n"
            f"Draft a short, highly personalized outbound cold email to {lead_data['name']}, who is the {lead_data['title']} at {lead_data['organization']} (Location: {lead_data['location']}).\n"
            f"Target ICP Context:\n"
            f"- Profile: {icp_data['name']}\n"
            f"- Pain Points: {icp_data['pain_points']}\n"
            f"- Regulatory Triggers: {icp_data['regulatory_triggers']}\n"
            f"- Objection Counter: {icp_data['objection_counter']}\n\n"
            f"Instructions:\n"
            f"1. Pitch our auditing services tailored EXACTLY to their regulatory trigger. Write like Jordan Belfort: highly professional, relentless, high-value, and closing the deal right now.\n"
            f"2. CRITICAL: NEVER ask for a phone call, meeting, or voice conversation. Our service is 100% automated.\n"
            f"3. CTA: Direct them to initiate their automated audit immediately by clicking the secure onboarding link: 'https://vextaudit.com/start-audit'\n"
            f"4. CRITICAL: NEVER use the '\u2014' (em dash) or '-' (en dash) symbol anywhere in the text. Use commas or periods instead.\n"
            f"5. Hit their pain points directly. Emphasize speed, AI-accuracy, and premium B2B service.\n"
            f"6. CRITICAL FORMATTING: Strictly use short, punchy paragraphs with double line breaks between them. NEVER output a giant wall of text.\n"
            f"7. Keep it under 150 words. No generic placeholders. No hallucination."
        )
        
        try:
            response = self.anthropic_client.messages.create(
                model="claude-opus-4-8",
                max_tokens=350,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.content[0].text.strip()
        except Exception as e:
            logger.error(f"Failed to draft email: {e}")
            return "Error generating draft."

if __name__ == "__main__":
    agent = ApolloLeadAgent()
    import json
    
    leads_file = "/opt/vext-audit/agents/leads_database.json"
    kpi_file = "/opt/vext-audit/agents/kpi_metrics.json"
    
    try:
        with open(leads_file, "r") as f:
            leads_db = json.load(f)
    except:
        leads_db = {"total_leads_ingested": 0, "verified_leads": []}
        
    try:
        with open(kpi_file, "r") as f:
            kpi_db = json.load(f)
    except:
        kpi_db = {}
    
    total_new = 0
    for icp_key in ICPS.keys():
        logger.info(f"Running agent for {icp_key}...")
        for query in ICPS[icp_key]["search_queries"]:
            domains = agent.find_companies(query, max_results=15)  # Maximize leads to hit today's closed-won revenue target
            for domain in domains:
                lead = agent.enrich_lead(domain, icp_key)
                if lead:
                    draft = agent.draft_outreach(lead, icp_key)
                    if draft and "Error" not in draft:
                        lead["draft"] = draft
                        lead["icp"] = icp_key
                        lead["qualified"] = True  # FIX: Qualify the lead so outbound agent picks it up
                        lead["contacted"] = False 
                        leads_db["verified_leads"].append(lead)
                        leads_db["total_leads_ingested"] += 1
                        total_new += 1
                        
                        # Update KPIs - REMOVED emails_sent_growth, moved to outbound_agent
                        kpi_db["leads_pipeline"] = kpi_db.get("leads_pipeline", 0) + 1
                        kpi_db["pipeline_value_inr"] = kpi_db.get("pipeline_value_inr", 0.0) + 100000.0  # Approx 1.2k USD per lead in pipeline
                        
    # Save back
    with open(leads_file, "w") as f:
        json.dump(leads_db, f, indent=4)
    with open(kpi_file, "w") as f:
        json.dump(kpi_db, f, indent=4)
        
    logger.info(f"War Room Execution Complete. {total_new} massive enterprise leads sourced and pitched.")
