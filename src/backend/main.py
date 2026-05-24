from fastapi import FastAPI, Request 
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi import Depends
import os
import secrets
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

load_dotenv()

app.add_middleware(
    SessionMiddleware,
    secret_key=os.getenv("SECRET_KEY"),
    https_only=True
)

app.mount("/static", StaticFiles(directory="src/frontend/public"), name="static")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

#middleware de seguridad
@app.middleware("http")
async def security_headers(request, call_next):

    response = await call_next(request)

    response.headers["X-Frame-Options"] = "DENY"

    response.headers["X-Content-Type-Options"] = "nosniff"

    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"

    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; "
        "script-src 'self' 'unsafe-inline'; "
        "style-src 'self' 'unsafe-inline'; "
        "img-src 'self' data:; "
        "font-src 'self'; "
        "connect-src 'self'; "
        "frame-ancestors 'none'; "
        "base-uri 'self'; "
        "form-action 'self';"
    )

    response.headers["Strict-Transport-Security"] = (
        "max-age=31536000; includeSubDomains"
    )

    return response

#rutas
app.include_router(users_router)
app.include_router(controles_router)
app.include_router(soa_router)
app.include_router(organizacion_router)




@app.get("/")
def login(request: Request):

    csrf_token = secrets.token_hex(32)

    request.session["csrf_token"] = csrf_token

    response = FileResponse(
        "src/frontend/views/login.html"
    )

    response.set_cookie(
        key="csrf_token",
        value=csrf_token,
        httponly=True,
        secure=True,
        samesite="strict"
    )

    return response

@app.get("/crear-cuenta")
def crear_cuenta(request: Request):

    csrf_token = secrets.token_hex(32)

    request.session["csrf_token"] = csrf_token

    response = FileResponse(
        "src/frontend/views/creacion-cuenta.html"
    )

    response.set_cookie(
        key="csrf_token",
        value=csrf_token,
        httponly=True,
        secure=True,
        samesite="strict"
    )

    return response

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