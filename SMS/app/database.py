

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

# DB_URL =  "mysql+pymysql://root:Root@1234@localhost:3633/sms_db"
DB_URL = "mysql+pymysql://root:Root%401234@localhost:3306/sms_db"

engine = create_engine(DB_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()