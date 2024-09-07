from pydantic import BaseModel, Field, validator
from datetime import datetime

TASK_STATES = ["pendiente", "en progreso", "completada"]

class User(BaseModel):
    id: str | None = None
    username: str
    email: str
    password: str
    role: str | None = None

class UserMostrar(BaseModel):
    id: str | None = None
    username: str
    email: str
    role: str | None = None

class Task(BaseModel):
    id: str| None = None
    task: str
    description: str
    date_expire: datetime
    state: str
    owner: str| None = None

    @validator("state")
    def validate_state(cls, value):
        if value not in TASK_STATES:
            raise ValueError(f"El estado debe ser uno de los siguientes: {', '.join(TASK_STATES)}")
        return value