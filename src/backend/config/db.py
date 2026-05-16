from sqlalchemy import create_engine,text

from sqlalchemy.orm import sessionmaker, declarative_base 

  
# Configuración de la conexión a la base de datos MySQL usando SQLAlchemy
DATABASE_URL = "mysql+pymysql://sgsi_user:sgsi_password@mysql:3306/sgsi"

  

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


if __name__ == "__main__":
    try:
        db = SessionLocal()
        print("✅ Conexión exitosa a MySQL")

        result = db.execute(text("""
            SHOW TABLES;
        """))

        print([row[0] for row in result])

        db.close()

    except Exception as e:
        print("❌ Error de conexión:", e)