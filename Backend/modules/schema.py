from pydantic import BaseModel,field_validator
 

class Login(BaseModel):
    email : str
    password: str 
    role: str

class Register(BaseModel):     
    name :str        
    email : str         
    password:str 
    confirm_password: str 
    phone :str        
    department :str    

class BookSchema(BaseModel):
    title: str
    author: str
    isbn: str       
class MemberSchema(BaseModel):
    name: str
    email: str
    phone: str
    department: str

class IssueSchema(BaseModel):
    book_id: int
    member_id: int
class ReturnSchema(BaseModel):
    book_id: int
