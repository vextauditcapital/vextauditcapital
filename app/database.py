import os
import logging
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

logger = logging.getLogger("vext-api-database")

# Primary configuration: Database URL (typically Supabase or AWS RDS Postgres)
DATABASE_URL = os.getenv("SUPABASE_DATABASE_URL") or os.getenv("DATABASE_URL")

# If no database URL is present, use a highly portable local SQLite instance inside the project root for local offline testing/development
if not DATABASE_URL:
    DATABASE_URL = "sqlite:///./vextaudit_local.db"
    logger.warning("No Postgres DATABASE_URL discovered. Initialising local SQLite fallback engine.")

# Set up database engine
# For PostgreSQL, configure connection pooling parameters to prevent connection starvation
connect_args = {}
if DATABASE_URL.startswith("sqlite"):
    connect_args["check_same_thread"] = False # Required for multi-threaded SQLite handling
else:
    # Optimised connection pooling for high-concurrency cloud deployments
    connect_args = {
        "keepalives": 1,
        "keepalives_idle": 30,
        "keepalives_interval": 10,
        "keepalives_count": 5
    }

engine = create_engine(
    DATABASE_URL, 
    pool_size=10, 
    max_overflow=20, 
    pool_timeout=30, 
    pool_recycle=1800,
    connect_args=connect_args
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# FastAPI Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
