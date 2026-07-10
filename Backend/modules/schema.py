from pydantic import BaseModel,field_validator
 

class login:
    email : str
    password: str 
    role: str

class register:
    name:str 
    email: str 
    password: str 
    confirm_password:str 