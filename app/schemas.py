from typing import Optional
from pydantic import BaseModel,EmailStr
from datetime import datetime



# -==============================================================================================================
# -==============================================================================================================
# defining schema for auther details
# class auther(BaseModel):
#       username:str
#       class Config:
#         orm_mode=True

# -==============================================================================================================

#defining schema to create post 
# class Post(BaseModel):
#     title:str
#     content:str
#     published:bool=True
# other way to define schema
# -==============================================================================================================
# Creating schemas for how to take/recieve response from user
class PostBase(BaseModel):
    title:str
    content:str
    published:bool=True
    created_on:datetime
    auther_id:int
 
    class Config:
        orm_mode=True

class PostCreate(BaseModel):
    
    title:str
    content:str
    published:bool
    # pass
    
# -==============================================================================================================
# Creating schemas for how to showas/send data to user

# creating schema for how post shows/send to user/ we inherit postbase model and add only those field whiv=ch we want to add
# class vote(BaseModel):
  
#     votes:int
#     class Config:
#         orm_mode=True
class PostResp(BaseModel):
    Post : PostBase
    votes : int
    
    # auther_name:auther
    # vote:vote
    # addingconfid class bcoz pydantuc model only read dictionary it dont read sqlalchemy model 
    class Config:
        orm_mode=True
class Postt(PostBase):
    post_id:int
    votes:int
     # addingconfid class bcoz pydantuc model only read dictionary it dont read sqlalchemy model 
    class Config:
        orm_mode=True
    
# class Post(PostBase):
#     Post:PostResp
#     votes:int
    
#     class Config:
#         orm_mode=True
# -==============================================================================================================
# -==============================================================================================================
#defining schemas for creating users
class UserBase(BaseModel):
    username:str
    email_id:EmailStr
    password:str
# -==============================================================================================================

#creating schema for data to show user
class UserShow(BaseModel):
    id:int
    username:str
    email_id:str 
    created_on:datetime
    class Config:
        orm_mode=True



# -==============================================================================================================
# -==============================================================================================================
# schema for useer login
class UserLogin(BaseModel):
    # username:str
    email_id:EmailStr
    password:str

# creating schema for validating token
class Token(BaseModel):
    access_token:str
    token_type:str
    
class TokenData(BaseModel):
    id:Optional[str]=None
# -==============================================================================================================
# -==============================================================================================================
# creatinf schema for vote
from pydantic.types import conint
class Vote(BaseModel):
    post_id:int
    # conint used when we have relation betn number
    dir:conint(le=1)