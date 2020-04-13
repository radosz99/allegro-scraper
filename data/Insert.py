import sqlite3
from sqlite3 import Error

def insert_print(conn, single_print):
    sql = ''' INSERT INTO stats(offer_id,offer_title,price, price_with_ship,username,offer_url,offer_img_url,analize_day,analize_hour,buyers,items_sold, promoted)
              VALUES(?,?,?,?,?,?,?,?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, single_print)
    conn.commit()
    return cur.lastrowid

def insert_offer(conn, single_offer):
    sql= ''' UPDATE offers
                SET  raports_quantity = (SELECT raports_quantity
                                        FROM offers
                                        WHERE offer_id = '''+single_offer[0]+''')+1 
                WHERE offer_id = ''' + single_offer[0]
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()


    sql = ''' INSERT INTO offers(offer_id, username, raports_quantity) 
                SELECT '''+ single_offer[0] + ''',' ''' + single_offer[2] + '''', 1  
                WHERE NOT EXISTS(SELECT 1 FROM offers WHERE offer_id = '''+ single_offer[0]+''')
            '''
    
    cur.execute(sql)
    conn.commit()
    sql = ''' UPDATE offers
                SET first_items_sold = '''+ str(single_offer[1]) +'''
                WHERE first_items_sold IS NULL and offer_id = ''' + single_offer[0]
    cur.execute(sql)
    conn.commit()

    sql = ''' UPDATE offers
                SET last_items_sold = '''+ str(single_offer[1])+'''
                WHERE offer_id = ''' + single_offer[0]
    cur.execute(sql)
    conn.commit()


    return cur.lastrowid