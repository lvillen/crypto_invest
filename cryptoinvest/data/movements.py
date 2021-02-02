from cryptoinvest.data.consulta import consulta
from cryptoinvest.data.cryptos import cryptos, wallet

DBFILE = 'cryptoinvest/data/database.db'

def get_movements():
    return consulta( '''SELECT
                        m.date 'date',
                        m.time 'time',
                        fc.crypto 'from_currency',
                        m.from_quantity 'from_quantity',
                        tc.crypto 'to_currency',
                        m.to_quantity 'to_quantity'
                        FROM movements AS m
                        INNER JOIN cryptos AS fc ON m.from_currency = fc.crypto_id
                        INNER JOIN cryptos AS tc ON m.to_currency = tc.crypto_id;
                        '''
    )

def total_invested():
    result = consulta('''
                    SELECT sum(from_quantity) AS total_invested 
                    FROM movements 
                    WHERE from_currency = 1;   
                    ''')
    
    return result[0]['total_invested']

def euros_balance():
    total_invested = consulta('''
                    SELECT sum(from_quantity) AS total_invested 
                    FROM movements 
                    WHERE from_currency = 1;   
                    ''')

    total_received = consulta('''
                    SELECT sum(to_quantity) AS total_received 
                    FROM movements 
                    WHERE to_currency = 1;   
                    ''')

    #Buscar una forma de hacerlo todo en una sentencia

    euros_balance = float(total_received[0]['total_received']) - float(total_invested[0]['total_invested'])
    
    return euros_balance

def actual_value():

    Valor actual en euros de nuestras cryptos: 
    Al existir 10 posibles cryptos debemos
    BUCLE FOR 
    • Para cada crypto obtener su total como: 
    La suma de Cantidad_to de todos los movimientos cuya Moneda_to es la crypto en cuestión - La suma de Cantidad_from de
    todos los movimientos cuya Moneda_from es la crypto en cuestión

    • Con esa cantidad utilizamos el endpoint de conversión (Ver registro de movimientos from_to) y convertimos ese total de crypto en euros
    
    • Sumamos los euros de cada una de las cryptos