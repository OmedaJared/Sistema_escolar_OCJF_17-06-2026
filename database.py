import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

# Configuración de MongoDB (Local o Atlas a través de variables de entorno)
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
DB_NAME = os.getenv("DB_NAME", "sistema_escolar_db")

try:
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    
    # Crear índices únicos para asegurar la consistencia de los datos
    db.alumnos.create_index("matricula", unique=True)
    db.maestros.create_index("num_empleado", unique=True)
    db.materias.create_index("codigo_materia", unique=True)
    
    print(f"Conexión exitosa a MongoDB. Base de datos: {DB_NAME}")
except Exception as e:
    print(f"Error al conectar a la base de datos: {e}")
    db = None

def get_db():
    return db
