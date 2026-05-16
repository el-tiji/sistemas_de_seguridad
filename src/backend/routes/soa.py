from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text

from src.backend.config.db import get_db

router = APIRouter(prefix="/soa", tags=["SoA"])

# Rutas para la gestión de SoA (Declaración de Aplicabilidad)
@router.post("/generate")
def generate_soa(db: Session = Depends(get_db)):

    try:
        # 1️⃣ Obtener controles existentes
        controls = db.execute(text("SELECT id FROM control")).fetchall()

        if not controls:
            raise HTTPException(
                status_code=400,
                detail="No existen controles para generar el SoA"
            )

        # 2️⃣ Obtener última versión
        last_version = db.execute(
            text("SELECT MAX(version) FROM soa")
        ).scalar()

        if last_version is None:
            new_version = 1
        else:
            new_version = last_version + 1

        # 3️⃣ Crear nueva cabecera SoA
        db.execute(
            text("""
                INSERT INTO soa (version)
                VALUES (:version)
            """),
            {"version": new_version}
        )

        db.commit()

        # Obtener el id del SoA recién creado
        soa_id = db.execute(text("SELECT LAST_INSERT_ID()")).scalar()

        # 4️⃣ Insertar detalles
        for control in controls:
            db.execute(
                text("""
                    INSERT INTO soa_detalle (soa_id, control_id, incluido, justificacion)
                    VALUES (:soa_id, :control_id, :incluido, :justificacion)
                """),
                {
                    "soa_id": soa_id,
                    "control_id": control[0],
                    "incluido": True,
                    "justificacion": "Evaluado y aprobado en esta versión"
                }
            )

        db.commit()

        return {
            "message": "SoA generada correctamente",
            "version": new_version,
            "total_controles": len(controls)
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Error al generar SoA: {str(e)}"
        )

@router.get("/list-soa")
def listar_soa(db: Session = Depends(get_db)):

    result = db.execute(text("""
        SELECT id, version, fecha
        FROM soa
        ORDER BY version DESC
    """))

    soa_list = result.fetchall()

    return [
        {
            "id": s[0],
            "version": s[1],
            "fecha": str(s[2])
        }
        for s in soa_list
    ]

@router.get("/detail/{soa_id}")
def detalle_soa(soa_id: int, db: Session = Depends(get_db)):

    result = db.execute(text("""
        SELECT c.codigo, c.descripcion, sd.incluido, sd.justificacion
        FROM soa_detalle sd
        JOIN control c ON sd.control_id = c.id
        WHERE sd.soa_id = :soa_id
    """), {"soa_id": soa_id})

    rows = result.fetchall()

    return [
        {
            "codigo": r[0],
            "descripcion": r[1],
            "incluido": r[2],
            "justificacion": r[3]
        }
        for r in rows
    ]