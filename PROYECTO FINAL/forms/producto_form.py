from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DecimalField, SubmitField
from wtforms.validators import DataRequired

class productoForm(FlaskForm):
    # Añadimos el SKU, nombre del producto, categoria y stock como campo obligatorio
    sku = StringField('SKU / Código', validators=[DataRequired()])
    nombre = StringField('Nombre del Producto', validators=[DataRequired()])
    categoria = StringField('Categoría', validators=[DataRequired()])
    cantidad = IntegerField('Stock', validators=[DataRequired()])
    tamano = StringField('Tamaño')
    peso = DecimalField('Peso')
    submit = SubmitField('Guardar Producto')