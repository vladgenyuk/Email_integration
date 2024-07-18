from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates


app = FastAPI()
templates = Jinja2Templates(directory="templates")


@app.get("/register")
def home(request: Request):
    return templates.TemplateResponse("registration.html", {"request": request})


@app.get("/load_emails")
def register(request: Request):
    return templates.TemplateResponse("load_emails.html", {"request": request})


@app.get("/all_emails")
def register(request: Request):
    return templates.TemplateResponse("all_emails.html", {"request": request})
