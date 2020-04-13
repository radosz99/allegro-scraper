import sqlite3
from sqlite3 import Error

def create_print(conn, single_print):
    print(single_print)
    sql = ''' INSERT INTO stats(offer_id,offer_title,price, price_with_ship,username,offer_url,offer_img_url,analize_day,analize_hour,buyers,items_sold, promoted)
              VALUES(?,?,?,?,?,?,?,?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, single_print)
    conn.commit()
    return cur.lastrowid
