from flask import Flask, render_template, redirect, url_for, flash, session, request
from services.producto_service import ProductoService
from services.auth_service import AuthService
from forms.producto_form import productoForm
import os
from fpdf import FPDF
from flask import make_response
from io import BytesIO


app = Flask(__name__)

# CONFIGURACIÓN CRÍTICA: La Secret Key permite usar session y flash
app.secret_key = 'panaderia_el_reventador_secret_key_2026'

# --- RUTAS DE AUTENTICACIÓN ---

@app.route('/login', methods=['GET', 'POST'])
def login():
    # Si ya está logueado, lo mandamos al index
    if 'username' in session:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        user = request.form.get('username')
        pasw = request.form.get('password')
        
        usuario_valido = AuthService.login(user, pasw)
        
        if usuario_valido:
            # Guardamos los datos en la sesión del navegador
            session['user_id'] = usuario_valido['id']
            session['username'] = usuario_valido['username']
            session['nombre_completo'] = usuario_valido['nombre_completo']
            flash(f"Bienvenido al sistema, {usuario_valido['nombre_completo']}")
            return redirect(url_for('index'))
        else:
            flash("Error: Usuario o contraseña incorrectos")
            
    return render_template("auth/login.html")

@app.route('/logout')
def logout():
    session.clear() # Limpia toda la sesión
    flash("Has cerrado sesión correctamente")
    return redirect(url_for('login'))


# --- RUTAS DEL INVENTARIO (TODAS PROTEGIDAS) ---

@app.route('/')
def index():
    if 'username' not in session:
        return redirect(url_for('login'))
        
    productos = ProductoService.listar_todos()
    return render_template("productos/index.html", productos=productos)


@app.route('/productos/nuevo', methods=['GET', 'POST'])
def producto_nuevo():
    if 'username' not in session:
        return redirect(url_for('login'))
        
    form = productoForm()
    if form.validate_on_submit():
        if ProductoService.insertar(
            form.sku.data, 
            form.nombre.data, 
            form.cantidad.data, 
            form.categoria.data, 
            form.tamano.data, 
            form.peso.data
        ):
            flash('¡Producto guardado con éxito!')
            return redirect(url_for('index'))
    
    return render_template("productos/producto_form.html", form=form, titulo="Nuevo Producto")


@app.route('/productos/editar/<string:sku>', methods=['GET', 'POST'])
def producto_editar(sku):
    if 'username' not in session:
        return redirect(url_for('login'))
        
    producto_data = ProductoService.obtener_por_sku(sku)
    if not producto_data:
        flash('Producto no encontrado')
        return redirect(url_for('index'))

    # Pre-rellenamos el formulario con los datos de la DB
    form = productoForm(data=producto_data)
    
    if form.validate_on_submit():
        if ProductoService.actualizar(
            sku, 
            form.nombre.data, 
            form.cantidad.data, 
            form.categoria.data, 
            form.tamano.data, 
            form.peso.data
        ):
            flash('¡Producto actualizado correctamente!')
            return redirect(url_for('index'))
            
    return render_template("productos/producto_form.html", form=form, titulo="Editar Producto")


@app.route('/productos/eliminar/<string:sku>')
def producto_eliminar(sku):
    if 'username' not in session:
        return redirect(url_for('login'))
        
    if ProductoService.eliminar(sku):
        flash('Producto eliminado con éxito')
    else:
        flash('Error al eliminar el producto')
    return redirect(url_for('index'))


@app.route('/productos/reporte')
def generar_reporte():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    
    productos = ProductoService.listar_todos()
    
    from fpdf import FPDF
    pdf = FPDF()
    pdf.add_page()
    
    # --- Configuración del PDF ---
    pdf.set_font("Arial", "B", 16)
    pdf.cell(190, 10, "INVENTARIO - PANADERIA EL REVENTADOR", ln=True, align="C")
    pdf.ln(10)
    
    # Cabeceras
    pdf.set_font("Arial", "B", 11)
    pdf.cell(30, 10, "SKU", 1)
    pdf.cell(80, 10, "Producto", 1)
    pdf.cell(30, 10, "Stock", 1)
    pdf.cell(50, 10, "Categoria", 1)
    pdf.ln()
    
    # Datos
    pdf.set_font("Arial", "", 10)
    for p in productos:
        # Reemplazamos caracteres problemáticos para latin-1
        nombre = str(p.get('producto', 'S/N')).encode('latin-1', 'replace').decode('latin-1')
        categoria = str(p.get('categoria', 'S/N')).encode('latin-1', 'replace').decode('latin-1')
        
        pdf.cell(30, 10, str(p['sku']), 1)
        pdf.cell(80, 10, nombre, 1)
        pdf.cell(30, 10, str(p['stock']), 1)
        pdf.cell(50, 10, categoria, 1)
        pdf.ln()
    
    # --- LA SOLUCIÓN DEFINITIVA ---
    # 1. Generamos el output como bytes
    pdf_output = pdf.output()
    
    # 2. Si fpdf2 devuelve un bytearray o bytes, lo envolvemos en BytesIO
    buffer = BytesIO(pdf_output)
    
    # 3. Creamos la respuesta enviando el valor del buffer
    response = make_response(buffer.getvalue())
    response.headers.set('Content-Disposition', 'attachment', filename='reporte_inventario.pdf')
    response.headers.set('Content-Type', 'application/pdf')
    
    return response

if __name__ == '__main__':
    app.run(debug=True, port=5000)