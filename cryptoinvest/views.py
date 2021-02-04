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
    mensajes = []
    
    try:
        datos = get_movements()
    except Exception as e:
        print('**ERROR**: LO QUE SEA QUE HACE / VERLO - get_movements: {} {}'.format(type(e).__name__, e))
        mensajes.append('Error en el acceso a base de datos. Consulte con el administrador.')
        return render_template('index.html', mensajes=mensajes)

    #Si renombro la base de datos como db1 funciona, pero si lo hago como db_ no

    return render_template('index.html', datos=datos, mensajes=mensajes)


@app.route('/purchase', methods=['GET', 'POST'])
def purchase():
    form = PurchaseForm()
    to_quantity = ""
    price_unit = ""
    now = datetime.now()
    calculate = False
    mensajes = []

    if request.method == 'POST':
        if form.calculate.data:
            if form.validate():
                try:
                    from_currency = get_crypto(form.from_currency.data) 
                    to_currency = get_crypto(form.to_currency.data)
                except Exception as e:
                    print('**ERROR**: Acceso a base de datos - relación crypto_id con crypto_name: {} {}'.format(type(e).__name__, e))
                    mensajes.append('Error en el acceso a base de datos. Consulte con el administrador.')
                    return render_template('purchase.html', form=form, to_quantity=to_quantity, price_unit=price_unit, calculate=calculate, mensajes=mensajes)

                try:
                    to_quantity = round(conversion(form.from_quantity.data, from_currency, to_currency), 8)
                except Exception as e:
                    print('**ERROR**: Acceso a API - consulta de conversion: {} {}'.format(type(e).__name__, e))
                    mensajes.append('Error en el acceso a la API. Consulte con el administrador.')
                    return render_template('purchase.html', form=form, to_quantity=to_quantity, price_unit=price_unit, calculate=calculate, mensajes=mensajes)
                
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
                    except Exception as e:
                        print('**ERROR**: Acceso a base de datos - inserción de movimientos: {} {}'.format(type(e).__name__, e))
                        mensajes.append('Error en el acceso a base de datos. Consulte con el administrador.')
                        return render_template('purchase.html', form=form, to_quantity=to_quantity, price_unit=price_unit, calculate=calculate, mensajes=mensajes)

        
            else:
                #En realidad quiero que me devuelva el template vacío
                return render_template('purchase.html', form=form, to_quantity=to_quantity, price_unit=price_unit, calculate=calculate, mensajes=mensajes)

    form.from_currency.choices = actual_cryptos()

    return render_template('purchase.html', form=form, to_quantity=to_quantity, price_unit=price_unit, calculate=calculate, mensajes=mensajes)


@app.route('/status')
def status():
    mensajes = []

    try:
        the_inv = total_invested()
    except Exception as e:
        print('**ERROR**: Acceso a base de datos - cálculo de € gastados: {} {}'.format(type(e).__name__, e))
        mensajes.append('Error en el acceso a base de datos. Consulte con el administrador.')
        return render_template('status.html', total_invested=f'{total_invested():.2f}', actual_value=f'{the_real_value:.2f}', mensajes=mensajes)

    try:    
        the_bal = euros_balance()
    except Exception as e:
        print('**ERROR**: Acceso a base de datos - balance de € invertidos: {} {}'.format(type(e).__name__, e))
        mensajes.append('Error en el acceso a base de datos. Consulte con el administrador.')
        return render_template('status.html', total_invested=f'{total_invested():.2f}', actual_value=f'{the_real_value:.2f}', mensajes=mensajes)

    try:
        the_val = actual_value()
    except Exception as e:
        print('**ERROR**: Acceso a API - consulta de conversion: {} {}'.format(type(e).__name__, e))
        mensajes.append('Error en el acceso a la API. Consulte con el administrador.')
        return render_template('status.html', total_invested=f'{total_invested():.2f}', actual_value=f'{the_real_value:.2f}', mensajes=mensajes)        
        
        #Aquí puede petar por dos lados
        #La API ha fallado con un error 429

        print('Error the_val')
        pass

    the_real_value = the_inv + the_bal + the_val


    
    return render_template('status.html', total_invested=f'{total_invested():.2f}', actual_value=f'{the_real_value:.2f}', mensajes=mensajes)