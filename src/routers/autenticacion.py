from datetime import datetime, timedelta, timezone
from typing import Annotated
from db.schemas.schemas import user_schema
from bson import ObjectId
from db.db import db_users
from jose import jwt, JWTError
from fastapi import Depends, APIRouter, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from pydantic import BaseModel
from db.models.models import User, UserMostrar
from templates.templates import templates

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter()

SECRET_KEY = "mysecretkey"  # Cambia esto por una clave segura
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 525600

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = db_users.users_proyect.find_one({"username": username})
    if user is None:
        raise credentials_exception
    return User(**user)

@router.post("/register")
async def register(user: User):
    user_in_db = db_users.users_proyect.find_one({"username": user.username})
    if user_in_db:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    hashed_password = get_password_hash(user.password)
    user.password = hashed_password
    
    user_dict = user.dict()
    user_dict["_id"] = ObjectId()
    user_dict["role"] = "user"
    db_users.users_proyect.insert_one(user_dict)
    
    return {"msg": "User registered successfully"}

@router.post("/register/admin")
async def register_admin(user: User):
    user_in_db = db_users.users_proyect.find_one({"username": user.username})
    if user_in_db:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    hashed_password = get_password_hash(user.password)
    user.password = hashed_password
    
    user_dict = user.dict()
    user_dict["_id"] = ObjectId()
    user_dict["role"] = "admin"
    db_users.users_proyect.insert_one(user_dict)
    
    return {"msg": "User registered successfully"}

@router.post("/register/editor")
async def register_editor(user: User):
    user_in_db = db_users.users_proyect.find_one({"username": user.username})
    if user_in_db:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    hashed_password = get_password_hash(user.password)
    user.password = hashed_password
    
    user_dict = user.dict()
    user_dict["_id"] = ObjectId()
    user_dict["role"] = "editor"
    db_users.users_proyect.insert_one(user_dict)
    
    return {"msg": "User registered successfully"}

@router.post("/token", response_model=dict)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = db_users.users_proyect.find_one({"username": form_data.username})
    if not user or not verify_password(form_data.password, user["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["username"]}, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/users/me", response_model=UserMostrar)
async def read_users_me(current_user: UserMostrar = Depends(get_current_user)):
    user = current_user.dict()
    user_from_db = db_users.users_proyect.find_one({"username": current_user.username})
    if user_from_db:
        user["id"] = str(user_from_db["_id"])
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El usuario no funciona")
    return user