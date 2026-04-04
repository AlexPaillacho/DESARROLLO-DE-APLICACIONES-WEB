from werkzeug.security import check_password_hash
# Cambiamos esto para importar la función directamente
from conexion.conexion import obtener_conexion 

class AuthService:
    @staticmethod
    def login(username_ingresado, password_ingresada):
        try:
            # Usamos la función que definiste en conexion.py
            db = obtener_conexion() 
            cursor = db.cursor(dictionary=True)

            sql = "SELECT id, username, password, nombre_completo FROM usuarios WHERE username = %s"
            cursor.execute(sql, (username_ingresado,))
            usuario_db = cursor.fetchone()

            cursor.close()
            db.close()

            if usuario_db:
                # Comparamos la clave con el Hash de la base de datos
                if check_password_hash(usuario_db['password'], password_ingresada):
                    return usuario_db 
            
            return None 

        except Exception as e:
            print(f"Error en AuthService: {e}")
            return None