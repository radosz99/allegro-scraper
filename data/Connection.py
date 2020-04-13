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
    create_table_sql = """ CREATE TABLE IF NOT EXISTS stats (
                                        offer_id text NOT NULL,
                                        offer_title text,
                                        username text NOT NULL,
                                        price real not NULL,
                                        price_with_ship real,
                                        offer_url text NOT NULL,
                                        offer_img_url text,
                                        analize_day text NOT NULL,
                                        analize_hour text NOT NULL,
                                        buyers int NOT NULL,
                                        items_sold int NOT NULL,
                                        promoted int NOT NULL
                                    ); """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)
        

def get_connection():
    database = r"Allegro_scanner\data\database\stats.db"

    # create a database connection
    conn = create_connection(database)

    if conn is not None:
        create_table(conn)
        return conn

        