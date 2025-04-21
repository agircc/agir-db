from setuptools import setup, find_packages

setup(
    name="agir_db",
    version="0.1.0",
    description="Database models and migration code for AGIR application",
    author="AGIR Team",
    author_email="info@agir.cc",
    url="https://github.com/agircc/agir-db",
    packages=find_packages(exclude=["tests*"]),
    python_requires=">=3.8",
    install_requires=[
        "sqlalchemy>=2.0.0",
        "alembic>=1.8.0",
        "psycopg2-binary>=2.9.0",
    ],
    include_package_data=True,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
) 