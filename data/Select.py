import sqlite3
from sqlite3 import Error

def select_all_prints(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM stats where items_sold>0 and username = 'sport_i_styl' order by items_sold DESC")
    rows = cur.fetchall()
    return rows

def select_print_by_offer_id(conn, offer_id):
    cur = conn.cursor()
    cur.execute("SELECT * FROM stats WHERE offer_id=" + offer_id)
    rows = cur.fetchall()
    return rows
        