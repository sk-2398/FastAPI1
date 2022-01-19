#creating database connector using sqlalchemy
from sqlalchemy import create_engine
import psycopg2
from psycopg2.extras import RealDictCursor
from sqlalchemy.ext.declarative import declarative_base
import time

from sqlalchemy.orm import sessionmaker
from .config import settings
# to connect database using following specified code and path
# SQLALCHEMY_DATABASE_URL='postgresql:://<username>:<password>@<ipaddress/hostname>/<databasename'
# SQLALCHEMY_DATABASE_URL='postgresql://postgres:suyog123@localhost/fastAPI1'
#instead of hardcoding database details we can use env so we import settings from confing
SQLALCHEMY_DATABASE_URL=f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}/{settings.database_name}'



# creating engine to connect database to sqlalchemy to database
engine=create_engine(SQLALCHEMY_DATABASE_URL)

# to conversation with database we create session
SessionLocal=sessionmaker(autocommit=False,autoflush=False,bind=engine)

Base=declarative_base()

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()
# ==================================================================================================
# connecting to database
while True:
    try:
        conn=psycopg2.connect(host='localhost',database='fastAPI',user='postgres',password='suyog123',cursor_factory=RealDictCursor)
        cursor=conn.cursor()
        print("Database connection Successfull")
        break
    except Exception as error:
        print("Database connection failed")
        print(error)
        time.sleep(60)