from cryptoinvest import app
from cryptoinvest.forms import PurchaseForm
from flask import render_template, request, url_for, redirect
import sqlite3
from cryptoinvest.data.movements import *
import datetime
from cryptoinvest.coinmarketcap_api.api_functions import *

DBFILE = app.config['DBFILE']

@app.route('/')
def movements():
    return render_template('index.html', datos=get_movements())

@app.route('/purchase', methods=['GET', 'POST'])
def purchase():
    form = PurchaseForm(request.form)
    to_quantity = ""

    #LLAMADA A BASE DE DATOS
    
    # '''
    # LEER LA BASE DE DATOS
    # HACER UN POST PARA CALCULATE
    # CAPAR LA POSIBILIDAD DE TOCAR NADA
    # HACER OTRO POST PARA QUE SE GRABE LA OPERACIÓN

    # No limitar la vista, validación vía Python
    # '''

    if request.method == 'POST' and request.form.get('calculate'):
        to_quantity = conversion(request.form.get('from_quantity'), request.form.get('from_currency'), request.form.get('to_currency'))
        
    else:
        print('Non operazzione')

        '''
        if form.validate():
            pass
            consulta('INSERT INTO movements (date, time, from_currency, from_quantity, to_currency, to_quantity) VALUES (?, ?, ?, ?, ?, ?);',
            (
                datetime.strftime(),
                datetime.strfdate(),
                ,
                ,
                ,
                ,
            ))    
        else:
            pass
        '''
    return render_template('purchase.html', form=form, to_quantity=to_quantity)

''' 
@app.route('/status')
    1: SALDO
        Sumar todo lo gastado en €
        La suma de Cantidad_to de todas los movimientos cuya
        Moneda_to es euros - La suma de Cantidad_from de todos 
        los movimientos cuya Moneda_from es euros

    2. INVERTIDO
        La suma de Cantidad_from cuando Moneda_from es euros

    3. VALOR ACTUAL CRYPTOS
        Bucle [qué monedas]
            Bucle [de cada moneda, qué cantidad] > Convertir a €
        total moneda += cantidad

    return render_template('status.html', datos=status())
'''
