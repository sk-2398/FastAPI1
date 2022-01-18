from sqlite3 import DatabaseError
from tkinter import CASCADE
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey
from .database import Base
from sqlalchemy import Column,Integer,String,Boolean
from sqlalchemy.sql.sqltypes import TIMESTAMP

from sqlalchemy.sql.expression import false, null,text

'''we cannot add any column after creating an table, we cannot extend any column so we have to use alembic which help us add or edit table column
we have to add some setting in env.py file in alemic, import Base from models.py file which we created in app to env.py 
and add url for database inalambic.ini or instead of hardcoding add 
config.set_main_option(" postgresql+psycopg2://postgres:suyog123@localhost:5432/fastAPI1") in env.py in alembic

to create table using alembic use command alembic revision -m "create posts table" it creates one py file in almbic folder we have to put logic in upgrade and downgrade function to create table in db
'''

# creating table for Post in daatabase
class Post(Base):
    __tablename__="posts"
    
    id=Column(Integer,nullable=False,primary_key=True)
    title=Column(String,nullable=False)
    content=Column(String,nullable=False)
    published=Column(Boolean,server_default="TRUE",nullable=false)
    created_on=Column(TIMESTAMP(timezone=True),nullable=False,server_default=text("now()"))
    # creating column for post auther id to find auther of post from user id
    auther_id=Column(Integer,ForeignKey("users.id",ondelete="CASCADE"),nullable=False)
    # to fetch post auther details we show realtion of tables
    auther_name=relationship("User")
    
    
    
    
    

#creating user model to save user information in db
class User(Base):
    __tablename__="users"
    id=Column(Integer,nullable=False,primary_key=True)
    username=Column(String,nullable=False,unique=True)
    email_id=Column(String,nullable=False,unique=True)
    password=Column(String,nullable=False)
    created_on=Column(TIMESTAMP(timezone=True),nullable=False,server_default=text("now()"))
    phone_number=Column(String)
    
    
# creating table for vote in Database

class Vote(Base):
    __tablename__="votes"
    user_id=Column(Integer, ForeignKey("users.id",ondelete="CASCADE"),primary_key=True)
    post_id=Column(Integer,ForeignKey("posts.id", ondelete="CASCADE"),primary_key=True)