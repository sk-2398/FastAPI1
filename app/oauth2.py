# generating JWT token....install -- pip install "python-jose[cryptography]
from jose import JWTError,jwt
from datetime import datetime,timedelta

from sqlalchemy.orm.session import Session

from app import database
from . import schemas
# to get current user for requested token
from fastapi import Depends,HTTPException,status
from fastapi.security import OAuth2PasswordBearer
from . import models
oauth2_scheme=OAuth2PasswordBearer(tokenUrl='login')
from .config import settings
# creating secrete key
#instead of harding coding SECRET_KEY ALG we import it from env from config
SECRET_KEY=settings.secret_key
ALGORITHM =settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

# define function to create JWT token

def create_access_token(data:dict):
    to_encode=data.copy()
    expire=datetime.utcnow()+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})
    encode_jwt=jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return encode_jwt

# creating function to verify/valid token
def verify_access_token(token:str,credentials_exception):
    try:
        payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        id:str=payload.get("user_id")
        print(id)
        if id is None:
            raise credentials_exception
        token_data=schemas.TokenData(id=id)
    
    except JWTError:
        raise credentials_exception
    
    return token_data
    
# creating function for getting current user for requested token

def get_current_user(token:str = Depends(oauth2_scheme),db: Session=Depends(database.get_db)):
    credentials_exception=HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail=f"could not validate credentials",headers={"WWW-Authenticate":"Bearer"})
    
    # to fetch user based on token
    token=verify_access_token(token,credentials_exception)
    user=db.query(models.User).filter(models.User.id==token.id).first()
    
    
    return user