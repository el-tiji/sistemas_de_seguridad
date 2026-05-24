from fastapi import APIRouter, Form, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from sqlalchemy import text
from passlib.context import CryptContext
from fastapi import Request

from src.backend.config.db import get_db

# Rutas para la gestión de usuarios (registro y login)
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
        total_users = db.execute(text("""
            SELECT COUNT(*)
            FROM usuario
        """)).scalar()

        roles_validos = ["admin","empresa", "usuario","auditor"]

        # =========================================
        # ASIGNAR ROL
        # =========================================
        if total_users == 0:
            rol = "admin"
        else:
            rol = rol.lower().strip()

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
    request.session["email"] = result.email
    request.session["rol"] = result.rol
    return RedirectResponse(url="/dashboard", status_code=303)

@router.get("/logout")
def logout(request: Request):

    request.session.clear()

    return RedirectResponse(
        url="/",
        status_code=303
    )