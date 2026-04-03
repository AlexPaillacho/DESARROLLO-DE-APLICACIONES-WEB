from conexion.conexion import obtener_conexion

class AuthService:
    @staticmethod
    def login(username, password):
        conn = obtener_conexion()
        if conn:
            cursor = conn.cursor(dictionary=True)
            # Buscamos el usuario y la clave tal cual (luego puedes usar hash por seguridad)
            sql = "SELECT * FROM usuarios WHERE username = %s AND password = %s"
            cursor.execute(sql, (username, password))
            usuario = cursor.fetchone()
            cursor.close()
            conn.close()
            return usuario
        return None