# db.py
import mysql.connector
from mysql.connector import Error

def get_connection():
    try:
        return mysql.connector.connect(
            host="localhost",   # o "localhost"
            port=3306,          # el puerto va por separado
            user="root",
            password="root",
            database="empleados_db"
        )
    except Error as e:
        # Lanza con mensaje claro para que lo veas en la GUI
        raise RuntimeError(f"No se pudo conectar a MySQL: {e}")
