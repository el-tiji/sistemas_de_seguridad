from fastapi import FastAPI 
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi import Depends
import os
import uvicorn
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
from src.backend.routes.users import router as users_router
from src.backend.routes.controles import router as controles_router

  
app = FastAPI( 

    title="Proyecto sgsi", 

    version="0.1" 

) 

app.add_middleware(
    SessionMiddleware,
    secret_key="super-secret-key"
)

app.mount("/static", StaticFiles(directory="src/frontend/public"), name="static")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

#rutas
app.include_router(users_router)
app.include_router(controles_router)

@app.get("/")
def login():
    return FileResponse("src/frontend/views/login.html")

@app.get("/dashboard")
def dashboard():
    return FileResponse("src/frontend/views/dashboard.html")


if __name__ == "__main__":
    uvicorn.run("src.backend.main:app", host="0.0.0.0", port=8000, reload=True)