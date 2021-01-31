import sqlite3
from sqlite3 import Error

'''
Ejecutarlo una vez antes de montar la app
'''

DBFILE = 'database.db' 
#DBFILE = app.config['DBFILE']

create_cryptos_table = 'CREATE TABLE IF NOT EXISTS cryptos (\
                                crypto_id integer PRIMARY KEY, \
                                crypto text NOT NULL);'

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

def create_table(conn, query):
    try:
        c = conn.cursor()
        c.execute(query)
    except Error as e:
        print('Creation error: '+ str(e))

def main():
    conn = create_connection(DBFILE)
    #conn = create_connection(DBFILE)

    if conn is not None:
        create_table(conn, create_cryptos_table)
        create_table(conn, create_movements_table)
        conn.commit()
        conn.close()
    else: 
        print("Error! Cannot create the database connection.")

if __name__ == '__main__':
    main()
