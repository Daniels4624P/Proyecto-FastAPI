from pymongo import MongoClient

URL_CONNECTION = "mongodb+srv://user:Gravityfalls@taskmanager.hcvxo.mongodb.net/?retryWrites=true&w=majority&appName=TaskManager"

client = MongoClient(URL_CONNECTION)

db_tasks = client.tasks_proyect_task_manager
db_users = client.users_proyect_task_manager