from fastapi import APIRouter, Form, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from sqlalchemy import text
from passlib.context import CryptContext
from fastapi import Request

from src.backend.config.db import get_db

router = APIRouter()
pwd_context = CryptContext(schemes=["pbkdf2_sha256"],deprecated="auto")

@router.post("/register")
def register(
    email: str = Form(...), 
    password: str = Form(...),
    rol: str = Form(...), 
    db: Session = Depends(get_db)
):
    hashed_password = pwd_context.hash(password)

    try:
        db.execute(text("""
            INSERT INTO usuario (email, password, rol) VALUES (:email, :password, :rol)
        """), {"email": email, "password": hashed_password, "rol": rol})
        db.commit()
        return RedirectResponse(url="/", status_code=303)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login")
def login(
    request: Request,
    email: str = Form(...), 
    password: str = Form(...), 
    db: Session = Depends(get_db)
):
    result = db.execute(text("""
        SELECT * FROM usuario WHERE email = :email
    """), {"email": email}).fetchone()

    if not result or not pwd_context.verify(password, result.password):
        raise HTTPException(status_code=400, detail="Credenciales inválidas")

    request.session["user_id"] = result.id
    return RedirectResponse(url="/dashboard", status_code=303)