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

def select_user_raports_id(conn, username):
    cur = conn.cursor()
    cur.execute("SELECT id FROM raports WHERE user_id = (SELECT id FROM users WHERE username = '" + username + "') ORDER BY id ASC")
    rows = cur.fetchall()
    return rows

def select_user_offers(conn, username, raports_quantity):
    cur = conn.cursor()
    cur.execute("SELECT id FROM offers WHERE raports_quantity = " + str(raports_quantity) + " and user_id = (SELECT id FROM users WHERE username = '" + username + "') order by last_items_sold DESC")
    rows = cur.fetchall()
    return rows

def select_money_from_offer(conn, offer_id):
    cur = conn.cursor()
    cur.execute("SELECT raport_id, price,items_sold FROM stats WHERE offer_id= " + offer_id + " ORDER BY raport_id ASC")
    rows = cur.fetchall()
    return rows

def select_money_from_offer_without_mask(conn, offer_id):
    cur = conn.cursor()
    cur.execute("SELECT raport_id, price,items_sold FROM stats WHERE offer_id= " + offer_id + " AND offer_title NOT LIKE '%Maska%' ORDER BY raport_id ASC")
    rows = cur.fetchall()
    return rows

def select_raport_by_date_and_user(conn, day, month, year, username):
    cur = conn.cursor()
    cur.execute("SELECT id FROM raports WHERE day = " + day + " AND month = " + month + " AND year = " + year + " AND user_id = (SELECT id FROM users WHERE username = '" + username+"')")
    rows = cur.fetchall()
    return rows

def select_stats_by_raport_id(conn, raport_id):
    cur = conn.cursor()
    cur.execute("SELECT offer_id, price, items_sold FROM stats WHERE raport_id = " + raport_id[0])
    rows = cur.fetchall()
    return rows

def select_sold_items_by_raport_id_and_offer_id(conn, raport_id, offer_id):
    cur = conn.cursor()
    cur.execute("SELECT items_sold FROM stats WHERE offer_id = " + str(offer_id) + " AND raport_id = " + str(raport_id[0]))
    rows = cur.fetchall()
    if(len(rows)==0):
        return -1
    else:
        return rows[0]

def select_stats_by_raport_id_and_key(conn, raport_id, name):
    cur = conn.cursor()
    cur.execute("SELECT offer_id, price, items_sold FROM stats WHERE raport_id = " + raport_id[0] + " AND offer_title LIKE '%"+name+"%'")
    rows = cur.fetchall()
    return rows