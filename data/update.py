import sqlite3
from sqlite3 import Error

def update_raports(conn, offers_quantity, raport_id):
    sql= ''' UPDATE raports SET offers_quantity = ''' + str(offers_quantity) + '''
                WHERE id = ''' + str(raport_id)
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()
