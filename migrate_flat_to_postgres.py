import os
import json
import logging
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine, Base
from app import models

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("vext-migration")

def run_migration():
    """
    Migrates lead data from the flat-file JSON leads_database.json (7MB)
    into the secure, relational PostgreSQL / SQLite database.
    """
    json_path = r"C:\Users\shyam\.gemini\antigravity\scratch\agents\leads_database.json"
    if not os.path.exists(json_path):
        logger.error(f"Flat database file not found at {json_path}")
        return
        
    logger.info("Connecting to database...")
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    
    logger.info("Loading leads_database.json...")
    with open(json_path, 'r', encoding='utf-8') as f:
        try:
            data = json.load(f)
        except Exception as e:
            logger.error(f"Failed to parse JSON file: {e}")
            db.close()
            return
            
    verified_leads = data.get("verified_leads", [])
    logger.info(f"Discovered {len(verified_leads)} leads to migrate.")
    
    inserted = 0
    updated = 0
    
    for idx, item in enumerate(verified_leads):
        email = item.get("email")
        if not email:
            continue
            
        # Check if lead already exists in db
        lead = db.query(models.Lead).filter(models.Lead.email == email).first()
        
        # Parse revenue
        rev = item.get("annual_revenue_inr", 0.0)
        try:
            rev_val = float(rev)
        except:
            rev_val = 0.0
            
        # Parse score
        score = item.get("icp_score", 0.0)
        try:
            score_val = float(score)
        except:
            score_val = 0.0
            
        if not lead:
            lead = models.Lead(
                name=item.get("name", "Unknown Contact"),
                email=email,
                company=item.get("company_name", ""),
                role=item.get("contact_role", ""),
                country=item.get("geography", ""),
                annual_revenue=rev_val,
                is_qualified=item.get("qualified", False),
                score=score_val,
                source_agent=item.get("generating_agent", "imported"),
                status="VETTED" if item.get("qualified") else "NEW"
            )
            db.add(lead)
            inserted += 1
        else:
            lead.name = item.get("name", lead.name)
            lead.company = item.get("company_name", lead.company)
            lead.role = item.get("contact_role", lead.role)
            lead.country = item.get("geography", lead.country)
            lead.annual_revenue = rev_val
            lead.is_qualified = item.get("qualified", lead.is_qualified)
            lead.score = score_val
            lead.source_agent = item.get("generating_agent", lead.source_agent)
            updated += 1
            
        # Commit every 200 items to manage transaction sizes
        if (idx + 1) % 200 == 0:
            db.commit()
            logger.info(f"Processed {idx + 1}/{len(verified_leads)} leads...")
            
    db.commit()
    logger.info(f"Migration completed successfully. Inserted: {inserted}, Updated: {updated}.")
    db.close()

if __name__ == "__main__":
    run_migration()
