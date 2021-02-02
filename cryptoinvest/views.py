from cryptoinvest import app
from cryptoinvest.forms import PurchaseForm
from flask import render_template, request, url_for, redirect
import sqlite3
from cryptoinvest.data.movements import *
from cryptoinvest.data.cryptos import *
from datetime import datetime
from cryptoinvest.coinmarketcap_api.api_functions import *

DBFILE = app.config['DBFILE']

@app.route('/')
def movements():
    Errors = []
    try:
        return render_template('index.html', datos=get_movements())
    except Error as e:
        print(e)
        Errors.append('Esto ha petau')
        return render_template('index.html', Errors=Errors)

@app.route('/purchase', methods=['GET', 'POST'])
def purchase():
    form = PurchaseForm()
    to_quantity = ""
    price_unit = ""
    now = datetime.now()
    #validate_1 = form.from_currency.validate(form) and form.from_quantity.validate(form) and form.to_currency.validate(form)
    calculate = False

    if request.method == 'POST':
        if form.calculate.data:
            if form.validate():
                from_currency = get_crypto(form.from_currency.data) 
                to_currency = get_crypto(form.to_currency.data)
                to_quantity = round(conversion(form.from_quantity.data, from_currency, to_currency), 8)
                price_unit = round((float(form.from_quantity.data) / to_quantity), 8)
                calculate = True
            
        """ if form.reset.data:
            form = PurchaseForm()
            to_quantity = ""
            price_unit = ""
            now = datetime.now()
            validate_1 = form.from_currency.validate(form) and form.from_quantity.validate(form) and form.to_currency.validate(form)
            calculate = False
            return render_template('purchase.html', form=form, to_quantity=to_quantity, price_unit=price_unit, calculate=calculate) """
            
        if form.submit.data:
            if form.validate():
                if form.from_currency.data != form.to_currency.data:
                    consulta('INSERT INTO movements (date, time, from_currency, from_quantity, to_currency, to_quantity) VALUES (?, ?, ?, ?, ?, ?);',
                    (
                        now.date(),
                        now.strftime('%H:%M:%S'),
                        form.from_currency.data,
                        form.from_quantity.data,
                        form.to_currency.data,
                        form.to_quantity.data,
                    ))    

                    return redirect(url_for('movements'))

                else:
                    print("Algo ha ido mal")
                    return render_template('purchase.html', form=form, to_quantity=to_quantity, price_unit=price_unit)

                #Tengo que volver a meter el form = PurchaseForm(request.form) Ó NO

                #LLAMADA A BASE DE DATOS
                
                # LEER LA BASE DE DATOS
                # CAPAR LA POSIBILIDAD DE TOCAR NADA
                # HACER OTRO POST PARA QUE SE GRABE LA OPERACIÓN

                # No limitar la vista, validación vía Python
        
            else:
                print(form.errors)

    return render_template('purchase.html', form=form, to_quantity=to_quantity, price_unit=price_unit, calculate=calculate)


@app.route('/status')
def status():
    print(euros_balance())
    
    return render_template('status.html', total_invested=f'{total_invested():.2f}')

''' 
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
