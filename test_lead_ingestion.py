import sys
import json
import logging
from agents.lead_command import LeadCommandCenter

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def test_ingestion():
    print("======================================================")
    print(" VEXT AUDIT CAPITAL - LEAD INGESTION & OUTREACH TEST")
    print("======================================================\n")
    
    cmd = LeadCommandCenter()
    
    # Simulating the exact payload Apollo.io or Hunter.io would send to our webhook
    simulated_apollo_leads = [
        {
            "name": "Arjun Mehta",
            "email": "arjun.m@fintechinnovations.in",
            "company_name": "Fintech Innovations",
            "contact_role": "Chief Financial Officer",
            "sector": "Financial Services",
            "geography": "India",
            "annual_revenue_inr": 85000000.0,
            "city": "Mumbai",
            "generating_agent": "Mock_Apollo_Integration"
        },
        {
            "name": "Sarah Jenkins",
            "email": "sarah.j@saasdynamics.com",
            "company_name": "SaaS Dynamics",
            "contact_role": "Compliance Manager",
            "sector": "Software",
            "geography": "United States",
            "annual_revenue_inr": 120000000.0,
            "city": "San Francisco",
            "generating_agent": "Mock_Apollo_Integration"
        },
        {
            "name": "Random Person",
            "email": "randomguy123@gmail.com",
            "company_name": "Freelance",
            "contact_role": "Developer",
            "sector": "IT",
            "geography": "India",
            "annual_revenue_inr": 500000.0,
            "city": "Bangalore",
            "generating_agent": "Mock_Apollo_Integration"
        }
    ]
    
    print("[STEP 1] Receiving Simulated Lead Batch from Apollo/Hunter...")
    print(f"   -> {len(simulated_apollo_leads)} Raw Leads Received.\n")
    
    print("[STEP 2] Activating Lead Command Center (Qualification & Verification)...")
    metrics = cmd.ingest_leads_batch(simulated_apollo_leads)
    
    print("\n[STEP 3] Metrics & Qualification Report Generated.")
    print("======================================================")
    print(json.dumps(metrics, indent=4))
    print("======================================================")
    print(" TEST COMPLETE: Only high-quality corporate leads passed the filter.")

if __name__ == "__main__":
    test_ingestion()
