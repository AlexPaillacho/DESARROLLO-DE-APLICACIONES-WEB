from flask import Flask, render_template, redirect, url_for, flash, session, request, make_response
from services.producto_service import ProductoService
from services.auth_service import AuthService
from forms.producto_form import productoForm
from flask import Flask, render_template, redirect, url_for, flash, session, request, make_response
from io import BytesIO # <--- Asegúrate de tener esta línea arriba en tus imports
from fpdf import FPDF
import os




app = Flask(__name__)
app.secret_key = 'logic_servis_2026_full_key'

# --- 1. SEGURIDAD (LOGIN/LOGOUT) ---

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'username' in session:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        user = request.form.get('username')
        pasw = request.form.get('password')
        usuario_valido = AuthService.login(user, pasw)
        
        if usuario_valido:
            session['user_id'] = usuario_valido['id']
            session['username'] = usuario_valido['username']
            session['nombre_completo'] = usuario_valido['nombre_completo']
            return redirect(url_for('index'))
        else:
            flash("Usuario o contraseña incorrectos", "danger")
            
    return render_template("auth/login.html")

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# --- 2. RUTAS PRINCIPALES ---

@app.route('/')
def index():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    productos = ProductoService.listar_todos()
    # Apuntamos a la subcarpeta 'productos' como tienes en VS Code
    return render_template('productos/index.html', productos=productos)

@app.route('/inicio')
def inicio():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('inicio.html')

# --- 3. GESTIÓN DE PRODUCTOS (NUEVO, EDITAR, ELIMINAR) ---

@app.route('/productos/nuevo', methods=['GET', 'POST'])
def producto_nuevo():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    form = productoForm()
    if form.validate_on_submit():
        if ProductoService.insertar(form.sku.data, form.nombre.data, form.cantidad.data, 
                                    form.categoria.data, form.tamano.data, form.peso.data):
            flash('¡Producto guardado!', "success")
            return redirect(url_for('index'))
    
    return render_template("productos/producto_form.html", form=form, titulo="Nuevo Producto")

@app.route('/productos/editar/<string:sku>', methods=['GET', 'POST'])
def producto_editar(sku):
    if 'username' not in session:
        return redirect(url_for('login'))
    
    # Obtenemos los datos actuales del producto
    producto_data = ProductoService.obtener_por_sku(sku)
    form = productoForm(data=producto_data)
    
    if form.validate_on_submit():
        if ProductoService.actualizar(sku, form.nombre.data, form.cantidad.data, 
                                      form.categoria.data, form.tamano.data, form.peso.data):
            flash('Producto actualizado correctamente', "success")
            return redirect(url_for('index'))
            
    return render_template("productos/producto_form.html", form=form, titulo="Editar Producto")

@app.route('/productos/eliminar/<string:sku>')
def producto_eliminar(sku):
    if 'username' not in session:
        return redirect(url_for('login'))
    
    ProductoService.eliminar(sku)
    flash("Producto eliminado", "warning")
    return redirect(url_for('index'))

# --- 4. REPORTES ---



@app.route('/productos/reporte')
def generar_reporte():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    try:
        productos = ProductoService.listar_todos()
        pdf = FPDF()
        pdf.add_page()
        
        # Título
        pdf.set_font("Arial", "B", 16)
        # Usamos latin-1 para evitar que tildes o la ñ rompan el PDF
        pdf.cell(190, 10, "LOGIC SERVIS - REPORTE DE ACTIVOS".encode('latin-1', 'replace').decode('latin-1'), ln=True, align="C")
        pdf.ln(10)
        
        # Tabla: Encabezados
        pdf.set_font("Arial", "B", 12)
        pdf.cell(30, 10, "SKU", 1)
        pdf.cell(100, 10, "Producto", 1)
        pdf.cell(30, 10, "Stock", 1)
        pdf.ln()
        
        # Tabla: Contenido
        pdf.set_font("Arial", "", 10)
        for p in productos:
            # Obtenemos nombre y stock de forma segura
            nombre = str(p.get('producto', p.get('nombre', 'S/N')))
            stock = str(p.get('stock', p.get('cantidad', 0)))
            
            # Limpiamos el texto para FPDF
            nombre_fpdf = nombre.encode('latin-1', 'replace').decode('latin-1')
            
            pdf.cell(30, 10, str(p['sku']), 1)
            pdf.cell(100, 10, nombre_fpdf, 1)
            pdf.cell(30, 10, stock, 1)
            pdf.ln()
        
        # OBTENCIÓN DE DATOS BINARIOS
        # En Python 3.10+, dest='S' devuelve un bytearray directamente
        pdf_output = pdf.output(dest='S')
        
        # Creamos la respuesta enviando los bytes directamente
        response = make_response(bytes(pdf_output)) 
        response.headers.set('Content-Type', 'application/pdf')
        response.headers.set('Content-Disposition', 'attachment', filename='reporte_logic_servis.pdf')
        
        return response

    except Exception as e:
        flash(f"Error técnico en PDF: {str(e)}", "danger")
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)