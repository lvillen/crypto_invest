from flask_wtf import FlaskForm
from wtforms import FloatField, SubmitField, SelectField
from wtforms.validators import DataRequired, ValidationError, NumberRange
from cryptoinvest.data.cryptos import *

monedas = [(1, "EUR"), (2, "ETH"), (3, "LTC"), (4, "BNB"), (5, "EOS"), (6, "XLM"), (7, "TRX"), (8, "BTC"), (9, "XRP"), (10, "BCH"), (11, "USDT"), (12, "BSV"), (13, "ADA")]

def actual_cryptos():
    try:
        actual_wallet = wallet()
    except Exception as e:
        print('**ERROR**: Acceso a base de datos - imposible realizar la consulta "wallet": {} {}'.format(type(e).__name__, e))
        mensajes = f'Debido a un error con la base de datos, no puede acceder a esta página, sentimos las molestias.'
        return mensajes
    
    result = []
    result.append(('1', 'EUR'))
    for dictionary in actual_wallet:
        if (float(dictionary['available']) > 0):
            result.append((dictionary['id'], dictionary['name']))
    
    return result

def available_cryptos(form, field):
    try:
        available_cr = wallet()
    except Exception as e:
        print('**ERROR**: Acceso a base de datos - imposible realizar la consulta "wallet": {} {}'.format(type(e).__name__, e))
        mensajes = f'Debido a un error con la base de datos, no puede acceder a esta página, sentimos las molestias.'
        return mensajes

    currency = form.from_currency.data

    for dictionary in available_cr:
        if dictionary['id'] == int(currency):
            if dictionary['available'] < field.data:
                raise ValidationError('No tiene saldo suficiente.')

def not_same_currency(form, field):
    from_currency = form.from_currency.data

    if field.data == from_currency:
        raise ValidationError('No puede hacer la operación, elija una moneda correcta.')


class PurchaseForm(FlaskForm):
    from_currency = SelectField('De qué moneda', choices=actual_cryptos(), validators=[DataRequired()]) 
    from_quantity = FloatField('Qué cantidad', validators=[DataRequired('Introduzca un número válido, recuerde que solo puede utilizar números y que los decimales deben ir precedidos de un punto.'), available_cryptos, NumberRange(min=0.00000001, max=1000000000 ,message='Introduzca un número válido.')])
    to_currency = SelectField('A qué moneda', choices=monedas, validators=[DataRequired(), not_same_currency])
    to_quantity = FloatField('Cantidad recibida', render_kw={'readonly': True})
    price_unit = FloatField('Precio por unidad', render_kw={'readonly': True})

    calculate = SubmitField('Calcular')
    submit = SubmitField('Aceptar')
    #reset = SubmitField('Reset')    