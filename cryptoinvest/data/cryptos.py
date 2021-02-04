from cryptoinvest.data.consulta import consulta

def cryptos():
    cryptos = consulta('SELECT crypto_id, crypto FROM cryptos;')
    
    result = []

    for dictionary in cryptos:
        result.append((dictionary['crypto_id'], dictionary['crypto']))

    return result
    
def get_crypto(crypto_id):
    the_crypto = consulta(f'SELECT crypto FROM cryptos WHERE crypto_id={crypto_id};')
    return the_crypto[0]['crypto']    

def wallet():                   
    wallet = consulta('''
                    SELECT tc.crypto 'name', tc.crypto_id 'id'
                    FROM movements AS m
                    INNER JOIN cryptos AS tc ON m.to_currency = tc.crypto_id
					WHERE m.to_currency != 1
					GROUP BY m.to_currency;
                    ''')   

    for crypto in wallet:
        crypto_amount = consulta(f'''
                    SELECT SUM(totalF) AS total_available
                    FROM (
                    SELECT SUM(to_quantity) as totalF
                    FROM movements
                    WHERE to_currency = {crypto['id']}
                    UNION
                    SELECT SUM(from_quantity)*-1 
                    FROM movements
                    WHERE from_currency = {crypto['id']});
                    ''')
        
        crypto['available'] = crypto_amount[0]['total_available']

    return wallet

""" 
def cryptos_disponibles():
    pocket_money = wallet()
    print(pocket_money)

    result = []

    for dictionary in pocket_money:
        if (float(dictionary['available']) > 0):
            result.append((dictionary['id'], dictionary['name']))
        
    result.append(('1', 'EUR'))

    return result 

"""

'''
cryptos_disponibles = []

for registro in consulta('SELECT from_currency, to_currency FROM movements;'):
    print(registro)
    cryptos_disponibles += registro

return cryptos_disponibles
'''

        
"""
    total_bitcoin = float(to_bitcoin[0]['to_bitcoin']) - float(from_bitcoin[0]['from_bitcoin'])
    
    
    
    wallet = {}

    for id in 
    clave crypto valor saldo
    
    Si la cantidad es <= 0:
        fuera de lista
    
    devolver lista


    • Para cada crypto obtener su total como: 
    La suma de Cantidad_to de todos los movimientos cuya Moneda_to es la crypto en cuestión - La suma de Cantidad_from de
    todos los movimientos cuya Moneda_from es la crypto en cuestión
"""