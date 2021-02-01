import sqlite3
from sqlite3 import Error

DBFILE = 'database.db' 

create_cryptos_table = 'CREATE TABLE IF NOT EXISTS cryptos (\
                                crypto_id integer PRIMARY KEY, \
                                crypto text NOT NULL);'

create_cryptos = '''INSERT INTO cryptos VALUES 
            (1, "EUR"), 
			(2, "ETH"), 
			(3, "LTC"), 
			(4, "BNB"), 
			(5, "EOS"),
			(6, "XLM"),
			(7, "TRX"),
			(8, "BTC"),
			(9, "XRP"),
			(10, "BCH"),
			(11, "USDT"),
			(12, "BSV"),
			(13, "ADA");
            '''

create_movements_table = 'CREATE TABLE IF NOT EXISTS movements (\
                                id integer PRIMARY KEY,\
                                date text NOT NULL, \
                                time text NOT NULL, \
                                from_currency integer, \
                                from_quantity real, \
                                to_currency integer, \
                                to_quantity real, \
                                FOREIGN KEY(from_currency) REFERENCES cryptos(crypto_id), \
                                FOREIGN KEY(to_currency) REFERENCES cryptos(crypto_id));'

def create_connection(db_file):
    conn = None
    print(db_file)
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print('Connection error: ' + str(e))

def execute_query(conn, query):
    try:
        c = conn.cursor()
        c.execute(query)
    except Error as e:
        print('Query error: '+ str(e))

def main():
    conn = create_connection(DBFILE)

    if conn is not None:
        execute_query(conn, create_cryptos_table)
        execute_query(conn, create_movements_table)
        execute_query(conn, create_cryptos)
        conn.commit()
        conn.close()
    else: 
        print("Error! Cannot create the database connection.")

if __name__ == '__main__':
    main()
