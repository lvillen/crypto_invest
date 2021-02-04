from cryptoinvest import app
from cryptoinvest.forms import PurchaseForm, actual_cryptos
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
    calculate = False

    if request.method == 'POST':
        if form.calculate.data:
            if form.validate():
                try:
                    from_currency = get_crypto(form.from_currency.data) 
                    to_currency = get_crypto(form.to_currency.data)
                except:
                    #Error que vaya a la base de datos
                    pass
                try:
                    to_quantity = round(conversion(form.from_quantity.data, from_currency, to_currency), 8)
                except:
                    #Error que vaya a la API
                    pass
                try:
                    price_unit = round((float(form.from_quantity.data) / to_quantity), 8)
                except:
                    print("Solo para ver qué ha pasado")
                    #Cómo controlarlo | Darle un voltio
                
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
                    try:
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
                    except:
                        #Error de base de datos
                        #return render_template('purchase.html', form=form, to_quantity=to_quantity, price_unit=price_unit)
                        pass
        
            else:
                #En realidad quiero que me devuelva el template vacío
                return render_template('purchase.html', form=form, to_quantity=to_quantity, price_unit=price_unit, calculate=calculate)

    form.from_currency.choices = actual_cryptos()

    return render_template('purchase.html', form=form, to_quantity=to_quantity, price_unit=price_unit, calculate=calculate)


@app.route('/status')
def status():
    try:
        the_inv = total_invested()
    except:
        #Error de base de datos
        pass

    try:    
        the_bal = euros_balance()
    except:
        #Error de base de datos
        pass

    try:
        the_val = actual_value()
    except:
        #Error de API
        pass

    the_real_value = the_inv + the_bal + the_val


    
    return render_template('status.html', total_invested=f'{total_invested():.2f}', actual_value=f'{the_real_value:.2f}')