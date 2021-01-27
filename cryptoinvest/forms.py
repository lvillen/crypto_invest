from flask_wtf import FlaskForm
from wtforms import FloatField, SubmitField, SelectField 
from wtforms.validators import DataRequired
from cryptoinvest.data.cryptos import *

class PurchaseForm(FlaskForm):
    from_currency = SelectField('FromMoneda', choices=cryptos_disponibles(), validators=[DataRequired()]) 
    from_quantity = FloatField('FromCantidad', validators=[DataRequired()])
    to_currency = SelectField('ToMoneda', choices=cryptos(), validators=[DataRequired()])
    to_quantity = FloatField('ToCantidad', validators=[DataRequired()])
    price_unit = FloatField('Precio por unidad', validators=[DataRequired()])

    calculate = SubmitField('Calcular')
    submit = SubmitField('Aceptar')