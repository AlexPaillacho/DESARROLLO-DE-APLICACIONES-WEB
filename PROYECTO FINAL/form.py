# formulario de Producto

from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, SubmitField, IntegerField
from wtforms.validators import data_required, length, number_range


class productoForm(FlaskForm):
    nombre = StringField ('nombre del porducto', validators=[data_required(), length(min=2, max=200)])
    descripcion = StringField ('descripcion del producto', validators=[data_required(), length(min=10, max=500)])
    cantidad = DecimalField ('precio del producto', validators=[data_required(), number_range (min=0, places=0)])
    precio = DecimalField ('precio del producto', validators=[data_required(), number_range (min=0.00, places=2)])
    submit = SubmitField ('agregar producto')