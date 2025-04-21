from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

# Convert the PostgresDsn to string explicitly before passing to create_engine
database_uri = str(settings.SQLALCHEMY_DATABASE_URI)
engine = create_engine(database_uri, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 