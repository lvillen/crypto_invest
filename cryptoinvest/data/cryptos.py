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

'''
def introducecryptos():
    INSERT INTO cryptos
        BLABLABLA

PD: Quizá deba ir en el initdb
'''


def wallet():
    to_bitcoin = consulta('''
                    SELECT sum(to_quantity) AS to_bitcoin
                    FROM movements 
                    WHERE to_currency = 8;   
                    ''')

    from_bitcoin = consulta('''
                    SELECT sum(from_quantity) AS from_bitcoin
                    FROM movements 
                    WHERE from_currency = 8;   
                    ''')
    
    total_bitcoin = float(to_bitcoin[0]['to_bitcoin']) - float(from_bitcoin[0]['from_bitcoin'])
    
    
    '''
    wallet = {}

    for id in 
    clave crypto valor saldo
    
    Si la cantidad es <= 0:
        fuera de lista
    
    devolver lista


    • Para cada crypto obtener su total como: 
    La suma de Cantidad_to de todos los movimientos cuya Moneda_to es la crypto en cuestión - La suma de Cantidad_from de
    todos los movimientos cuya Moneda_from es la crypto en cuestión
    '''