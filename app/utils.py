# to encrypt password
from passlib.context import CryptContext
# to encrypt or hashing the password in database
pwd_context=CryptContext(schemes=["bcrypt"],deprecated="auto")

# defining function to hash password
def hash(password:str):
    return pwd_context.hash(password)
    

# defining function to check password is correct for login/JWT token 

def verify(plain_password,hashed_password):
    return pwd_context.verify(plain_password,hashed_password)