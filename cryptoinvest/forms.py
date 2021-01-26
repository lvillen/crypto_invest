from flask_wtf import FlaskForm
from wtforms import FloatField, SubmitField, SelectField #TODO más
from wtforms.validators import DataRequired, #TODO los demás

monedas = ('EUR', 'ETH', 'LTC', 'BNB', 'EOS', 'XLM', 'TRX', 'BTC', 'XRP', 'BCH', 'USDT', 'BSV', 'ADA')

class PurchaseForm(FlaskForm):

    from_currency = SelectField('Moneda', choices=monedas, validators=[DataRequired()]) 
    from_quantity = FloatField('Cantidad', validators=[DataRequired()])
    to_currency = SelectField('Moneda', choices=monedas, validators=[DataRequired()])
    to_quantity = FloatField('Cantidad', validators=[DataRequired()])

    calculate = SubmitField('Calcular')
    submit = SubmitField('Aceptar')