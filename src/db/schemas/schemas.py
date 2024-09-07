def task_schema(task) -> dict:
    return {"id": str(task["_id"]),
            "task": task["task"],
            "description": task["description"],
            "date_expire": task["date_expire"],
            "state": task["state"],
            "owner": task["owner"]}

def tasks_schema(tasks) ->list:
    return [task_schema(user) for user in tasks]

def user_schema(user):
    return {
        "id": str(user["_id"]),
        "username": user["username"],
        "email": user["email"],
        "password": user["password"],
        "role": user["role"]
    }
def users_schema(users):
    return [user_schema(user) for user in users]