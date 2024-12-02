from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session
from auth import create_access_token, verify_password, get_password_hash
from database import get_db
from models import User
from passlib.hash import bcrypt

router = APIRouter()

# Modelo para los datos del cuerpo de la solicitud
class UserCreate(BaseModel):
    email: EmailStr  # Valida que sea un email válido
    password: str

@router.post("/signup")
def signup(user: UserCreate, db: Session = Depends(get_db)):
    # Debugging: imprimir los datos recibidos
    print("Datos recibidos:", user.dict())

    # Verificar si el usuario ya existe
    user_exists = db.query(User).filter(User.email == user.email).first()
    if user_exists:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Crear un nuevo usuario
    hashed_password = bcrypt.hash(user.password)
    new_user = User(email=user.email, password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User created successfully", "user": {"id": new_user.id, "email": new_user.email}}

@router.post("/login")
def login(email: str, password: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    access_token = create_access_token({"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}