from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# SQL Server connection details
DB_CONFIG = {
    "server": "server-name",
    "database": "db-name",
    "username": "login",
    "password": "password"
}

# SQLAlchemy connection string (No ODBC Required)
DATABASE_URL = f"mssql+pymssql://{DB_CONFIG['username']}:{DB_CONFIG['password']}@{DB_CONFIG['server']}/{DB_CONFIG['database']}"

# Create engine & session
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

def get_db_session():
    return SessionLocal()
