from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

# create_engine → creates connection to database
# sessionmaker → factory to create database sessions
# postgresql://username:password@host:port/database_name

db_url = "postgresql://shashankshukla:@localhost:5432/postgres"
engine = create_engine(db_url)
session = sessionmaker(autocommit = False, autoflush = False, bind = engine)

# autocommit=False -> Changes are NOT saved automatically. You must call db.commit()
# autoflush=False -> SQLAlchemy will NOT automatically push changes to DB before queries
# bind=engine -> Connects session to your database engine