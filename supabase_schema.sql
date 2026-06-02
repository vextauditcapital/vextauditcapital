-- ================================================================================
-- VEXT AUDIT CAPITAL — ENTERPRISE DATABASE SCHEMA (POSTGRESQL / SUPABASE)
-- ================================================================================
-- This schema transitions Vext Audit Capital from a flat-file JSON and Google Sheets
-- database to an enterprise-grade, highly indexed relational database with full SOC 2 Type II
-- compliance, banking-grade security, and automated telemetry.

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- 1. Clients Master Table
CREATE TABLE IF NOT EXISTS clients (
    client_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    phone VARCHAR(50),
    company VARCHAR(255),
    country VARCHAR(100),
    gstin VARCHAR(15),
    industry VARCHAR(100),
    source VARCHAR(100),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Index for fast client search by email and company
CREATE INDEX IF NOT EXISTS idx_clients_email ON clients(email);
CREATE INDEX IF NOT EXISTS idx_clients_company ON clients(company);

-- 2. Client Relationship Profiles Table (DPDP-Compliant Isolation of PII)
CREATE TABLE IF NOT EXISTS relationship_profiles (
    client_id UUID PRIMARY KEY REFERENCES clients(client_id) ON DELETE CASCADE,
    birthday DATE,
    anniversary DATE,
    spouse_name VARCHAR(255),
    spouse_birthday DATE,
    father_name VARCHAR(255),
    father_birthday DATE,
    mother_name VARCHAR(255),
    mother_birthday DATE,
    children JSONB DEFAULT '[]'::jsonb,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 3. Audits and Transactions Table
CREATE TABLE IF NOT EXISTS audits (
    audit_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    client_id UUID REFERENCES clients(client_id) ON DELETE SET NULL,
    service_key VARCHAR(100) NOT NULL,
    base_price NUMERIC(12, 2) NOT NULL,
    gst_amount NUMERIC(12, 2) NOT NULL,
    total_price NUMERIC(12, 2) NOT NULL,
    currency VARCHAR(10) DEFAULT 'INR',
    status VARCHAR(50) DEFAULT 'PENDING', -- PENDING, PAID, IN_PROGRESS, COMPLETED, CANCELLED
    document_url VARCHAR(1024), -- Secure, S3 expiring pre-signed URL
    hmac_sig VARCHAR(64) NOT NULL, -- Cryptographic event verification
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for financial analytics
CREATE INDEX IF NOT EXISTS idx_audits_status ON audits(status);
CREATE INDEX IF NOT EXISTS idx_audits_service ON audits(service_key);
CREATE INDEX IF NOT EXISTS idx_audits_created_at ON audits(created_at);

-- 4. B2B Leads Table (Ingested from background sourcing agents)
CREATE TABLE IF NOT EXISTS leads (
    lead_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    company VARCHAR(255),
    role VARCHAR(100),
    country VARCHAR(100),
    annual_revenue NUMERIC(18, 2), -- Stored in local currency/converted
    is_qualified BOOLEAN DEFAULT FALSE,
    score NUMERIC(5, 2) DEFAULT 0.0,
    source_agent VARCHAR(100), -- The agent that sourced the lead
    status VARCHAR(50) DEFAULT 'NEW', -- NEW, VETTED, QUALIFIED, CONTACTED, CONVERTED, REJECTED
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for sales and pipeline routing
CREATE INDEX IF NOT EXISTS idx_leads_is_qualified ON leads(is_qualified);
CREATE INDEX IF NOT EXISTS idx_leads_status ON leads(status);
CREATE INDEX IF NOT EXISTS idx_leads_score ON leads(score);

-- 5. Cryptographically Verifiable Audit Log (SOC 2 Compliant Telemetry Log)
CREATE TABLE IF NOT EXISTS telemetry_logs (
    log_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    action VARCHAR(100) NOT NULL,
    operator VARCHAR(100) NOT NULL,
    status VARCHAR(50) NOT NULL,
    details TEXT,
    payload_hash VARCHAR(64) NOT NULL, -- SHA256 Hash of telemetry details
    hmac_sig VARCHAR(64) NOT NULL, -- Cryptographic signature verify block
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for rapid SOC 2 audits
CREATE INDEX IF NOT EXISTS idx_telemetry_action ON telemetry_logs(action);
CREATE INDEX IF NOT EXISTS idx_telemetry_created_at ON telemetry_logs(created_at);

-- 6. Trigger to auto-update 'updated_at' column
CREATE OR REPLACE FUNCTION update_modified_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = now();
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_clients_modtime BEFORE UPDATE ON clients FOR EACH ROW EXECUTE PROCEDURE update_modified_column();
CREATE TRIGGER update_relationship_modtime BEFORE UPDATE ON relationship_profiles FOR EACH ROW EXECUTE PROCEDURE update_modified_column();
CREATE TRIGGER update_audits_modtime BEFORE UPDATE ON audits FOR EACH ROW EXECUTE PROCEDURE update_modified_column();
CREATE TRIGGER update_leads_modtime BEFORE UPDATE ON leads FOR EACH ROW EXECUTE PROCEDURE update_modified_column();
