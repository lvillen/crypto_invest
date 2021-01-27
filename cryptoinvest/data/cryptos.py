from cryptoinvest.data.consulta import *

def cryptos_disponibles():
    return cryptos()    

    '''
    cryptos_disponibles = []
    
    for registro in consulta('SELECT from_currency, to_currency FROM movements;'):
        print(registro)
        cryptos_disponibles += registro

    return cryptos_disponibles
    '''

def cryptos():
    return consulta('SELECT crypto FROM cryptos;')