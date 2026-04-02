from conexion.conexion import obtener_conexion

class ProductoService:

    @staticmethod
    def listar_todos():
        try:
            conexion = obtener_conexion()
            cursor = conexion.cursor(dictionary=True) # Para usar p.nombre en el HTML
            cursor.execute("SELECT * FROM inv_prd")
            productos = cursor.fetchall()
            cursor.close()
            conexion.close()
            return productos
        except Exception as e:
            print(f"Error al listar: {e}")
            return []
        

    @staticmethod
    def insertar(nombre, stock, categoria, tamano, peso):
        try:
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            
            # SQL usando los campos de tu tabla inv_prd
            # OJO: Si en phpMyAdmin tu columna tiene la ñ (tamaño), ponla con ñ aquí.
            sql = """INSERT INTO inv_prd (nombre, stock, categoria, tamaño, peso) 
                     VALUES (%s, %s, %s, %s, %s)"""
            
            valores = (nombre, stock, categoria, tamano, peso)
            
            cursor.execute(sql, valores)
            conexion.commit() # ¡ESTO ES LO QUE GUARDA LOS CAMBIOS EN XAMPP!
            
            cursor.close()
            conexion.close()
            return True
        except Exception as e:
            print(f"Error al insertar en MariaDB: {e}")
            return False
        
    # Añade esto a tu clase ProductoService
@staticmethod
def eliminar(sku):
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM inv_prd WHERE sku = %s", (sku,))
        conexion.commit()
        cursor.close()
        conexion.close()
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

@staticmethod
def obtener_por_sku(sku):
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("SELECT * FROM inv_prd WHERE sku = %s", (sku,))
    producto = cursor.fetchone()
    cursor.close()
    conexion.close()
    return producto