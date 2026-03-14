from flask import Flask, render_template, url_for, request, redirect, flash

from form import productoForm
 
app = Flask(__name__)

app.config['SECRET_KEY'] = 'MI_CLAVE_SECRETA'

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/Page2/<LandPage>')
def Page2(LandPage):
    return f'Bienvenido necesitas una, {LandPage}!'

@app.route('/Page3/<CorporacPage>')
def Page3(CorporacPage):
    return f'Bienvenido a la pagina para tu empresa, {CorporacPage}!'

#ruta de productos
@app.route('/productos/nuevo', methods =['GET', 'POST'])
def producto_nuevo():
    form=productoForm()
    if form.validate_on_submit():
        nombre = form.nombre.data
        descripcion = form.descripcion.data
        cantidad = form.cantidad.data
        precio = form.cantidad.data
        
        flash(' Producto agregado exitosamente')

        return redirect(url_for("inico"))
    return render_template("producto_form.html", form=form)


if __name__ == "__main__":
    app.run(debug=True)
