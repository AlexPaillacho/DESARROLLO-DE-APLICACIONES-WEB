from werkzeug.security import check_password_hash

from conexion.conexion import obtener_conexion 

class AuthService:
    @staticmethod
    def login(username_ingresado, password_ingresada):
        try:
            
            db = obtener_conexion() 
            cursor = db.cursor(dictionary=True)

            sql = "SELECT id, username, password, nombre_completo FROM usuarios WHERE username = %s"
            cursor.execute(sql, (username_ingresado,))
            usuario_db = cursor.fetchone()

            cursor.close()
            db.close()

            if usuario_db:
                
                if check_password_hash(usuario_db['password'], password_ingresada):
                    return usuario_db 
            
            return None 

        except Exception as e:
            print(f"Error en AuthService: {e}")
            return None