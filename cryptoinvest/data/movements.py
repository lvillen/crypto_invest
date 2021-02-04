from cryptoinvest.data.consulta import consulta
from cryptoinvest.data.cryptos import cryptos, wallet
from cryptoinvest.coinmarketcap_api.api_functions import conversion

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
    balance = consulta('''
                SELECT SUM(totalF) AS balance
                FROM (
                SELECT SUM(to_quantity) as totalF
                FROM movements
                WHERE to_currency = 1
                UNION
                SELECT SUM(from_quantity)*-1 
                FROM movements
                WHERE from_currency = 1);
            ''')

    return balance[0]['balance']
    

def actual_value():
    cryptos = wallet()

    actual_value = .0

    for crypto in cryptos:
        euros = conversion(crypto['available'], crypto['name'], 'EUR')
        actual_value += euros
    
    return actual_value