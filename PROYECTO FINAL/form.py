# formulario de Producto

from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, SubmitField, IntegerField
from wtforms.validators import data_required, length, number_range


class productoForm(FlaskForm):
    nombre = StringField
    descripcion = StringField ('descripcion del producto', validators=[data_required(), length(min=10, max=500)])
    precio = DecimalField ('precio del producto', validators=[data_required(), length(min=10, max=500)])
    submit = SubmitField ('agregar producto')