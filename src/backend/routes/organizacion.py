from fastapi import APIRouter, Form, Depends, HTTPException, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from sqlalchemy import text
from fastapi import Request

from src.backend.config.db import get_db

router = APIRouter( 
    prefix="/organizaciones",
    tags=["Organizaciones"])

def validar_sesion(request: Request):

    user_id = request.session.get("user_id")

    if not user_id:
        raise HTTPException(
            status_code=401,
            detail="No autenticado"
        )

    return user_id

def validar_auditor(request: Request):

    validar_sesion(request)

    rol = request.session.get("rol")

    if rol != "auditor":
        raise HTTPException(
            status_code=403,
            detail="No autorizado"
        )

# =========================================
# CREAR ORGANIZACION
# =========================================
@router.post("/crear-organizacion")
def crear_organizacion(
    request: Request,
    nombre: str = Form(...),
    descripcion: str = Form(...),
    alcance_sgsi: str = Form(...),
    db: Session = Depends(get_db)
):

    validar_sesion(request)

    try:

        db.execute(text("""
            INSERT INTO organizacion (
                nombre,
                descripcion,
                alcance_sgsi
            )
            VALUES (
                :nombre,
                :descripcion,
                :alcance_sgsi
            )
        """), {
            "nombre": nombre,
            "descripcion": descripcion,
            "alcance_sgsi": alcance_sgsi
        })

        db.commit()

        return RedirectResponse(
            url="/dashboard",
            status_code=303
        )

    except Exception as e:
        db.rollback()

        raise HTTPException(
            status_code=500,
            detail=f"Error al crear organización: {str(e)}"
        )

# =========================================
# LISTAR ORGANIZACIONES
# =========================================
@router.get("/listar-organizaciones")
def listar_organizaciones(
    request: Request,
    db: Session = Depends(get_db)
):
    validar_sesion(request)

    try:

        result = db.execute(text("""
            SELECT
                id,
                nombre,
                descripcion,
                alcance_sgsi,
                fecha_creacion
            FROM organizacion
            ORDER BY id DESC
        """))

        rows = result.fetchall()

        return [
            {
                "id": r[0],
                "nombre": r[1],
                "descripcion": r[2],
                "alcance_sgsi": r[3],
                "fecha_creacion": str(r[4])
            }
            for r in rows
        ]

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Error al listar organizaciones: {str(e)}"
        )

# =========================================
# DETALLE ORGANIZACION
# =========================================
@router.get("/{organizacion_id}")
def obtener_organizacion(
    request: Request,
    organizacion_id: int,
    db: Session = Depends(get_db)
):
    validar_sesion(request)

    try:

        result = db.execute(text("""
            SELECT
                id,
                nombre,
                descripcion,
                alcance_sgsi,
                fecha_creacion
            FROM organizacion
            WHERE id = :id
        """), {
            "id": organizacion_id
        })

        row = result.fetchone()

        if not row:
            raise HTTPException(
                status_code=404,
                detail="Organización no encontrada"
            )

        return {
            "id": row[0],
            "nombre": row[1],
            "descripcion": row[2],
            "alcance_sgsi": row[3],
            "fecha_creacion": str(row[4])
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Error al obtener organización: {str(e)}"
        )