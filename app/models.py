import uuid
from sqlalchemy import Column, String, Boolean, Numeric, DateTime, ForeignKey, Date, Text, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base

# Helper to support UUIDs across both Postgres and SQLite
def generate_uuid():
    return str(uuid.uuid4())

class Client(Base):
    __tablename__ = "clients"
    
    client_id = Column(String(36), primary_key=True, default=generate_uuid)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    phone = Column(String(50))
    company = Column(String(255), index=True)
    country = Column(String(100))
    gstin = Column(String(15))
    industry = Column(String(100))
    source = Column(String(100))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    profile = relationship("RelationshipProfile", back_populates="client", uselist=False, cascade="all, delete-orphan")
    audits = relationship("Audit", back_populates="client")

class RelationshipProfile(Base):
    __tablename__ = "relationship_profiles"
    
    client_id = Column(String(36), ForeignKey("clients.client_id", ondelete="CASCADE"), primary_key=True)
    birthday = Column(Date)
    anniversary = Column(Date)
    spouse_name = Column(String(255))
    spouse_birthday = Column(Date)
    father_name = Column(String(255))
    father_birthday = Column(Date)
    mother_name = Column(String(255))
    mother_birthday = Column(Date)
    children = Column(JSON, default=[]) # Stored as JSON list of child structures
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    client = relationship("Client", back_populates="profile")

class Audit(Base):
    __tablename__ = "audits"
    
    audit_id = Column(String(36), primary_key=True, default=generate_uuid)
    client_id = Column(String(36), ForeignKey("clients.client_id", ondelete="SET NULL"), index=True)
    service_key = Column(String(100), nullable=False, index=True)
    base_price = Column(Numeric(12, 2), nullable=False)
    gst_amount = Column(Numeric(12, 2), nullable=False)
    total_price = Column(Numeric(12, 2), nullable=False)
    currency = Column(String(10), default="INR")
    status = Column(String(50), default="PENDING", index=True)
    document_url = Column(String(1024))
    hmac_sig = Column(String(64), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    client = relationship("Client", back_populates="audits")

class Lead(Base):
    __tablename__ = "leads"
    
    lead_id = Column(String(36), primary_key=True, default=generate_uuid)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    company = Column(String(255))
    role = Column(String(100))
    country = Column(String(100))
    annual_revenue = Column(Numeric(18, 2))
    is_qualified = Column(Boolean, default=False, index=True)
    score = Column(Numeric(5, 2), default=0.0, index=True)
    source_agent = Column(String(100))
    status = Column(String(50), default="NEW", index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

class TelemetryLog(Base):
    __tablename__ = "telemetry_logs"
    
    log_id = Column(String(36), primary_key=True, default=generate_uuid)
    action = Column(String(100), nullable=False, index=True)
    operator = Column(String(100), nullable=False)
    status = Column(String(50), nullable=False)
    details = Column(Text)
    payload_hash = Column(String(64), nullable=False)
    hmac_sig = Column(String(64), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
