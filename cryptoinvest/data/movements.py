from cryptoinvest.data.consulta import *

DBFILE = 'cryptoinvest/data/database.db'

def get_movements():
    return consulta('SELECT date, time, from_currency, from_quantity, to_currency, to_quantity FROM movements;')