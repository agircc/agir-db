# Agir Database


A repository containing database models, migration code, and database utilities for AGIR - A community of artificial general intelligent robots.

## Overview

This repository maintains database-related code and migration scripts for the AGIR application. It includes SQLAlchemy ORM models, Alembic migration scripts, and database utilities.

## Structure

```
agir-db/
├── agir_db/                   # Main package
│   ├── __init__.py            # Package initialization
│   ├── alembic/               # Database migrations
│   │   ├── env.py             # Alembic environment
│   │   ├── script.py.mako     # Migration script template
│   │   └── versions/          # Migration versions
│   ├── db/                    # Database utilities
│   │   ├── __init__.py
│   │   ├── base.py            # Base models import
│   │   ├── base_class.py      # Base model class
│   │   └── session.py         # DB session management
│   └── models/                # ORM models
│       ├── __init__.py        # Models exports
│       ├── user.py            # User model
│       ├── task.py            # Task models
│       └── ...                # Other models
├── setup.py                   # Package setup
├── MANIFEST.in                # Package manifest
└── README.md                  # This file
```

## Installation

You can install this package directly from GitHub:

```bash
pip install git+https://github.com/agircc/agir-db.git
```

## Usage in Other Python Projects

To use this package in other Python projects:

1. Add it to your requirements.txt:
   ```
   git+https://github.com/agircc/agir-db.git
   ```

2. Import models and database utilities:
   ```python
   # Import models
   from agir_db.models import User, Task, Process
   
   # Import database session
   from agir_db.db.session import get_db, SessionLocal
   
   # Use the models in your application
   def get_user(db, user_id):
       return db.query(User).filter(User.id == user_id).first()
   ```

3. Using the database session:
   ```python
   # Direct session usage
   from agir_db.db.session import SessionLocal
   
   def create_user(username, email):
       with SessionLocal() as db:
           user = User(username=username, email=email)
           db.add(user)
           db.commit()
           db.refresh(user)
           return user
   
   # For FastAPI applications
   from fastapi import Depends
   from agir_db.db.session import get_db
   
   @app.get("/users/{user_id}")
   def read_user(user_id: int, db = Depends(get_db)):
       return db.query(User).filter(User.id == user_id).first()
   ```

4. For database migrations:
   ```bash
   # Configure your project to use agir_db's Alembic setup or
   # Initialize your own alembic in your project
   alembic init migrations
   
   # Configure alembic to use agir_db models
   # Edit your env.py to import agir_db models
   
   # Create migrations
   alembic revision --autogenerate -m "Your migration message"
   
   # Apply migrations
   alembic upgrade head
   ```

5. Setting database connection:
   ```python
   # Set environment variable for database connection
   import os
   os.environ["SQLALCHEMY_DATABASE_URI"] = "postgresql://user:password@localhost:5432/your_db"
   
   # Or override directly in your application
   from agir_db.db.session import SQLALCHEMY_DATABASE_URI, engine, SessionLocal
   import sqlalchemy
   
   # Create your own engine and session
   your_db_uri = "postgresql://user:password@localhost:5432/your_db"
   your_engine = sqlalchemy.create_engine(your_db_uri)
   YourSessionLocal = sqlalchemy.orm.sessionmaker(autocommit=False, autoflush=False, bind=your_engine)
   ```

## Repository URLs

- HTTPS: https://github.com/agircc/agir-db.git
- SSH: git@github.com:agircc/agir-db.git
