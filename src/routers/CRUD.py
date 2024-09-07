from bson import ObjectId
from fastapi import APIRouter, HTTPException,status, Response, Depends, Request
from db.db import db_tasks, db_users
from db.models.models import Task, User, TASK_STATES
from db.schemas.schemas import user_schema,users_schema,task_schema,tasks_schema
from routers.autenticacion import get_current_user
from email.message import EmailMessage
import smtplib
from fastapi.templating import Jinja2Templates
from templates.templates import templates

router = APIRouter()

@router.get("/tareas")
async def mostrar_tareas(current_user: User = Depends(get_current_user)):
    if current_user.role in ["admin", "editor"]:
        return tasks_schema(db_tasks.tasks.find())
    tasks = tasks_schema(db_tasks.tasks.find({"owner": current_user.username}))
    return tasks

@router.get("/tarea")
async def find_user(task: str, current_user: User = Depends(get_current_user)):
    try:
        if current_user.role in ["admin", "editor"]:
            item = db_tasks.tasks.find_one({"task": task})
        if item is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No se encontro la tarea")
        return task_schema(item)
    except:
        item = db_tasks.tasks.find_one({"task": task, "owner": current_user.username})
        if item is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No se encontro la tarea")
        return task_schema(item)

@router.post("/crear_tarea")
async def crear_tarea(task: Task, current_user: User = Depends(get_current_user)):
    new_task = dict(task)
    del new_task["id"]
    new_task["owner"] = current_user.username
    existing_task = db_tasks.tasks.find_one({"task": task.task, "owner": current_user.username})
    if existing_task:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="La tarea ya existe")
    id = db_tasks.tasks.insert_one(new_task).inserted_id
    tarea = db_tasks.tasks.find_one({"_id": id})
    if not tarea:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Tarea no encontrada")
    owner = db_users.users_proyect.find_one({"username": current_user.username})
    if not owner:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Usuario no encontrado")
    recipient_email = owner.get("email")
    if not recipient_email:
        raise HTTPException(status_code=404, detail="Correo electrónico del usuario no encontrado")
    msg = EmailMessage()
    msg.set_content(f"Se pudo crear correctamente su tarea: {tarea["task"]}")
    msg["subject"] = "Creacion de Tarea en su Task Manager"
    msg["to"] = recipient_email
    user = "gola2010sa@gmail.com"
    msg["from"] = user
    password = "yvammjotufcmquai"
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(user, password)
        server.send_message(msg)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al enviar el correo: {e}")
    return f"tarea creada y correo enviado, tarea: {tarea["task"]}"

@router.put("/actualizar_tarea/{id}")
async def actualizar_tarea(id: str, task: Task, current_user: User = Depends(get_current_user)):
    task_db = db_tasks.tasks.find_one({"_id": ObjectId(id)})
    if not task_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="La tarea no existe")
    if current_user.role in ["admin", "editor"] or (current_user.role == "user" and task_db["owner": current_user.username]):
        db_tasks.tasks.update_one({"_id": ObjectId(id)},{"$set": task.dict(exclude={"id","owner"})})
        updated_task = db_tasks.tasks.find_one({"_id": ObjectId(id)})
        return task_schema(updated_task)
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No tiene suficientes permisos")

@router.delete("/eliminar_tarea/{task}")
async def eliminar_tarea(task: str, current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Usted no tiene permisos suficientes")
    found = db_tasks.tasks.find_one_and_delete({"task": task})
    if not found:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No se pudo eliminar la tarea")
    return Response(content="Su tarea fue eliminada correctamente")

