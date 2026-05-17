from fastapi import APIRouter, Form, Depends, HTTPException, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from sqlalchemy import text

from src.backend.config.db import get_db

router = APIRouter(prefix="/api/control",
    tags=["Control"])

# =========================================
# CREAR CONTROL
# =========================================
@router.post("/crear-control")
def crear_control(
    request: Request,
    codigo: str = Form(...),
    descripcion: str = Form(...),
    estado: str = Form(...),
    db: Session = Depends(get_db)
):

    # Validar sesión
    user_id = request.session.get("user_id")

    if not user_id:
        raise HTTPException(
            status_code=401,
            detail="No autenticado"
        )

    try:

        # Validar si el control ya existe
        existe = db.execute(
            text("""
                SELECT id
                FROM control
                WHERE codigo = :codigo
            """),
            {"codigo": codigo}
        ).fetchone()

        if existe:
            raise HTTPException(
                status_code=400,
                detail="El control ya existe"
            )

        # Insertar control
        db.execute(
            text("""
                INSERT INTO control (
                    codigo,
                    descripcion,
                    estado
                )
                VALUES (
                    :codigo,
                    :descripcion,
                    :estado
                )
            """),
            {
                "codigo": codigo,
                "descripcion": descripcion,
                "estado": estado
            }
        )

        db.commit()

        return {
            "message": "Control creado correctamente"
        }

    except HTTPException:
        raise

    except Exception as e:

        db.rollback()

        raise HTTPException(
            status_code=500,
            detail=f"Error al crear control: {str(e)}"
        )

# =========================================
# LISTAR CONTROLES
# =========================================
@router.get("/listar-controles")
def listar_controles(
    db: Session = Depends(get_db)
):

    try:

        result = db.execute(text("""
            SELECT
                id,
                codigo,
                descripcion,
                estado
            FROM control
            ORDER BY codigo ASC
        """))

        controles = result.fetchall()

        return [
            {
                "id": c[0],
                "codigo": c[1],
                "descripcion": c[2],
                "estado": c[3]
            }
            for c in controles
        ]

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Error al listar controles: {str(e)}"
        )

# =========================================
# OBTENER CONTROL POR ID
# =========================================
@router.get("/{control_id}")
def obtener_control(
    control_id: int,
    db: Session = Depends(get_db)
):

    result = db.execute(
        text("""
            SELECT
                id,
                codigo,
                descripcion,
                estado
            FROM control
            WHERE id = :id
        """),
        {"id": control_id}
    ).fetchone()

    if not result:
        raise HTTPException(
            status_code=404,
            detail="Control no encontrado"
        )

    return {
        "id": result[0],
        "codigo": result[1],
        "descripcion": result[2],
        "estado": result[3]
    }

# =========================================
# ACTUALIZAR CONTROL
# =========================================
@router.put("/actualizar/{control_id}")
def actualizar_control(
    control_id: int,
    codigo: str = Form(...),
    descripcion: str = Form(...),
    estado: str = Form(...),
    db: Session = Depends(get_db)
):

    try:

        existe = db.execute(
            text("""
                SELECT id
                FROM control
                WHERE id = :id
            """),
            {"id": control_id}
        ).fetchone()

        if not existe:
            raise HTTPException(
                status_code=404,
                detail="Control no encontrado"
            )

        db.execute(
            text("""
                UPDATE control
                SET
                    codigo = :codigo,
                    descripcion = :descripcion,
                    estado = :estado
                WHERE id = :id
            """),
            {
                "id": control_id,
                "codigo": codigo,
                "descripcion": descripcion,
                "estado": estado
            }
        )

        db.commit()

        return {
            "message": "Control actualizado correctamente"
        }

    except HTTPException:
        raise

    except Exception as e:

        db.rollback()

        raise HTTPException(
            status_code=500,
            detail=f"Error al actualizar control: {str(e)}"
        )

# =========================================
# ELIMINAR CONTROL
# =========================================
@router.delete("/eliminar/{control_id}")
def eliminar_control(
    control_id: int,
    db: Session = Depends(get_db)
):

    try:

        existe = db.execute(
            text("""
                SELECT id
                FROM control
                WHERE id = :id
            """),
            {"id": control_id}
        ).fetchone()

        if not existe:
            raise HTTPException(
                status_code=404,
                detail="Control no encontrado"
            )

        db.execute(
            text("""
                DELETE FROM control
                WHERE id = :id
            """),
            {"id": control_id}
        )

        db.commit()

        return {
            "message": "Control eliminado correctamente"
        }

    except HTTPException:
        raise

    except Exception as e:

        db.rollback()

        raise HTTPException(
            status_code=500,
            detail=f"Error al eliminar control: {str(e)}"
        )