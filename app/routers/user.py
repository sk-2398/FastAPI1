from typing import List
from fastapi import FastAPI,Response,status,HTTPException,Depends,APIRouter
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2

from psycopg2.extras import RealDictCursor
from sqlalchemy.sql.expression import false
from sqlalchemy.sql.operators import exists
from sqlalchemy.sql.sqltypes import Boolean
# to join /create model to main file
from .. import models
from ..database import engine,SessionLocal

from sqlalchemy.orm import Session
import time
from ..database import get_db
from ..utils import hash
from ..schemas import UserBase, UserShow
# defining router to connect with main file
router=APIRouter(
    prefix="/users",
    tags=["Users"]
)




#creating user functions

@router.post("/new_user",status_code=status.HTTP_201_CREATED,response_model=UserShow)
def create_user(user:UserBase,db: Session = Depends(get_db)):
    # haching user password
    hashed_password=hash(user.password)
    user.password=hashed_password
    new_user=models.User(**user.dict())
    # print(new_user)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
# -==============================================================================================================
# creating function for fetching user

@router.get("/{id}",response_model=UserShow)
def get_user(id:int,db: Session = Depends(get_db)):
    user=db.query(models.User).filter(models.User.id == id).first()
    if user==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Page Not Found")
    
    return user