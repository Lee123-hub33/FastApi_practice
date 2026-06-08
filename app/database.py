import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from dotenv import load_dotenv
from urllib.parse import urlparse, quote_plus

load_dotenv()

RAW_DATABASE_URL = os.getenv("DATABASE_URL")

if not RAW_DATABASE_URL:
    raise ValueError("DATABASE_URL must be set in .env file.")

# Parse the string into safe components to isolate your password
parsed_url = urlparse(RAW_DATABASE_URL)

# Extract and securely encode only the password component in memory
if parsed_url.password:
    encoded_password = quote_plus(parsed_url.password)
    # Rebuild the URL safely without hardcoding anything
    DATABASE_URL = RAW_DATABASE_URL.replace(f":{parsed_url.password}@", f":{encoded_password}@")
else:
    DATABASE_URL = RAW_DATABASE_URL

engine = create_engine(DATABASE_URL)
sessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()