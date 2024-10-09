# db_connection.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

def connect_to_db():
    # Database connection details
    host = "35.224.207.195"
    port = "5432"
    dbname = "carerecords1"
    user = "postgres"
    password = "jelszo"

    # Create the database URL
    DATABASE_URL = f"postgresql://{user}:{password}@{host}:{port}/{dbname}"

    # Create the SQLAlchemy engine
    engine = create_engine(DATABASE_URL)

    # Create a configured "Session" class
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    # Return the SessionLocal class
    return SessionLocal()

def get_db():
    SessionLocal = connect_to_db()  # Get the SessionLocal class
    db = SessionLocal
    try:
        yield db
    finally:
        db.close()