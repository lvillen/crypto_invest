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
    cryptos = consulta('SELECT crypto FROM cryptos;')
    
    result = []

    for dictionary in cryptos:
        result.append(dictionary['crypto'])

    return result
    
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