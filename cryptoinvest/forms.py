from flask_wtf import FlaskForm
from wtforms import FloatField, SubmitField, SelectField
from wtforms.validators import DataRequired, ValidationError, NumberRange
from cryptoinvest.data.cryptos import *

def actual_cryptos():
    #Gestionar aquí
    try:
        actual_wallet = wallet()
    except:
        return (1, 'EUR')
    
    result = []
    result.append(('1', 'EUR'))
    for dictionary in actual_wallet:
        if (float(dictionary['available']) > 0):
            result.append((dictionary['id'], dictionary['name']))
    
    return result

def available_cryptos(form, field):
    #Gestionar aquí
    try:
        available_cr = wallet()
    except:
        pass 
    
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
    from_currency = SelectField('FromMoneda', choices=actual_cryptos(), validators=[DataRequired()]) 
    from_quantity = FloatField('FromCantidad', validators=[DataRequired('Introduzca un número válido, recuerde que solo puede utilizar números y que los decimales deben ir precedidos de un punto.'), available_cryptos, NumberRange(min=0.00000001, max=1000000000 ,message='Introduzca un número válido.')])
    to_currency = SelectField('ToMoneda', choices=cryptos(), validators=[DataRequired(), not_same_currency])
    to_quantity = FloatField('ToCantidad', render_kw={'readonly': True})
    price_unit = FloatField('Precio por unidad', render_kw={'readonly': True})

    calculate = SubmitField('Calcular')
    submit = SubmitField('Aceptar')
    #reset = SubmitField('Reset')    