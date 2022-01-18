# we have many enviroments created in project so we have to set every enviroment while production or
# development for validation or verfication of env variables, 
# if we forgot to set any env the app may be creashed. while retriving env variable it is all are in form of string so we have validate eery variable is in right form
# so pandanting has builtin function "BaseSettings" for performing all of this validation and form
from pydantic import BaseSettings

# for validation
class Settings(BaseSettings):
    database_hostname:str
    database_port:str
    database_password:str
    database_name:str
    database_username:str
    secret_key:str
    algorithm:str
    access_token_expire_minutes:int
    
    class Config:
        env_file= '.env'

settings = Settings()