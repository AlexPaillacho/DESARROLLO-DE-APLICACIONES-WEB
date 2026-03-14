# formulario de Producto

from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, SubmitField, IntegerField
from wtforms.validators import data_required, length, number_range


class productoForm(FlaskForm):
    nombre = StringField ('nombre del porducto', validators=[data_required(), length(min=2, max=200)])
    descripcion = StringField ('descripcion del producto', validators=[data_required(), length(min=2, max=500)])
    cantidad = DecimalField ('cantidad del producto', places=0 ,validators=[data_required(), number_range (min=0.00)])
    precio = DecimalField ('precio del producto', places=2, validators=[data_required(), number_range (min=0.00)])
    submit = SubmitField ('agregar producto')