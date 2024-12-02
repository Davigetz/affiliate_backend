from fastapi import FastAPI
from routers import users, products
from fastapi.middleware.cors import CORSMiddleware

from database import Base, engine
from models import User, Product

# Crear las tablas en la base de datos
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:3000"],  # URLs permitidas (frontend)
    allow_credentials=True,
    allow_methods=["*"],  # Métodos permitidos (GET, POST, etc.)
    allow_headers=["*"],  # Encabezados permitidos
)

# Incluir rutas
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(products.router, prefix="/products", tags=["Products"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the Affiliate Platform!"}