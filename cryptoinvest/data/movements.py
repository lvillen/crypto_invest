import sqlite3
from sqlite3 import Error

DBFILE = 'cryptoinvest/data/database.db'

def create_connection(db_file):
    conn = None

    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

def get_movements(conn, query, params=()):
    try:
        c = conn.cursor()
        c.execute(query, params)
        conn.commit()
        rows = c.fetchall()
        conn.close()
    except Error as e:
        print(e)

def consulta(query, params=()):
    '''
    'SELECT * FROM TABLA' -> [(),(), (),]
    'SELECT * FROM TABLA VACIA ' -> []
    'INSERT ...' -> []
    'UPDATE ...' -> []
    'DELETE ...' -> []
    '''

    if len(filas) == 0:
        return filas

    columnNames = []
    for columnName in c.description:
        columnNames.append(columnName[0])

    listaDeDiccionarios = []

    for fila in filas:
        d = {}
        for ix, columnName in enumerate(columnNames):
            d[columnName] = fila[ix]
        listaDeDiccionarios.append(d)

    return listaDeDiccionarios


def get_movements():


'''
class DB():
    def __init__:

    def getmovements():

    def addmovement():

    def ...
'''
