from fastapi import APIRouter, Form, Depends, HTTPException
from fastapi.responses import RedirectResponse
from httpcore import request
from sqlalchemy.orm import Session
from sqlalchemy import text
from passlib.context import CryptContext
from fastapi import Request

from src.backend.config.db import get_db

router = APIRouter()

@router.post("/crear-control")
def registar_control(
    request: Request,
    codigo: str = Form(...), 
    descripcion: str = Form(...), 
    estado: str = Form(...),
    db: Session = Depends(get_db)
):
    user_id = request.session.get("user_id")
    if not user_id:
        raise HTTPException(status_code=401, detail="No autenticado")

    try:
        db.execute(text("""
            INSERT INTO controles (codigo, descripcion, estado) VALUES (:codigo, :descripcion, :estado)
        """), {"codigo": codigo, "descripcion": descripcion, "estado": estado})
        db.commit()
        return RedirectResponse(url="/dashboard", status_code=303)
    except Exception as e:
        raise HTTPException(status_code=400, detail="Error al crear el control")