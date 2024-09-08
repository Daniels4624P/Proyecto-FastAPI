from bson import ObjectId
from fastapi import FastAPI, Request, BackgroundTasks
from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from routers import CRUD,autenticacion
from templates.templates import templates
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from db.db import db_tasks, db_users

app = FastAPI()

scheduler = BackgroundScheduler()
scheduler.start()

# Función para enviar correos (igual que antes)
def enviar_correo(destinatario, asunto, cuerpo):
    remitente = "gola2010sa@gmail.com"
    password = "yvammjotufcmquai"  # O usa variables de entorno

    msg = MIMEMultipart()
    msg['From'] = remitente
    msg['To'] = destinatario
    msg['Subject'] = asunto
    msg.attach(MIMEText(cuerpo, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(remitente, password)
        texto = msg.as_string()
        server.sendmail(remitente, destinatario, texto)
        server.quit()
        print(f"Correo enviado a {destinatario}")
    except Exception as e:
        print(f"Error al enviar correo: {e}")

def obtener_email_usuario(user):
    usuario = db_users.users_proyect.find_one({"username": user})
    if not usuario:
        return None
    return usuario['email']

# Función para verificar tareas desde MongoDB
def verificar_tareas():
    ahora = datetime.now()
    
    # Obtener todas las tareas que no han expirado
    tareas = db_tasks.tasks.find({"date_expire": {"$gte": ahora}})
    
    for tarea in tareas:
        diferencia = tarea['date_expire'] - ahora
        usuario_email = obtener_email_usuario(tarea['owner'])

        if usuario_email:
            if timedelta(days=1) >= diferencia > timedelta(days=0) and not tarea.get("reminder_1d_sent", False):
                enviar_correo(
                    usuario_email,
                    f"Recordatorio: Tarea '{tarea['task']}' se vence en 1 día",
                    f"Tu tarea '{tarea['task']}' se vence en 24 horas."
                )
                db_tasks.tasks.update_one({"_id": tarea["_id"]},{"$set": {"reminder_1d_sent": True}})
            if timedelta(hours=1) >= diferencia > timedelta(hours=0) and not tarea.get("reminder_1h_sent", False):
                enviar_correo(
                    usuario_email,
                    f"Recordatorio: Tarea '{tarea['task']}' se vence en 1 hora",
                    f"Tu tarea '{tarea['task']}' se vence en 1 hora."
                )
                db_tasks.tasks.update_one({"_id": tarea["_id"]},{"$set": {"reminder_1h_sent": True}})

# Ejecuta la verificación de tareas cada minuto
scheduler.add_job(verificar_tareas, 'interval', minutes=1)

@app.on_event("startup")
async def startup_event():
    if not scheduler.running:
        scheduler.start()
    else:
        print("El scheduler ya está en ejecución.")

@app.on_event("shutdown")
async def shutdown_event():
    if scheduler.running:
        scheduler.shutdown()

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
