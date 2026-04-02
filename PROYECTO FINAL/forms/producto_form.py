from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, SubmitField, IntegerField
from wtforms.validators import DataRequired

class productoForm(FlaskForm):
    # Usamos los nombres que pide tu base de datos
    nombre = StringField('Nombre del Producto', validators=[DataRequired()])
    categoria = StringField('Categoría', validators=[DataRequired()])
    cantidad = IntegerField('Stock Inicial', validators=[DataRequired()])
    tamano = DecimalField('Tamaño (Altura)', places=2)
    peso = DecimalField('Peso (kg)', places=2)
    submit = SubmitField('Agregar producto')