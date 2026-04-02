import mysql.connector

def obtener_conexion():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="", # Vacío como confirmamos
        database="inventario" # Nombre que veo en tu phpMyAdmin
    )