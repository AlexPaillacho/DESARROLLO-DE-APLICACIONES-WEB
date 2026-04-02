from flask import Flask, render_template, request, redirect, url_for, flash, make_response
from services.producto_service import ProductoService
from forms.producto_form import productoForm 
from fpdf import FPDF

app = Flask(__name__)
app.secret_key = 'uea_clave_secreta_el_reventador'

# 1. RUTA INICIO: LISTAR (Punto 4 CRUD)
@app.route('/')
def index():
    productos_db = ProductoService.listar_todos()
    return render_template('productos/productos.html', productos=productos_db)

# 2. RUTA NUEVO: INSERTAR (Punto 4 CRUD)
@app.route('/productos/nuevo', methods=['GET', 'POST'])
def producto_nuevo():
    form = productoForm()
    if form.validate_on_submit():
        if ProductoService.insertar(form.nombre.data, form.cantidad.data, 
                                    form.categoria.data, form.tamano.data, form.peso.data):
            flash('¡Producto guardado con éxito!')
            return redirect(url_for('index'))
    return render_template("productos/producto_form.html", form=form, titulo="Nuevo Producto")

# 3. RUTA EDITAR: BUSCAR POR SKU (Punto 4 CRUD)
@app.route('/productos/editar/<int:sku>', methods=['GET', 'POST'])
def producto_editar(sku):
    producto_data = ProductoService.obtener_por_sku(sku)
    form = productoForm(data=producto_data)
    
    if form.validate_on_submit():
        # Aquí llamamos al servicio para hacer el UPDATE en la base de datos
        # (Asegúrate de tener el método .actualizar en tu ProductoService)
        if ProductoService.actualizar(sku, form.nombre.data, form.cantidad.data, form.categoria.data):
            flash('¡Producto actualizado con éxito!')
            return redirect(url_for('index'))
            
    return render_template("productos/producto_form.html", form=form, titulo="Editar Producto")

# 4. RUTA ELIMINAR (Punto 4 CRUD)
@app.route('/productos/eliminar/<int:sku>')
def producto_eliminar(sku):
    if ProductoService.eliminar(sku):
        flash('¡Producto eliminado correctamente!')
    else:
        flash('Error al eliminar.')
    return redirect(url_for('index'))

# 5. RUTA REPORTE PDF (Punto 6 Rúbrica)
@app.route('/reporte/pdf')
def generar_pdf():
    productos = ProductoService.listar_todos()
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(190, 10, "Reporte de Inventario - El Reventador", ln=True, align='C')
    pdf.ln(10)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(30, 10, "SKU", 1)
    pdf.cell(80, 10, "Nombre", 1)
    pdf.cell(40, 10, "Stock", 1)
    pdf.ln()
    pdf.set_font("Arial", '', 10)
    for p in productos:
        pdf.cell(30, 10, str(p['sku']), 1)
        pdf.cell(80, 10, p['nombre'], 1)
        pdf.cell(40, 10, str(p['stock']), 1)
        pdf.ln()
    response = make_response(pdf.output(dest='S').encode('latin-1'))
    response.headers.set('Content-Type', 'application/pdf')
    response.headers.set('Content-Disposition', 'attachment', filename='reporte.pdf')
    return response

# 6. RUTA ACERCADE
@app.route('/acercade')
def about():
    return render_template('about.html')

# FINAL: ENCENDIDO
if __name__ == '__main__':
    app.run(debug=True)