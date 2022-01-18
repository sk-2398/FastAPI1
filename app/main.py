from typing import List
from fastapi import FastAPI,Response,status,HTTPException,Depends
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
from sqlalchemy.sql.expression import false
from sqlalchemy.sql.sqltypes import Boolean
# to join /create model to main file
from .import models
from .database import engine,SessionLocal
models.Base.metadata.create_all(bind=engine)
from sqlalchemy.orm import Session
from .database import get_db
from .utils import hash
from .routers import post,user,auth,vote
from .config import Settings
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
 # "http://localhost.tiangolo.com",
    # "https://localhost.tiangolo.com",
    # "http://localhost",
    # "http://localhost:8080",
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def main():
    return {"message": "Hello World"}



# creating function or defining decorators for user and post 
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)




@app.get("/")
def root():
    return {"message": "Hello suyog"}

#creating get request /now is the url
@app.get("/new")
def get_post():
    return {"message":"This is new page"}




# creating function to test sqlalchemy
# @app.get("/sqlalchemy")
# def test_posts(db: Session = Depends(get_db)):
#     #creating database query
#     post=db.query(models.Post).all()
#     return {"data":post}
#     # return {"status":"success"}






#creating post request
@app.post("/create_post")
def create_post(post: dict=Body(...)): #post:dict=Body(...) it fetch all fields in body converted it into dict and stored in variable name body
    print(post)
    return {"new post": f"title :{post['title']} content:{post['content']}"}



# #defining schema to create post 
# class Post(BaseModel):
#     title:str
#     content:str
#     published:bool=True

    # published=Boolean
# -==============================================================================================================


# -==============================================================================================================




# creating demo database in form of array
my_posts=[{"title":"my first post","content":"This is my first post","id":7},
          {"title":"my second post","content":"This is my second post","id":8},
          {"title":"my third post","content":"This is my third post","id":9}]
# -==============================================================================================================

# defining function to fetch post by id
def find_post(id):
    for p in my_posts:
        if p['id']==id:
            return p
# -==============================================================================================================

# finding index of post to delete post
def index_post(id):
    for i,p in enumerate(my_posts):
        if p['id']==id:
            return i
# -==============================================================================================================
    
# #  creating function for getting latest post
# @app.get("/posts/latest")
# def latest_post():
#     post=my_posts[len(my_posts)-1]
#     print(len(my_posts))
#     return {"detail" : post}


# -==============================================================================================================
# -==============================================================================================================
# -==============================================================================================================
