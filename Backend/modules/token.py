from jwt import encode,decode
import datetime
import os
from dotenv import load_dotenv
load_dotenv()

def create_toke(data:dict):
    copy_data=data.copy()
    copy_data["exp"]=datetime.datetime.utcnow()+datetime.timedelta(minutes=20)
    copy_data["iat"]=datetime.datetime.utcnow()
    token=encode(copy_data,key=os.getenv("SECRETKEY"),algorithm=os.getenv("ALGORITHM"))
    return token

def decode_token(token:str)->dict:
    data=decode(token,key=os.getenv("SECRETKEY"),algorithms=[os.getenv("ALGORITHM")])
    return data
