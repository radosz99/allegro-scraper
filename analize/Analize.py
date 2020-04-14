from data.connection import get_connection
from data.select import select_user_raports_id
from data.select import select_user_offers
from data.select import select_user_raports
from data.select import select_money_from_offer
from data.select import select_money_from_offer_without_mask
from data.select import select_raport_by_date_and_user
from data.select import select_stats_by_raport_id
from data.select import select_sold_items_by_raport_id_and_offer_id
from data.select import select_stats_by_raport_id_and_key
from analize.raport import get_string_date
import matplotlib.pyplot as plt


def convert_data(data):
    data_converted=[]
    for single_data in data:
        data_converted.append(str(single_data).replace('(','').replace(',','').replace(')',''))
    return data_converted

def get_raports_dates(conn, username):
    raports = select_user_raports(conn, username)
    raports_array=[]
    for single_raport in raports:
        raports_array.append(str(single_raport[0]) + '\n' + get_string_date(single_raport))
    return raports_array

def get_sales_raport(username, with_mask):
    conn = get_connection()
    raports = convert_data(select_user_raports_id(conn,username))
    offers = convert_data(select_user_offers(conn, username, len(raports)))
    raports_array = get_raports_dates(conn, username)
    sum_array = []
    for i in range(len(raports)):
        sum_array.append(0)
    for x in range (len(offers)):
        if (with_mask==True):
            money_offer_array = select_money_from_offer(conn, offers[x])
        else:
            money_offer_array = select_money_from_offer_without_mask(conn, offers[x])

        if(len(money_offer_array)==0):
            continue
        sum_current = int(money_offer_array[0][1]*money_offer_array[0][2])
        sum_array[0]=sum_array[0]+sum_current
        for y in range(len(raports)-1):
            try:
                diff = money_offer_array[y+1][2]-money_offer_array[y][2]
            except IndexError:
                diff =0
            if(diff<0):
                diff=0
            try:
                sum_offer_raport = int(money_offer_array[y+1][1]*(money_offer_array[y+1][2]-money_offer_array[y][2]))
            except IndexError:
                sum_offer_raport =0
            sum_array[y+1] = sum_array[y+1]+sum_offer_raport+sum_current
            sum_current=sum_current+sum_offer_raport

    plt.plot(raports_array, sum_array)
    plt.grid(True)
    plt.title('Zyski dla wybranych raportow')
    plt.xlabel('Numery raportow')
    plt.ylabel('Laczna zysk ze sprzedazy [PLN]')
    plt.show()


def get_raports_id(username, date1, date2):
    date1.replace(".0", ".")
    date2.replace(".0", ".")
    date1_conv = date1.split(".")
    date2_conv = date2.split(".")
    raport_1_id = select_raport_by_date_and_user(get_connection(), date1_conv[0], date1_conv[1],date1_conv[2],username)
    raport_2_id = select_raport_by_date_and_user(get_connection(), date2_conv[0], date2_conv[1],date2_conv[2],username) 
    return raport_1_id, raport_2_id

def get_difference_two_raports(username, date1, date2, name):
    raports_id = get_raports_id(username, date1, date2)
    raports_1_id_conv = remove_redundant_stuff_from_string(raports_id[0])
    raports_2_id_conv = remove_redundant_stuff_from_string(raports_id[1])
    if(name==''):
        offers = select_stats_by_raport_id(get_connection(), raports_2_id_conv)
    else:
        offers = select_stats_by_raport_id_and_key(get_connection(), raports_2_id_conv, name)
    difference=0
    #print(offers)
    for offer in offers:
        items_sold = remove_redundant_stuff_from_string(select_sold_items_by_raport_id_and_offer_id(get_connection(), raports_1_id_conv, offer[0]))
        if(int(items_sold)<0):
            continue
        diff = int(offer[2])-int(items_sold)
        if(diff<0):
            diff = 0
        difference = difference + int(diff*float(offer[1]))
        diff = 0
    return difference


def remove_redundant_stuff_from_string(string):
    return str(string).replace('(','').replace(',','').replace(')','').replace(']','').replace('[','')