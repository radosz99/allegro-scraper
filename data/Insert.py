import sqlite3
from sqlite3 import Error

def insert_print(conn, single_raport):
    sql = ''' INSERT INTO stats(offer_id,offer_title,price, price_with_ship,offer_url,offer_img_url,raport_id,buyers,items_sold, promoted)
              VALUES(?,?,?,?,?,?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, single_raport)
    conn.commit()
    return cur.lastrowid

def insert_user(conn, single_user):
    sql = ''' INSERT INTO users(username) 
                SELECT '''+"'"+ single_user[0] + ''''
                WHERE NOT EXISTS(SELECT 1 FROM users WHERE username = ''' + "'" +single_user[0]+'''')
            '''
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()

    sql= ''' UPDATE users SET recommend_count = ''' + str(single_user[1]) + ''', not_recommend_count = ''' + str(single_user[2])+''',
                offers_quantity = ''' + str(single_user[3]) + '''
                WHERE username = ''' + "'" + single_user[0] + '''' '''
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()

    return cur.lastrowid

def insert_offer(conn, single_offer):
    sql= ''' UPDATE offers
                SET  raports_quantity = (SELECT raports_quantity
                                        FROM offers
                                        WHERE id = '''+single_offer[0]+''')+1 
                WHERE id = ''' + single_offer[0]
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()


    sql = ''' INSERT INTO offers(id, user_id, raports_quantity) 
                SELECT '''+ single_offer[0] + ''', (SELECT id FROM users WHERE username = ''' +"'" + single_offer[2] +''''), 1  
                WHERE NOT EXISTS(SELECT 1 FROM offers WHERE id = '''+ single_offer[0]+''')
            '''
    cur.execute(sql)
    conn.commit()
    sql = ''' UPDATE offers
                SET first_items_sold = '''+ str(single_offer[1]) +'''
                WHERE first_items_sold IS NULL and id = ''' + single_offer[0]
    cur.execute(sql)
    conn.commit()

    sql = ''' UPDATE offers
                SET last_items_sold = '''+ str(single_offer[1])+'''
                WHERE id = ''' + single_offer[0]
    cur.execute(sql)
    conn.commit()


    return cur.lastrowid

def insert_raport(data, conn,username):
    data_parts = data.split(".")
    sql = ''' INSERT INTO raports(user_id, offers_quantity, day, month, year, hour, minutes) 
                VALUES((SELECT id FROM users 
                        WHERE username = ''' + "'" + username + ''''), 0, '''+ data_parts[0] + ''', '''+ data_parts[1] + '''
                        , ''' + data_parts[2] + ''', '''+ data_parts[3] + ''', '''+ data_parts[4] + ''')
            '''
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()
    return cur.lastrowid