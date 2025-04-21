from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

# Database configuration - should be set in environment variables
SQLALCHEMY_DATABASE_URI = os.environ.get(
    "SQLALCHEMY_DATABASE_URI", 
    "postgresql://postgres:postgres@localhost:5432/agir"
)

# Convert the PostgresDsn to string explicitly before passing to create_engine
database_uri = SQLALCHEMY_DATABASE_URI
engine = create_engine(database_uri, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 