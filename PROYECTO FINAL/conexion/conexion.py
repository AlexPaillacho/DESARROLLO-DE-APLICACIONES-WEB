import mysql.connector

def obtener_conexion():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="", # colocar la contraseña
        database="inventario" # Nombre de mi base de datos de phpmyadmin
    )