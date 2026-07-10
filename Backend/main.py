from modules.hashed_password import check_password,create_hash_password
from modules.token import create_toke,decode_token
from fastapi import FastAPI,Request,Depends,BackgroundTasks
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.security import OAuth2PasswordBearer
from modules.schema import login,register


templates=Jinja2Templates(directory="frontend")

app=FastAPI(
    title="Library BOOK Management TOOL",
    summary="Its a demo book management system",
    description="you can manage all your library books",
    version="0.0.1",
    contact="123456789"
)
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
    password=user.password

