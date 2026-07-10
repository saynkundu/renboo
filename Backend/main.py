from modules.hashed_password import check_password,create_hash_password
from modules.token import create_toke,decode_token
from fastapi import FastAPI,Request,Depends,BackgroundTasks,HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse,
from fastapi.staticfiles import StaticFiles
from fastapi.security import OAuth2PasswordBearer
from modules.schema import login,register
from modules.database import MySQLDatabase


templates=Jinja2Templates(directory="../Frontend")


app = FastAPI(
    title="My API",
    description="Example FastAPI app",
    version="1.0.0",
    contact={
        "name": "Support Team",
        "url": "https://example.com/contact",
        "email": "support@example.com"
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT"
    }
)

db=MySQLDatabase()
outh=OAuth2PasswordBearer(tokenUrl="token")

""" get methods"""


@app.post("token")
async def create_token(request:Request):
    data=await request.json()
    tok=create_toke(data)
    return {"token":tok,"access_type":"bearer"}

@app.get("/",response_class=HTMLResponse)
async def home_page(request:Request):
    return templates.TemplateResponse({"request":request},"index.html")

@app.post("/login",response_class=HTMLResponse)
async def user_login(user:login):
    query = """
        SELECT * FROM users
        WHERE email = %s
    """

    db_user = db.fetch_one(query, (user.email,))

    # Check if user exists
    if db_user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    # Check password
    if db_user["password"] != user.password:
        raise HTTPException(
            status_code=401,
            detail="Invalid password"
        )

    return {
        "message": "Login Successful",
        "user": {
            "id": db_user["id"],
            "username": db_user["username"],
            "email": db_user["email"]
        }
    }

