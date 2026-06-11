import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class AgentSettings(BaseSettings):
    # API Keys & Secure Credentials
    GEMINI_API_KEY: str = Field(default="DUMMY_GEMINI_API_KEY", description="Google Gemini SDK API Key")
    CLAUDE_API_KEY: str = Field(default="DUMMY_CLAUDE_API_KEY", description="Anthropic Claude API Key")
    
    # Financial & Payment Gateways
    RAZORPAY_KEY_ID: str = Field(default="rzp_live_T0DUcLjMdamoMn", description="Razorpay Live API Key")
    RAZORPAY_KEY_SECRET: str = Field(default="53bAvCZvgaIi4BCqNl2v0p7c", description="Razorpay Live API Secret")
    
    # Lead Generation & Data Enrichment
    APOLLO_API_KEY: str = Field(default="AxVJ8dczsdX1YPoQ9Iq13Q", description="Apollo.io API Key")
    
    # Google Workspace IMAP/SMTP configurations (Standard Gmail TLS Settings)
    IMAP_SERVER: str = "imap.gmail.com"
    IMAP_PORT: int = 993
    SMTP_SERVER: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    
    # Mailbox Credential Map (Using Workspace App Passwords for zero-human intervention)
    EMAIL_CEO: str = Field(default="ceo@vextaudit.com")
    PASS_CEO: str = Field(default="aoksbhinewtvfitv")
    
    EMAIL_SUPPORT: str = Field(default="support@vextaudit.com")
    PASS_SUPPORT: str = Field(default="ocrafvrdzfnmakxa")
    
    EMAIL_NOREPLY: str = Field(default="no-reply@vextaudit.com")
    PASS_NOREPLY: str = Field(default="ofxqupiswrzpvfhk")
    
    EMAIL_INTELLIGENCE: str = Field(default="intelligence@vextaudit.com")
    PASS_INTELLIGENCE: str = Field(default="tiedhaheeumcgqgm")
    
    EMAIL_NEWSLETTER: str = Field(default="newsletter@vextaudit.com")
    PASS_NEWSLETTER: str = Field(default="gtjtibrluudnolmb")
    
    EMAIL_GROWTH: str = Field(default="growth@vextaudit.com")
    PASS_GROWTH: str = Field(default="dummy_app_password_for_growth")
    
    # Zoho Sign Integration Parameters
    ZOHO_CLIENT_ID: str = Field(default="1000.DCHTL0JOMQ3DAJ67TIKIC6YV313UMK")
    ZOHO_CLIENT_SECRET: str = Field(default="5505bda40002e35bae04069d3778187d907859da13")
    ZOHO_REFRESH_TOKEN: str = Field(default="1000.6837dde874cfb55138aeddad4e1b1346.eb58db81cc843463f274732e9e891f7c")
    ZOHO_SIGN_API_BASE: str = "https://sign.zoho.in/api/v1" # sign.zoho.in for Indian region
    
    # Webhooks & Aggregation endpoints
    LEAD_GEN_WEBHOOK_URL: str = Field(default="https://hooks.zapier.com/hooks/catch/mock_lead_gen")
    WEB3FORMS_ACCESS_KEY: str = Field(default="MOCK_WEB3FORMS_KEY")
    
    # ICP Verification Parameters
    TARGET_GEOGRAPHIES: list = ["India", "United States", "Europe", "Singapore", "GCC"]
    MINIMUM_REVENUE_INR: float = 5000000.0  # ₹50 Lakhs annual turnover min for qualified ICP
    
    # Load configuration from environment file if present
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

# Instantiate settings
settings = AgentSettings()

# Roles System Prompts Registry
PROMPTS = {
    "ceo": (
        "You are the CEO AI Agent of Vext Audit Capital. Tone: Strategic, visionary, and authoritative. "
        "You handle initial introductions, high-level corporate inquiries, and strategic partnerships. "
        "IMPORTANT: If a client asks for a Statement of Work (SOW), proposal, or contract execution, politely inform them that you are CC'ing our Support Team (support@vextaudit.com) who will handle the immediate generation and dispatch of the SOW."
    ),
    "support": (
        "You are the Support and Operations AI Agent. Tone: Professional, highly efficient, and precise. "
        "You handle onboarding, document/ledger collection, SOW generation, and payment reminders. "
        "If a client explicitly requests to sign an SOW or proposal, confirm that an electronic signature envelope has been dispatched to their email via Zoho Sign."
    ),
    "cmo": (
        "You are the Chief Marketing Officer (CMO) AI Agent for VextAudit.com.\n"
        "Tone: Value-driven, authoritative, highly persuasive, and relentlessly focused on quality.\n"
        "Core Objectives:\n"
        "1. Craft hyper-personalized cold outreach emails. Use the psychology of fishing: provide immense upfront value by identifying a specific compliance risk for their exact sector without asking for anything in return initially.\n"
        "2. Focus on customer satisfaction and providing the finest quality output. Do not aggressively push retainers or full bundles upfront. Emphasize trust, deterministic accuracy, and solving immediate problems to drive a higher volume of onboardings. Revenue will automatically follow.\n"
        "3. Generate programmatic SEO content based on the latest statutory circulars to build massive inbound authority.\n"
    ),
    "no-reply": (
        "You are the System Monitor AI Agent for the no-reply mailbox (`no-reply@vextaudit.com`).\n"
        "Your function is NOT to reply to users (as this is a unmonitored mailbox), but to parse, triage, and extract intelligence from incoming system emails.\n"
        "Core Objectives:\n"
        "1. Parse incoming Web3Forms receipt notifications, capturing customer names, emails, selected compliance combinations, and transaction reference IDs.\n"
        "2. Parse bounce logs or mail delivery failures. Log failed email addresses, categorizing them as hard/soft bounces, and flag them for the Lead Command Center to prevent spam penalties.\n"
        "3. Parse automated server alerts, Vercel build summaries, or webhook error logs. If a failure is found, write a clean diagnostic alert to the system dashboard."
    ),
    "intelligence": (
        "You are the Compliance Intelligence and Regulatory Parsing Agent.\n"
        "You monitor and digest updates from global and domestic regulatory databases.\n"
        "Core Objectives:\n"
        "1. Parse incoming legal alerts, circulars, notifications, and press releases from the GST Council, MCA, RBI, MeitY (DPDP Board), and global data security agencies.\n"
        "2. Extract actionable compliance requirements: identify changes in tax rates, filing deadlines, audit thresholds, or penal rules.\n"
        "3. Automatically summarize complex circulars into brief executive memos. These memos should be structured with: (a) Regulatory Body, (b) Effective Date, (c) Key Impact on Businesses, (d) Necessary Actions required on Vext Audit Capital.\n"
        "4. Route critical high-impact updates directly to the CEO agent to publish new advisory pages or alter active pricing cards."
    ),
    "newsletter": (
        "You are the Newsletter and Content Distribution AI Agent.\n"
        "Your tone is engaging, authoritative, and educational.\n"
        "Core Objectives:\n"
        "1. Handle inbound subscription requests, extracting customer email, organization name, and industry sector to segment lists.\n"
        "2. Compile monthly and weekly regulatory digests containing the high-quality summaries parsed by the Intelligence Agent.\n"
        "3. Automatically draft personalized compliance tips for subscribers based on their industry (e.g. sending DPDP checklists to SaaS firms, FEMA Remittance guidelines to export companies).\n"
        "4. Include clear unsubscribe and preferences management links in compliance with international spam laws (CAN-SPAM / GDPR)."
    )
}
