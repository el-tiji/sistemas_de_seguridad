from fastapi import FastAPI 
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi import Depends
import os
from dotenv import load_dotenv
import uvicorn
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
from src.backend.routes.users import router as users_router
from src.backend.routes.controles import router as controles_router
from src.backend.routes.soa import router as soa_router 
from src.backend.routes.organizacion import router as organizacion_router

#configuracion de fastapi 
app = FastAPI( 

    title="Proyecto sgsi", 

    version="0.1" 

) 

app.add_middleware(
    SessionMiddleware,
    secret_key=os.getenv("SECRET_KEY")
)

app.mount("/static", StaticFiles(directory="src/frontend/public"), name="static")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

#rutas
app.include_router(users_router)
app.include_router(controles_router)
app.include_router(soa_router)
app.include_router(organizacion_router)

@app.get("/")
def login():
    return FileResponse("src/frontend/views/login.html")

@app.get("/crear-cuenta")
def crear_cuenta():
    return FileResponse("src/frontend/views/creacion-cuenta.html")

@app.get("/dashboard")
def dashboard():
    return FileResponse("src/frontend/views/dashboard.html")

@app.get("/controles")
def controles():
    return FileResponse("src/frontend/views/creacion-control.html")

@app.get("/soa")
def soa():
    return FileResponse("src/frontend/views/creacion-soa.html")

@app.get("/organizaciones")
def organizaciones():
    return FileResponse("src/frontend/views/organizaciones.html")


if __name__ == "__main__":
    uvicorn.run("src.backend.main:app", host="0.0.0.0", port=5000, reload=True)