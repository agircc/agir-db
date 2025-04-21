import os
import sys
from logging.config import fileConfig
import getpass

# Add the project root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
from app.db.base import Base
target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.
from app.core.config import settings

# Use database URL from configuration
config.set_main_option("sqlalchemy.url", str(settings.SQLALCHEMY_DATABASE_URI))

def run_migrations_offline():
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        include_schemas=True,
        include_object=include_object,
    )

    with context.begin_transaction():
        context.run_migrations()


def include_object(object, name, type_, reflected, compare_to):
    """Determine which objects should be included in auto-generated migrations"""
    return True


def process_revision_directives(context, revision, directives):
    """Hook function to modify generated migration scripts"""
    # Main migration script
    if directives and len(directives) > 0:
        # Get script object
        script = directives[0]
        if script.upgrade_ops and script.upgrade_ops.ops:
            # Find operations that create enum types and ensure they execute before column additions
            enum_ops = []
            non_enum_ops = []
            
            for op in script.upgrade_ops.ops:
                if hasattr(op, 'create_type') and op.create_type:
                    enum_ops.append(op)
                else:
                    non_enum_ops.append(op)
            
            # Reorganize operation order, create enum types first
            script.upgrade_ops.ops = enum_ops + non_enum_ops


def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, 
            target_metadata=target_metadata,
            include_schemas=True,
            include_object=include_object,
            process_revision_directives=process_revision_directives,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online() 