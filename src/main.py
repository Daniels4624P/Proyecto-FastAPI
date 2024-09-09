from fastapi import FastAPI, Request
import asyncio
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from routers import CRUD,autenticacion
from templates.templates import templates
from routers.notification_task import check_tasks_one_day,check_tasks_one_hour

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(check_tasks_one_hour())

@app.on_event("startup")
async def evento_de_inicio():
    asyncio.create_task(check_tasks_one_day())

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(CRUD.router)
app.include_router(autenticacion.router)

@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/users/me/page", response_class=HTMLResponse)
async def users_me_page(request: Request):
    return templates.TemplateResponse("me.html", {"request": request})

@app.get("/register/page")
async def register(request: Request):
    return templates.TemplateResponse("register.html",{"request": request})

@app.get("/register/admin/sadsadsadsadsadsadsad/page")
async def register(request: Request):
    return templates.TemplateResponse("register_admin.html",{"request": request})

@app.get("/register/editor/sadasdsadsadsads/page")
async def register(request: Request):
    return templates.TemplateResponse("register_editor.html",{"request": request})

@app.get("/tareas/page")
async def tareas(request: Request):
    return templates.TemplateResponse("tareas.html", {"request": request})

@app.get("/tarea/page")
async def tareas(request: Request):
    return templates.TemplateResponse("tarea.html", {"request": request})

@app.get("/crear_tarea/page")
async def tareas(request: Request):
    return templates.TemplateResponse("crear_tarea.html", {"request": request})

@app.get("/actualizar_tarea/page")
async def tareas(request: Request):
    return templates.TemplateResponse("actualizar_tarea.html", {"request": request})

@app.get("/eliminar_tarea/page")
async def tareas(request: Request):
    return templates.TemplateResponse("eliminar_tarea.html", {"request": request})