import sqlite3
from sqlite3 import Error

def select_all_offers(conn, username, min_items):
    cur = conn.cursor()
    sql = "SELECT id FROM offers WHERE first_items_sold>=" + str(min_items) + " AND user_id = (SELECT id FROM users WHERE username = '" + username + "')ORDER BY first_items_sold DESC"
    cur.execute(sql)
    rows = cur.fetchall()
    return rows

def select_raports_by_offer_id(conn, offer_id):
    cur = conn.cursor()
    cur.execute("SELECT * FROM stats WHERE offer_id=" + offer_id)
    rows = cur.fetchall()
    return rows

def select_all_raports(conn, username):
    cur = conn.cursor()
    cur.execute("SELECT * FROM stats WHERE username='" + username + "' ORDER BY analize_day ASC, analize_hour ASC")
    rows = cur.fetchall()
    return rows

def select_user_raports(conn, username):
    cur = conn.cursor()
    cur.execute("SELECT * FROM raports WHERE user_id = (SELECT id FROM users WHERE username = '" + username + "') ORDER BY id ASC")
    rows = cur.fetchall()
    return rows
