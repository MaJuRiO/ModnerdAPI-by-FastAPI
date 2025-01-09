from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "mysql+pymysql://admin:wHg05rEqGbQe3k3GvllSiDFq260BK45meu4EZS1v@database-cpe-34-senior-project.c7skg2ygwit0.ap-southeast-1.rds.amazonaws.com:3306/modlink_database"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()