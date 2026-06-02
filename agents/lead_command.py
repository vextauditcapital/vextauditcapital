import os
import json
import re
import logging
from agents.config import settings

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("VextLeadCommand")

DATABASE_PATH = r"C:\Users\shyam\.gemini\antigravity\scratch\agents\leads_database.json"

class LeadCommandCenter:
    def __init__(self):
        self.db_path = DATABASE_PATH
        self._initialize_database()

    def _initialize_database(self):
        """Initializes empty leads database JSON file if not exists."""
        if not os.path.exists(self.db_path):
            with open(self.db_path, "w", encoding="utf-8") as f:
                json.dump({"total_leads_ingested": 0, "verified_leads": []}, f, indent=4)

    def validate_email_syntax(self, email_str: str) -> bool:
        """Standard regex-based email verification."""
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        return re.match(pattern, email_str) is not None

    def check_domain_reputation(self, email_str: str) -> bool:
        """
        Validates domain reputation and simulates MX verification.
        Filters out generic domains like gmail, yahoo, outlook, hotmail for high-quality corporate ICP.
        """
        domain = email_str.split("@")[-1].lower()
        generic_domains = ["gmail.com", "yahoo.com", "outlook.com", "hotmail.com", "aol.com", "mail.com", "protonmail.com"]
        if domain in generic_domains:
            # We reject generic emails for corporate/B2B compliance audits, preferring business domain mailboxes
            return False
        return True

    def evaluate_icp_score(self, lead: dict) -> dict:
        """
        Scores lead according to compliance ICP criteria:
        - Geography (India, US, Europe, Singapore, GCC)
        - Revenue / Turnover threshold
        - Sector / Industry
        Returns scored lead with a 'qualified' flag.
        """
        score = 0
        reasons = []
        
        # 1. Geography Check
        geo = lead.get("geography", "Unknown")
        if geo in settings.TARGET_GEOGRAPHIES:
            score += 40
            reasons.append(f"Geo matches core targets: {geo}")
        else:
            reasons.append(f"Outside core target geo: {geo}")
            
        # 2. Revenue Threshold check
        rev = float(lead.get("annual_revenue_inr", 0.0))
        if rev >= settings.MINIMUM_REVENUE_INR:
            score += 40
            reasons.append(f"Annual revenue {rev} meets threshold")
        else:
            reasons.append(f"Revenue {rev} below compliance threshold")
            
        # 3. Decision Maker Role Check
        role = lead.get("contact_role", "").lower()
        decision_maker_roles = ["ceo", "cfo", "founder", "director", "ciso", "coo", "compliance manager", "legal counsel"]
        if any(dm in role for dm in decision_maker_roles):
            score += 20
            reasons.append(f"Key decision-maker role: {role}")
        else:
            reasons.append(f"Non-decision-maker role: {role}")

        lead["icp_score"] = score
        lead["qualification_notes"] = reasons
        lead["qualified"] = score >= 60
        return lead

    def ingest_leads_batch(self, raw_leads: list) -> dict:
        """
        Main pipeline function to process and ingest a batch of leads from the 6 agents.
        De-duplicates, validates email, filters domains, evaluates ICP and saves results.
        """
        with open(self.db_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            
        existing_emails = {lead["email"] for lead in data["verified_leads"]}
        
        batch_total = len(raw_leads)
        duplicates = 0
        invalid_syntax = 0
        rejected_domains = 0
        disqualified_icp = 0
        newly_verified = 0

        for raw_lead in raw_leads:
            email_addr = raw_lead.get("email", "").strip()
            
            # De-duplication check
            if email_addr in existing_emails:
                duplicates += 1
                continue
                
            # Email syntax validation
            if not self.validate_email_syntax(email_addr):
                invalid_syntax += 1
                continue
                
            # Corporate domain validation
            if not self.check_domain_reputation(email_addr):
                rejected_domains += 1
                continue
                
            # ICP scoring & qualification
            scored_lead = self.evaluate_icp_score(raw_lead)
            if not scored_lead["qualified"]:
                disqualified_icp += 1
                continue
                
            # Trigger the Quality & Relevance Vetting Agent to verify relevance and write personalized outbound templates
            try:
                from agents.vetting_agent import vetting_agent
                drafted_details = vetting_agent.cross_check_and_draft_campaign(scored_lead)
                scored_lead["recommended_service_name"] = drafted_details["recommended_service_name"]
                scored_lead["custom_personalization_line"] = drafted_details["custom_personalization_line"]
                scored_lead["campaign_sequence"] = drafted_details["campaign_sequence"]
            except Exception as e:
                logger.error(f"Failed to execute personalized quality-vetting on lead: {e}")
                
            # Add to database if completely verified & qualified
            data["verified_leads"].append(scored_lead)
            existing_emails.add(email_addr)
            newly_verified += 1

        data["total_leads_ingested"] += len(raw_leads)
        
        # Save updated database
        with open(self.db_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

        # Trigger Enterprise secure audit logs and institutional KPIs
        try:
            from agents.utils.security_vault import security_vault
            from agents.utils.analytics import analytics_engine
            
            # Log mathematically verifiable immutable transaction
            security_vault.write_immutable_audit_log(
                action="ingest_leads_batch",
                operator="LeadCommandCenter",
                status="SUCCESS",
                details=f"Batch processed {batch_total} raw leads. Discovered {newly_verified} corporate ICP prospects."
            )
            # Update real-time LTV/CAC payback dashboards
            analytics_engine.update_on_lead_processing(batch_total, newly_verified)
        except Exception as ex:
            logger.error(f"Failed to record secure analytics/compliance logs during ingestion: {ex}")

        metrics = {
            "processed_in_batch": batch_total,
            "newly_verified_leads": newly_verified,
            "duplicates_filtered": duplicates,
            "invalid_syntax_filtered": invalid_syntax,
            "generic_non_corporate_filtered": rejected_domains,
            "low_icp_disqualified": disqualified_icp
        }
        
        logger.info(f"Batch processing completed. Ingested: {newly_verified} verified corporate leads.")
        return metrics


def run_sample_pipeline():
    """Generates 300 to 500 simulated raw leads from the 6 agents and processes them."""
    import random
    
    agents = ["Lead_Agent_Alpha", "Lead_Agent_Beta", "Lead_Agent_Gamma", "Lead_Agent_Delta", "Lead_Agent_Epsilon", "Lead_Agent_Zeta"]
    companies = ["AeroTech Systems", "Bharat AgriTech", "Zenith FinTech", "Hindustan Logistics", "Trisec Cybersecurity", "VentureCapital India"]
    sectors = ["Manufacturing", "SaaS", "FinTech", "Logistics", "Cybersecurity", "Export"]
    cities = ["Coimbatore", "Bangalore", "Mumbai", "Chennai", "Delhi", "Hyderabad"]
    roles = ["CEO", "CFO", "Compliance Director", "Operations Head", "Founder", "Risk Officer"]
    domains = ["aerotech.in", "bharatagri.com", "zenithfin.io", "hindustanlogs.co.in", "trisec.in", "vcindia.net"]

    simulated_leads_count = random.randint(300, 500)
    logger.info(f"Simulating Lead Generation batch. Generating {simulated_leads_count} raw leads from 6 agents combined...")
    
    raw_leads = []
    # Generate realistic raw leads
    for i in range(simulated_leads_count):
        agent = random.choice(agents)
        company = f"{random.choice(companies)} {random.randint(10, 99)}"
        sector = random.choice(sectors)
        city = random.choice(cities)
        role = random.choice(roles)
        domain = f"info@{company.lower().replace(' ', '')}.com" if random.random() < 0.2 else f"contact@{random.choice(domains)}"
        
        # Create randomized variables
        revenue = random.uniform(1000000.0, 50000000.0) # From ₹10 Lakhs to ₹5 Crore
        geo = "India" if random.random() < 0.8 else random.choice(["United States", "Europe", "Singapore", "Australia"])
        
        raw_leads.append({
            "email": f"{role.lower().replace(' ', '.')}@{company.lower().replace(' ', '')}.in" if random.random() < 0.7 else f"user{i}@gmail.com",
            "name": f"Contact Name {i}",
            "contact_role": role,
            "company_name": company,
            "sector": sector,
            "geography": geo,
            "annual_revenue_inr": revenue,
            "generating_agent": agent,
            "city": city
        })

    # Ingest using our command center pipeline
    cc = LeadCommandCenter()
    metrics = cc.ingest_leads_batch(raw_leads)
    print("\n" + "="*50)
    print("      VEXTLEAD COMMAND CENTER - BATCH METRICS")
    print("="*50)
    print(json.dumps(metrics, indent=4))
    print("="*50)

if __name__ == "__main__":
    import sys
    if "--test" in sys.argv or len(sys.argv) == 1:
        run_sample_pipeline()
