from bcrypt import hashpw,checkpw,gensalt

def create_hash_password(raw_password:str):
    return hashpw(raw_password.encode("UTF-8"),gensalt(12))

def check_password(raw_password:str,hashed_password:bytes)->bool:
    return checkpw(raw_password.encode("UTF-8"),hashed_password)