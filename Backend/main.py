from modules.hashed_password import check_password,create_hash_password
from modules.token import create_toke,decode_token
from fastapi import FastAPI,Request,Depends,BackgroundTasks,HTTPException,Response
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.security import OAuth2PasswordBearer
from modules.schema import Login,Register,BookSchema,IssueSchema,MemberSchema,ReturnSchema
from modules.database import MySQLDatabase
import datetime


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
async def user_login(user:Login):
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

@app.post("/register",response_class=HTMLResponse)
async def new_user(user:Register):
    query="""
SELECT email FROM users WHERE email=%s;
    """

    
    db_user = db.fetch_one(query, (user.email,))

    # Check if user exists
    if db_user:
        raise HTTPException(
            status_code=404,
            detail="Account Already present please Login"
        )
    else:
        if user.password!= user.confirm_password:
            raise HTTPException(
                status_code=400,
                detail="password and confirm password not match"
            )
        else:
            query_="""
INSERT INTO users(name,email,password_hash,phone,department,status,created_at) VALUES(%s,%s,%s,%s,%s,%s,%s);
"""
            hashed_password=create_hash_password(user.password)
            response=db.insert(query,(user.name,user.email,hashed_password,user.phone,user.department,"ACTIVE",datetime.datetime.now()))
            if response:
                token=create_token(user)
                return templates.TemplateResponse({"response":"user created","token":token},"dashboard.html")
            else:
                raise HTTPException(
                    status_code=400,
                    detail="Account not created please try again letter"
                )



@app.post("/logout", response_class=HTMLResponse)
async def logout(response: Response):
    # If you store JWT in cookies, clear it
    response.delete_cookie("access_token")
    return templates.TemplateResponse({"logout":"succesfully logged out"},"index.html")



"""     Dashboard """
@app.get("/dashboard/total-books")
async def total_books(request: Request):
    query = "SELECT COUNT(*) AS total FROM books;"
    result = db.fetch_one(query)
    return templates.TemplateResponse("dashboard.html", {"request": request, "total_books": result["total"]})

@app.get("/dashboard/available-books")
async def available_books(request: Request):
    query = "SELECT COUNT(*) AS available FROM books WHERE status='AVAILABLE';"
    result = db.fetch_one(query)
    return templates.TemplateResponse("dashboard.html", {"request": request, "available_books": result["available"]})

@app.get("/dashboard/issued-books")
async def issued_books(request: Request):
    query = "SELECT COUNT(*) AS issued FROM books WHERE status='ISSUED';"
    result = db.fetch_one(query)
    return templates.TemplateResponse("dashboard.html", {"request": request, "issued_books": result["issued"]})

@app.get("/dashboard/total-members")
async def total_members(request: Request):
    query = "SELECT COUNT(*) AS members FROM members;"
    result = db.fetch_one(query)
    return templates.TemplateResponse("dashboard.html", {"request": request, "total_members": result["members"]})



""" BOOKS """


@app.post("/books/add")
async def add_book(request: Request, book: BookSchema):
    query = "INSERT INTO books (title, author, isbn, status) VALUES (%s, %s, %s, %s);"
    db.insert(query, (book.title, book.author, book.isbn, "AVAILABLE"))
    return templates.TemplateResponse("books.html", {"request": request, "message": "Book added successfully"})

@app.post("/books/edit/{book_id}")
async def edit_book(request: Request, book_id: int, book: BookSchema):
    query = "UPDATE books SET title=%s, author=%s, isbn=%s WHERE id=%s;"
    db.update(query, (book.title, book.author, book.isbn, book_id))
    return templates.TemplateResponse("books.html", {"request": request, "message": "Book updated successfully"})

@app.post("/books/delete/{book_id}")
async def delete_book(request: Request, book_id: int):
    query = "DELETE FROM books WHERE id=%s;"
    db.delete(query, (book_id,))
    return templates.TemplateResponse("books.html", {"request": request, "message": "Book deleted successfully"})

@app.get("/books/search")
async def search_books(request: Request, keyword: str):
    query = "SELECT * FROM books WHERE title LIKE %s OR author LIKE %s;"
    results = db.fetch_all(query, (f"%{keyword}%", f"%{keyword}%"))
    return templates.TemplateResponse("books.html", {"request": request, "books": results})

""" member management """


@app.post("/members/add")
async def add_member(request: Request, member: MemberSchema):
    query = "INSERT INTO members (name, email, phone, department) VALUES (%s, %s, %s, %s);"
    db.insert(query, (member.name, member.email, member.phone, member.department))
    return templates.TemplateResponse("members.html", {"request": request, "message": "Member added successfully"})

@app.post("/members/edit/{member_id}")
async def edit_member(request: Request, member_id: int, member: MemberSchema):
    query = "UPDATE members SET name=%s, email=%s, phone=%s, department=%s WHERE id=%s;"
    db.update(query, (member.name, member.email, member.phone, member.department, member_id))
    return templates.TemplateResponse("members.html", {"request": request, "message": "Member updated successfully"})

@app.post("/members/delete/{member_id}")
async def delete_member(request: Request, member_id: int):
    query = "DELETE FROM members WHERE id=%s;"
    db.delete(query, (member_id,))
    return templates.TemplateResponse("members.html", {"request": request, "message": "Member deleted successfully"})

@app.get("/members/view")
async def view_members(request: Request):
    query = "SELECT * FROM members;"
    results = db.fetch_all(query)
    return templates.TemplateResponse("members.html", {"request": request, "members": results})


"""##book isuues"""

@app.post("/books/issue")
async def issue_book(request: Request, issue: IssueSchema):
    query = "UPDATE books SET status='ISSUED', issued_to=%s WHERE id=%s;"
    db.update(query, (issue.member_id, issue.book_id))
    return templates.TemplateResponse("issue.html", {"request": request, "message": "Book issued successfully"})

@app.post("/books/return")
async def return_book(request: Request, return_: ReturnSchema):
    query = "UPDATE books SET status='AVAILABLE', issued_to=NULL WHERE id=%s;"
    db.update(query, (return_.book_id,))
    return templates.TemplateResponse("issue.html", {"request": request, "message": "Book returned successfully"})

@app.get("/books/issued")
async def view_issued_books(request: Request):
    query = "SELECT * FROM books WHERE status='ISSUED';"
    results = db.fetch_all(query)
    return templates.TemplateResponse("issue.html", {"request": request, "issued_books": results})
