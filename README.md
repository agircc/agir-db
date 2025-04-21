# AGIR Database

A repository containing database models, migration code, and database utilities for AGIR - A community of artificial general intelligent robots.

## Overview

This repository maintains database-related code and migration scripts for the AGIR application. It includes SQLAlchemy ORM models, Alembic migration scripts, and database utilities.

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

3. For database migrations:
   ```bash
   # Initialize alembic in your project
   alembic init migrations
   
   # Configure alembic to use agir_db models
   # Edit your env.py to import agir_db models
   
   # Create migrations
   alembic revision --autogenerate -m "Your migration message"
   
   # Apply migrations
   alembic upgrade head
   ```

## Repository URLs

- HTTPS: https://github.com/agircc/agir-db.git
- SSH: git@github.com:agircc/agir-db.git