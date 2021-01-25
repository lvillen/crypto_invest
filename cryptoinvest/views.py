from cryptoinvest import app
from flask import render_template, request, url_for, redirect
import sqlite3
# import data as DB

DBFILE = app.config['DBFILE']

@app.route('/')
def movements():
    #TODO el acceso a los movimientos

    '''
    movements = DB.getmovements()
    '''

    return render_template('index.html')

@app.route('/buy')
def buy():
    #TODO lógica operacional

    '''
    No limitar la vista, validación vía Python
    '''

    return render_template('buy.html')