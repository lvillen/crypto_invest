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
    cryptos = consulta('SELECT crypto_id, crypto FROM cryptos;')
    
    result = []

    for dictionary in cryptos:
        result.append((dictionary['crypto_id'], dictionary['crypto']))

    return result
    

def get_crypto(crypto_id):
    the_crypto = consulta(f'SELECT crypto FROM cryptos WHERE crypto_id={crypto_id};')
    return the_crypto[0]['crypto']

    #A medio montar
    

'''
def introducecryptos():
    INSERT INTO cryptos
        BLABLABLA

PD: Quizá deba ir en el initdb
'''

'''
def wallet():
    Lista de criptos sin €
    Dic vacío cryptos

    clave crypto valor saldo
    
    Si la cantidad es <= 0:
        fuera de lista
    
    devolver lista
'''