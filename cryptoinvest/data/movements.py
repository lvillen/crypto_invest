from cryptoinvest.data.consulta import *

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