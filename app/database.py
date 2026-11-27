import os

import psycopg2
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_NAME = os.getenv("DB_NAME", "clasificador_db")
DB_USER = os.getenv("DB_USER", "app_ia")
DB_PASSWORD = os.getenv("DB_PASSWORD", "password")
DB_PORT = os.getenv("DB_PORT", "5432")

def conectar_db():
    try:
        conexion = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            port=DB_PORT
        )
        return conexion
    except psycopg2.Error as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None

def guardar_historial(mensaje: str, motor: str, clasificacion: str):
    conexion = conectar_db()
    if not conexion:
        return False
    
    try:
        cursor = conexion.cursor()
        cursor.execute(
            """
            INSERT INTO historial_commits (mensaje, motor, clasificacion)
            VALUES (%s, %s, %s);
            """,
            (mensaje, motor, clasificacion)
        )
        conexion.commit()
        cursor.close()
        conexion.close()
        return True
    except psycopg2.Error as e:
        print(f"Error al guardar en la base de datos: {e}")
        if conexion:
            conexion.close()
        return False
def obtener_historial(limite: int = 20):
    conexion = conectar_db()
    if not conexion:
        return []

    try:
        cursor = conexion.cursor()
        cursor.execute(
            "SELECT * FROM historial_commits ORDER BY id DESC LIMIT %s;",
            (limite,),
        )
        filas = cursor.fetchall()
        columnas = [desc[0] for desc in cursor.description]
        cursor.close()
        conexion.close()
        return [dict(zip(columnas, fila)) for fila in filas]
    except psycopg2.Error as e:
        print(f"Error al consultar el historial: {e}")
        if conexion:
            conexion.close()
        return []
