from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from routers import CRUD,autenticacion
from templates.templates import templates
from datetime import datetime, timedelta
import schedule
from db.db import db_tasks, db_users
import smtplib
from email.mime.text import MIMEText
import time
import threading

app = FastAPI()

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

smtp_server = "smtp.gmail.com"
smtp_port = 587
smtp_username = "taskmanager61@gmail.com"
smtp_password = "ftlucrdbiaanpeuz"

def job():
    now = datetime.now()
    one_day_later = now + timedelta(days=1)

    start_of_day = datetime(one_day_later.year,one_day_later.month,one_day_later.day)
    end_of_day = start_of_day + timedelta(days=1)

    tasks_expiring = db_tasks.tasks.find({"date_expire": {"$gte": start_of_day, "$lt": end_of_day}})

    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(smtp_username,smtp_password)

    for task in tasks_expiring:
        owner_username = task["owner"]
        task_name = task["task"]
        date_expire = task["date_expire"]

        user = db_users.users_proyect.find_one({"username": owner_username})
        if user and "email" in user:
            user_email = user["email"]

            subject = f"Recordatorio: La tarea '{task_name}' está próxima a expirar"
            body = f"Hola {owner_username},\n\nLa tarea '{task_name}' expira el {date_expire.strftime('%Y-%m-%d %H:%M:%S')}.\nPor favor, tómate un momento para completarla o actualizar su estado.\n\nSaludos,\nEquipo de Task Manager"
            msg = MIMEText(body)
            msg['Subject'] = subject
            msg['From'] = smtp_username
            msg['To'] = user_email

            try:
                server.sendmail(smtp_username, user_email, msg.as_string())
                print(f"Correo enviado a {user_email} sobre la tarea {task_name}.")
            except Exception as e:
                print(f"Error al enviar correo a {user_email}: {e}")
        
        else:
            print(f"No se encontró el correo electrónico para el usuario {owner_username}.")

    server.quit()

def run_scheduler():
    # Programar la tarea diaria
    schedule.every().day.at("00:00").do(job)
    
    while True:
        schedule.run_pending()
        time.sleep(60)

# Iniciar el scheduler en un hilo separado
scheduler_thread = threading.Thread(target=run_scheduler)
scheduler_thread.daemon = True  # El hilo se cerrará cuando termine el programa principal
scheduler_thread.start()

# Aquí iría tu código principal
print("El programa principal sigue ejecutándose.")

# Simulación de código adicional
for i in range(10):
    print(f"Realizando otra tarea... {i}")
    time.sleep(2)

def job_2():
    now = datetime.now()
    one_hour_later = now + timedelta(hours=1)

    start_of_hour = now
    end_of_hour = one_hour_later

    tareas = db_tasks.tasks.find({"date_expire": {"$gte": start_of_hour, "$lt": end_of_hour}})

    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(smtp_username, smtp_password)

    for tarea in tareas:
        owner_username = tarea["owner"]
        task = tarea["task"]
        date_expire = tarea["date_expire"]

        user = db_users.users_proyect.find_one({"username": owner_username})
        if user and "email" in user:
            user_email = user["email"]

            subject = f"Recordatorio: La tarea '{task}' expira en una hora"
            body = (f"Hola {owner_username},\n\n"
                f"La tarea '{task}' expira el {date_expire.strftime('%Y-%m-%d %H:%M:%S')}.\n"
                "Te recomendamos que tomes acción para completarla o actualizar su estado.\n\n"
                "Saludos,\nEquipo de Task Manager")
            msg = MIMEText(body)
            msg["Subject"] = subject
            msg["From"] = smtp_username
            msg["To"] = user_email

            try:
                server.sendmail(smtp_username,user_email,msg.as_string())
                print(f"Correo enviado a {user_email} sobre la tarea '{task}'.")
            except Exception as e:
                print(f"Error al enviar correo a {user_email}: {e}")
        else:
            print(f"No se encontró el correo electrónico para el usuario {owner_username}.")
    server.quit()
def run_scheduler_2():
    schedule.every().hour.at(":39").do(job_2)

    while True:
        schedule.run_pending()
        time.sleep(60)

scheduler_thread_2 = threading.Thread(target=run_scheduler_2)
scheduler_thread_2.daemon = True
scheduler_thread_2.start()

print("El programa principal sigue ejecutandose.")

for i in range(10):
    print(f"Realizando otra tarea... {i}")
    time.sleep(2)
