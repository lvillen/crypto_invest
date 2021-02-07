from cryptoinvest import application
from cryptoinvest.forms import PurchaseForm, actual_cryptos
from flask import render_template, request, url_for, redirect
import sqlite3
from cryptoinvest.data.movements import *
from cryptoinvest.data.cryptos import *
from datetime import datetime
from cryptoinvest.coinmarketcap_api.api_functions import *

DBFILE = application.config['DBFILE']

@application.route('/')
def movements():
    mensajes = []
    
    try:
        datos = get_movements()
    except Exception as e:
        print('**ERROR**: Error en la base de datos - no se puedo realizar el acceso a la tabla "movements": {} {}'.format(type(e).__name__, e))
        mensajes.append('Error en el acceso a base de datos. Consulte con el administrador.')
        return render_template('index.html', mensajes=mensajes)

    return render_template('index.html', datos=datos, mensajes=mensajes)


@application.route('/purchase', methods=['GET', 'POST'])
def purchase():
    mensajes = []
    
    try: 
        form = PurchaseForm()
        form.from_currency.choices = actual_cryptos()
    except Exception as e:
                    print('**ERROR**: Acceso a base de datos en la creación del formulario no disponible: {} {}'.format(type(e).__name__, e))
                    mensajes.append('Debido a un error en el acceso a la base de datos no se pudo crear esta página. Sentimos las molestias.')
                    return render_template('500.html', mensajes=mensajes)
    
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
                    return render_template('500.html', mensajes=mensajes)

                try:
                    to_quantity = round(conversion(form.from_quantity.data, from_currency, to_currency), 8)
                except Exception as e:
                    print('**ERROR**: Acceso a API - Error 400: {} {}'.format(type(e).__name__, e))
                    mensajes.append('Error 400 en el acceso a la API. Sentimos informarle que su petición no pudo realizarse. Consulte con el administrador.')
                    return render_template('400.html', mensajes=mensajes)

                try:
                    price_unit = round((float(form.from_quantity.data) / to_quantity), 8)
                except ZeroDivisionError as e:
                    print('**ERROR**: Divisón no disponible: {} {}'.format(type(e).__name__, e))
                    mensajes.append('No se pudo acceder al recurso, sentimos las molestias. Inténtelo de nuevo accedienco a "compra" en el link superior realizando una operación cuya división no resulte en 0.')
                    return render_template('404.html', mensajes=mensajes)
                
                calculate = True

                return render_template('purchase.html', form=form, to_quantity=to_quantity, price_unit=price_unit, calculate=calculate, mensajes=mensajes)
            
            else: 
                return render_template('purchase.html', form=form, to_quantity=to_quantity, price_unit=price_unit, calculate=calculate, mensajes=mensajes)


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
                            return render_template('500.html', mensajes=mensajes)
            else:
                return render_template('purchase.html', form=form, to_quantity=to_quantity, price_unit=price_unit, calculate=calculate, mensajes=mensajes)

    return render_template('purchase.html', form=form, to_quantity=to_quantity, price_unit=price_unit, calculate=calculate, mensajes=mensajes)


@application.route('/status')
def status():
    mensajes = []

    try:
        the_inv = total_invested()
    except Exception as e:
        print('**ERROR**: Acceso a base de datos - cálculo de € gastados: {} {}'.format(type(e).__name__, e))
        mensajes.append('Error en el acceso a base de datos. Consulte con el administrador.')
        return render_template('status.html', total_invested='No se pudo mostrar', actual_value='No se pudo mostrar', mensajes=mensajes)

    try:    
        the_bal = euros_balance()
    except Exception as e:
        print('**ERROR**: Acceso a base de datos - balance de € invertidos: {} {}'.format(type(e).__name__, e))
        mensajes.append('Error en el acceso a base de datos. Consulte con el administrador.')
        return render_template('status.html', total_invested='No se pudo mostrar', actual_value='No se pudo mostrar', mensajes=mensajes)

    try:
        the_val = actual_value()
    except Exception as e:
        print('**ERROR**: Acceso a API - consulta de conversion: {} {}'.format(type(e).__name__, e))
        mensajes.append('Error en el acceso a la API. Consulte con el administrador.')
        return render_template('status.html', total_invested='No se pudo mostrar', actual_value='No se pudo mostrar', mensajes=mensajes)        
        
        #Aquí puede petar por dos lados
        #La API ha fallado con un error 429

        print('Error the_val')
        pass

    the_real_value = the_inv + the_bal + the_val

    return render_template('status.html', total_invested=f'{the_inv:.2f} €', actual_value=f'{the_real_value:.2f} €', mensajes=mensajes)

@application.route('/500')
def error500():
    mensajes = []
    return render_template('500.html', mensajes=mensajes)

@application.route('/400')
def error400():
    mensajes = []
    return render_template('400.html', mensajes=mensajes)

@application.route('/404')
def error404():
    mensajes = []
    return render_template('404.html', mensajes=mensajes)
