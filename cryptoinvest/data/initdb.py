import sqlite3
from sqlite3 import Error

'''
Ejecutarlo una vez antes de montar la app

¡¡¡Está petando por algún lado!!!
'''

DBFILE = 'cryptoinvest/data/database.db'

def create_connection(db_file):
    conn = None

    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

def create_table(conn, query):
    try:
        c = conn.cursor()
        c.execute(query)
    except Error as e:
        print(e)

def main():
    create_movements_table = 'CREATE TABLE IF NOT EXISTS movements (\
                            id integer PRIMARY KEY, date text NOT NULL, \
                            time text NOT NULL, from_currency integer, \
                            from_quantity real, to_currency integer, \
                            to_quantity real);'

    conn = create_connection(DBFILE)

    if conn is not None:
        create_table(conn, create_movements_table)
        conn.commit()
        conn.close()
    else: 
        print("Error! Cannot create the database connection.")

    

if __name__ == '__main__':
    main()
