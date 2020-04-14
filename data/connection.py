import sqlite3
from sqlite3 import Error
import data.database as db

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        c = conn.cursor()
        c.execute('pragma encoding')
    except Error as e:
        print(e)

    return conn

def create_table(conn):

    create_table_sql = """ CREATE TABLE IF NOT EXISTS users (
                                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                                        username TEXT NOT NULL,
                                        recommend_count INTEGER, 
                                        not_recommend_count INTEGER,
                                        offers_quantity INTEGER
                                    ); """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

    create_table_sql = """ CREATE TABLE IF NOT EXISTS raports (
                                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                                        user_id INTEGER NOT NULL,
                                        offers_quantity INTEGER,
                                        day INTEGER NOT NULL,
                                        month INTEGER NOT NULL,
                                        year INTEGER NOT NULL,
                                        hour INTEGER NOT NULL,
                                        minutes INTEGER NOT NULL,
                                        FOREIGN KEY(user_id) REFERENCES users(id)
                                    ); """

    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)   

 
    create_table_sql = """ CREATE TABLE IF NOT EXISTS offers (
                                        id INTEGER PRIMARY KEY,
                                        user_id INTEGER NOT NULL,
                                        last_items_sold INTEGER,
                                        first_items_sold INTEGER,
                                        raports_quantity INTEGER,
                                        FOREIGN KEY(user_id) REFERENCES users(id)
                                    ); """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)    

    create_table_sql = """ CREATE TABLE IF NOT EXISTS stats (
                                        offer_id INTEGER NOT NULL,
                                        offer_title TEXT,
                                        price REAL not NULL,
                                        price_with_ship REAL,
                                        offer_url TEXT,
                                        offer_img_url TEXT,
                                        raport_id INTEGER NOT NULL,
                                        buyers INTEGER,
                                        items_sold INTEGER,
                                        promoted INTEGER,
                                        FOREIGN KEY(offer_id) REFERENCES offers(id)
                                        FOREIGN KEY(raport_id) REFERENCES raports(id)
                                    ); """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)



def get_connection():
    #database = r"C:\Users\Radek\Desktop\Allegro_analizer\sqlite\db\pythonsqlite.db"
    database = r"Allegro_scanner\data\database\stats.db"

    # create a database connection
    conn = create_connection(database)

    if conn is not None:
        create_table(conn)
        return conn

        