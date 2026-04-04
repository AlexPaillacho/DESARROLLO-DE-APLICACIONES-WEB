from conexion.conexion import obtener_conexion

class ProductoService:
    
    @staticmethod
    def listar_todos():
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)
        
        # SQL Limpio: id_prd con ruc y prod_empl con usuario
        sql = """
            SELECT 
                p.sku, 
                p.nombre AS producto, 
                p.stock, 
                p.categoria,
                IFNULL(c.nombre, 'Sin Cliente') AS cliente_nombre, 
                IFNULL(e.nombre, 'No asignado') AS empleado_nombre
            FROM inv_prd p
            LEFT JOIN inv_cliente c ON p.id_prd = c.ruc
            LEFT JOIN inv_empl e ON p.prod_empl = e.usuario
        """
        
        cursor.execute(sql)
        productos = cursor.fetchall()
        cursor.close()
        conexion.close()
        return productos

    @staticmethod
    def insertar(sku, nombre, stock, categoria, tamaño, peso, id_prd=None, prod_empl=None):
        conn = obtener_conexion()
        if conn:
            try:
                cursor = conn.cursor()
                # Limpieza de datos antes de insertar
                val_tamaño = tamaño if tamaño else "N/A"
                val_peso = peso if peso else 0.0
                val_stock = stock if stock else 0
                
                # Insertamos vinculando las llaves foráneas id_prd y prod_empl
                sql = """INSERT INTO inv_prd (sku, nombre, stock, categoria, tamaño, peso, id_prd, prod_empl) 
                         VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
                cursor.execute(sql, (sku, nombre, val_stock, categoria, val_tamaño, val_peso, id_prd, prod_empl))
                conn.commit()
                cursor.close()
                return True
            except Exception as e:
                print(f"Error al insertar: {e}")
            finally:
                conn.close()
        return False

    @staticmethod
    def actualizar(sku, nombre, stock, categoria, tamaño, peso, id_prd=None, prod_empl=None):
        conn = obtener_conexion()
        if conn:
            try:
                cursor = conn.cursor()
                val_tamaño = tamaño if tamaño else "N/A"
                val_peso = peso if peso else 0.0
                
                # Actualizamos también las relaciones por si cambiaron de dueño o cliente
                sql = """UPDATE inv_prd 
                         SET nombre=%s, stock=%s, categoria=%s, tamaño=%s, peso=%s, id_prd=%s, prod_empl=%s 
                         WHERE sku=%s"""
                cursor.execute(sql, (nombre, stock, categoria, val_tamaño, val_peso, id_prd, prod_empl, sku))
                conn.commit()
                cursor.close()
                return True
            except Exception as e:
                print(f"Error al actualizar: {e}")
            finally:
                conn.close()
        return False

    @staticmethod
    def eliminar(sku):
        conn = obtener_conexion()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM inv_prd WHERE sku = %s", (sku,))
                conn.commit()
                cursor.close()
                return True
            except Exception as e:
                print(f"Error al eliminar: {e}")
            finally:
                conn.close()
        return False

    @staticmethod
    def obtener_por_sku(sku):
        conn = obtener_conexion()
        if conn:
            try:
                cursor = conn.cursor(dictionary=True)
                # Usamos * para traer todos los campos, incluyendo id_prd y prod_empl
                cursor.execute("SELECT * FROM inv_prd WHERE sku = %s", (sku,))
                producto = cursor.fetchone()
                cursor.close()
                return producto
            finally:
                conn.close()
        return None