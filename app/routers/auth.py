# JWT authentication
from fastapi import APIRouter,HTTPException,Depends,status,Response
# /to retriving user credentials via built in function
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..database import get_db
from ..schemas import Token, UserLogin
from .. import models
from ..utils import verify
from ..oauth2 import create_access_token
router=APIRouter(
    tags=['Authentications']
)

@router.post("/login",response_model=Token)
# def login(user_credential:UserLogin,db:Session=Depends(get_db)):
# retriving user credentials by buillt in function
def login(user_credential:OAuth2PasswordRequestForm=Depends(),db:Session=Depends(get_db)):
    user=db.query(models.User).filter(models.User.email_id==user_credential.username).first() 
    #when we use built in fun to retrive user credentials / put data in form-data in postman
    # user_uname=db.query(models.User).filter(models.User.username==user_credential.username).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Invalid Email or username")
    
    if not verify(user_credential.password,user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Invalid Credentials")
        
    # Creating access token
    access_token=create_access_token(data= {"user_id":user.id})
    
    return {"access_token":access_token,"token_type":"bearer"}

