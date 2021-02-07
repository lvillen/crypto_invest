from cryptoinvest import application
from cryptoinvest.forms import PurchaseForm, actual_cryptos
from flask import render_template, request, url_for, redirect
import sqlite3
from cryptoinvest.data.movements import *
from cryptoinvest.data.cryptos import *
from datetime import datetime
from cryptoinvest.coinmarketcap_api.api_functions import *

DBFILE = application.config['DBFILE']

@application.errorhandler(404)
def pagina_no_encontrado(error):
    return render_template('404.html'), 404

@application.route('/')
def movements():
    header = "Vea sus movimientos"
    mensajes = []
    
    try:
        datos = get_movements()
    except Exception as e:
        print('**ERROR**: Error en la base de datos - no se puedo realizar el acceso a la tabla "movements": {} {}'.format(type(e).__name__, e))
        mensajes.append('Error en el acceso a base de datos. Consulte con el administrador.')
        return render_template('index.html', header=header, mensajes=mensajes)

    return render_template('index.html', header=header, datos=datos, mensajes=mensajes)


@application.route('/purchase', methods=['GET', 'POST'])
def purchase():
    header = "Adquiera cryptomonedas"
    mensajes = []
    
    try: 
        form = PurchaseForm()
    except Exception as e:
        print('**ERROR**: Acceso a base de datos en la creación del formulario no disponible: {} {}'.format(type(e).__name__, e))
        mensajes.append(actual_cryptos())
        return render_template('500.html', header=header, mensajes=mensajes)

    try:
        if isinstance(actual_cryptos(), str):
            print('**ERROR**: Acceso a base de datos en la creación del formulario no disponible: {} {}'.format(type(e).__name__, e))
            mensajes.append(actual_cryptos())
            return render_template('500.html', header=header, mensajes=mensajes)
        else:
            form.from_currency.choices = actual_cryptos()
    except Exception as e:
        print('**ERROR**: Acceso a base de datos en la creación del formulario no disponible: {} {}'.format(type(e).__name__, e))
        mensajes.append(actual_cryptos())
        return render_template('500.html', header=header, mensajes=mensajes)

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
                except Exception as e:
                    print('**ERROR**: Acceso a base de datos - relación crypto_id con crypto_name: {} {}'.format(type(e).__name__, e))
                    mensajes.append('Error en el acceso a base de datos. Consulte con el administrador.')
                    return render_template('500.html', header=header, mensajes=mensajes)

                try:
                    to_quantity = round(conversion(form.from_quantity.data, from_currency, to_currency), 8)
                except Exception as e:
                    print('**ERROR**: Acceso a API - Error 400: {} {}'.format(type(e).__name__, e))
                    mensajes.append('Error 400 en el acceso a la API. Sentimos informarle que su petición no pudo realizarse. Consulte con el administrador.')
                    return render_template('400.html', header=header, mensajes=mensajes)

                try:
                    price_unit = round((float(form.from_quantity.data) / to_quantity), 8)
                except ZeroDivisionError as e:
                    print('**ERROR**: Divisón no disponible: {} {}'.format(type(e).__name__, e))
                    mensajes.append('No podemos hacer café con una tetera. Por favor, realice una división que no divida entre 0.')
                    return render_template('418.html', header=header, mensajes=mensajes)
                
                calculate = True

                return render_template('purchase.html', header=header, form=form, to_quantity=to_quantity, price_unit=price_unit, calculate=calculate, mensajes=mensajes)
            
            else: 
                return render_template('purchase.html', header=header, form=form, to_quantity=to_quantity, price_unit=price_unit, calculate=calculate, mensajes=mensajes)


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
                            return render_template('500.html', header=header, mensajes=mensajes)
            else:
                return render_template('purchase.html', header=header, form=form, to_quantity=to_quantity, price_unit=price_unit, calculate=calculate, mensajes=mensajes)

    return render_template('purchase.html', header=header, form=form, to_quantity=to_quantity, price_unit=price_unit, calculate=calculate, mensajes=mensajes)


@application.route('/status')
def status():
    header = "Compruebe el estado de sus inversiones"
    mensajes = []

    try:
        the_inv = total_invested()
        if the_inv == None:
            the_inv = 0
    except Exception as e:
        print('**ERROR**: Acceso a base de datos - cálculo de € gastados: {} {}'.format(type(e).__name__, e))
        mensajes.append('Error en el acceso a base de datos. Consulte con el administrador.')
        return render_template('status.html', header=header, total_invested='No se pudo mostrar', actual_value='No se pudo mostrar', mensajes=mensajes)

    try:    
        the_bal = euros_balance()
        if the_bal == None:
            the_bal = 0
    except Exception as e:
        print('**ERROR**: Acceso a base de datos - balance de € invertidos: {} {}'.format(type(e).__name__, e))
        mensajes.append('Error en el acceso a base de datos. Consulte con el administrador.')
        return render_template('status.html', header=header, total_invested='No se pudo mostrar', actual_value='No se pudo mostrar', mensajes=mensajes)

    try:
        the_val = actual_value()
        if the_val == None:
            the_val = 0
    except Exception as e:
        print('**ERROR**: Acceso a API - consulta de conversion: {} {}'.format(type(e).__name__, e))
        mensajes.append('Error en el acceso a la API. Consulte con el administrador.')
        return render_template('status.html', header=header, total_invested='No se pudo mostrar', actual_value='No se pudo mostrar', mensajes=mensajes)        

    the_real_value = the_inv + the_bal + the_val

    return render_template('status.html', header=header, total_invested=f'{the_inv:.2f} €', actual_value=f'{the_real_value:.2f} €', mensajes=mensajes)

@application.route('/500')
def error500():
    mensajes = []
    return render_template('500.html', mensajes=mensajes)

@application.route('/400')
def error400():
    mensajes = []
    return render_template('400.html', mensajes=mensajes)

@application.route('/418')
def error418():
    mensajes = []
    return render_template('418.html', mensajes=mensajes)
