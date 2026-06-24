from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

# Configuración de MongoDB (Local o Atlas a través de variables de entorno)
MONGODB_USERNAME="j25759298_db_user"
MONGODB_PASSWORD="y6Kf7b33aj3jaadx"
MONGODB_URI="mongodb+srv://j25759298_db_user:y6Kf7b33aj3jaadx@cluster0.pgyhwyx.mongodb.net"

try:
    client = MongoClient(MONGODB_URI)
    db = client[MONGODB_USERNAME]
    
    # Crear índices únicos para asegurar la consistencia de los datos
    db.alumnos.create_index("matricula", unique=True)
    db.maestros.create_index("num_empleado", unique=True)
    db.materias.create_index("codigo_materia", unique=True)
    
    print(f"Conexión exitosa a MongoDB. Base de datos: {MONGODB_USERNAME}")
except Exception as e:
    print(f"Error al conectar a la base de datos: {e}")
    db = None

def get_db():
    return db

