from cryptoinvest import app
from flask import render_template, request, url_for, redirect
import sqlite3

DBFILE = app.config['DBFILE']

@app.route('/')
def movements():
    #TODO el acceso a los movimientos

    return render_template('index.html')

@app.route('/buy')
def buy():
    #TODO lógica operacional

    return render_template('buy.html')