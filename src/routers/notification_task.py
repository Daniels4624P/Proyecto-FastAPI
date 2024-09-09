import asyncio
from datetime import datetime, timedelta
from db.db import db_tasks, db_users
from email_service import send_email

async def check_tasks_one_day():
    while True:
        now =  datetime.now()
        soon_expiry = now + timedelta(days=1)

        tasks = db_tasks.tasks.find({"date_expire": {"$lte":soon_expiry.isoformat()}, "state": "pendiente"})

        for tarea in tasks:
            user = db_users.users_proyect.find_one({"username": tarea["owner"]})
            if user:
                await send_email(user["email"], "Tarea a punto de vencer", f'Tu tarea: {tarea["task"]} se vence en un dia, completala pronto')

        await asyncio.sleep(60)

async def check_tasks_one_hour():
    while True:
        now = datetime.now()
        soon_expiry = now + timedelta(hours=1)

        tasks = db_tasks.tasks.find({"date_expire": {"$lte": soon_expiry.isoformat()}, "state": "pendiente"})

        for tarea in tasks:
            user = db_users.users_proyect.find_one({"username": tarea["owner"]})
            if user:
                await send_email(user["email"], "Tarea a punto de vencer", f'Tu tarea: {tarea["task"]} se vence en una hora, completala pronto')

        await asyncio.sleep(60)