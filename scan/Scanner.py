import time
import math
import functools 
import urllib.request as urllib2
import urllib.error as url_error
from datetime import datetime
import data.Insert as DataBase
import data.Update as DataBaseUpdate
 
def find_element(source, substring, shift):
    position = source.find(substring,0,len(source))+len(substring)
    text =  source[ position : position + shift]
    return text

def get_source_code(url):
    print(url)
    start=time.time()
    text=''
    try:
        response = urllib2.urlopen(url)
        text = str(response.read())
    except url_error.HTTPError as f:
        print("Brak odpowiedzi od serwera")
        print('Error code: ', f.code)
    except url_error.URLError as e:
        print("Zły url")
        print('Error code: ', e.reason)

    end=time.time()
    #print("Odebranie " + str(end-start))
    return text

def get_number_of_offers(source_code):
    text = find_element(source_code,"span data-role=\"counter-value\">", 10)
    text = text.split("<")
    return int(text[0].replace(" ", ""))

def make_page_link(user_site, site_number):
    return user_site + "?p="+str(site_number)+"&order=qd"

def add_user_to_database(username,conn):
    source_code = get_source_code("https://allegro.pl/uzytkownik/"+username)
    if(find_element_position(source_code, "Nie znale\\xc5\\xbali\\xc5\\x9bmy u")!=-1):
        return False
    else:
        user_info = get_user_info(source_code,get_source_code("https://allegro.pl/uzytkownik/"+username+"/oceny"), username)
        DataBase.insert_user(conn,user_info)
        return True

def get_user_info(source_code, source_code_assessment, username):
    offers_quantity = get_number_of_offers(source_code)
    position = find_element_position(source_code_assessment, "\"recommendCount\":")
    text = source_code_assessment[position+17:position+100]
    text_parts = text.split(",")
    recommend_count = int(text.split(",")[0])
    not_recommend_count = int(text_parts[1].split(":")[1])
    return (username, recommend_count,not_recommend_count,offers_quantity)

def navigate_to_user_wall(username,conn,raport_id):
    offers_quantity=0

    for x in range(get_page_numbers(get_source_code(make_page_link("https://allegro.pl/uzytkownik/"+username, 1)))):
        arrays_for_database = parse_page(get_source_code(make_page_link("https://allegro.pl/uzytkownik/"+username, x+1)), username, conn,raport_id)
        offers_array = arrays_for_database[0]
        raports_array = arrays_for_database[1]
        for single_offer in offers_array:
            offers_quantity=offers_quantity+1
            print(single_offer)
            DataBase.insert_offer(conn,(single_offer[0],single_offer[1],single_offer[2]))
        for single_raport in raports_array:
            print(single_raport)
            DataBase.insert_print(conn, single_raport)

    DataBaseUpdate.update_raports(conn, offers_quantity, raport_id)
               
def parse_page(page_source, username, conn, raport_id):
    promo_quantity = get_promo_offers_on_page_quantity(page_source)
    offers_quantity = get_offers_on_page_quantity(page_source)
    print("Ofert - " + str(offers_quantity) + ", ofert bez sprzedazy - " + str(get_offers_with_no_sales_quantity_on_page(page_source)))
    price_info = get_offers_price_with_ship(page_source, offers_quantity)
    sale_array = get_offers_array_sales_on_page(page_source, offers_quantity)
    link_array = get_offers_links(offers_quantity, page_source)
    image_array = get_offer_image_links(offers_quantity, page_source)  
    return parse_data(link_array,image_array, promo_quantity, username, sale_array,price_info[0], price_info[1],raport_id)
    
def get_offers_price_with_ship(source, quantity):
    price_array=[0 for i in range(quantity)]
    price_with_ship_array=[0 for i in range(quantity)]
    
    for x in range(quantity):
        position = find_element_position(source, "amount\\\\\":\\\\\"")
        text_parts=source[position:position+200].split("\\\\\"")
        source=source[position+10:len(source)-1]
        price_array[x]=text_parts[2]
        
        text_parts=text_parts[12].split("u003E")
        price = text_parts[1].split(" z")[0]
        
        price = price.replace(" ","")
    
    
        if(price[0:7]=='darmowa'):
            price_with_ship_array[x]=price_array[x]
        else:
            price_with_ship_array[x]=price.replace(",",".")

    return price_with_ship_array, price_array
        
               
def get_offers_on_page_quantity(source):
    counter=0
    link_info = make_offer_link(source)
    new_position = int(link_info[1]) 
    while new_position!=-1:
        counter=counter+1
        source = source[int(new_position)+2 : len(source)-1]
        link_info = make_offer_link(source)
        new_position = int(link_info[1]) 
              
    return int(counter/2)
    
def get_offer_image_links(offers_quantity,source):
    image_array=[0 for i in range(offers_quantity)]
    for x in range(offers_quantity):
        link_info =make_image_link_universal(source)
        #link_info = make_image_link(source)
        source = source[int(link_info[1]) + 20 : len(source)-1]
        image_array[x]=link_info[0]
    return image_array    
    
    
def make_image_link(source_code):
    position = find_element_position(source_code,"img data-src=\"")
    text =  source_code[ position + 14 : position + 100]
    text = text.split("\" alt=\"\" ")
    link_info = (text[0], position)
    return link_info

def make_image_link_universal(source_code):
    position = find_element_position(source_code,"allegroimg.com/s128")
    text =  source_code[ position -15: position + 60]
    text = text.split("\"")
    link_info = (text[1], position)
    return link_info
    
    
def get_offers_links(offers_quantity, source):
    link_array =[0 for i in range(offers_quantity)]
    for x in range(offers_quantity):
        link_info = make_offer_link(source)
        source = source[link_info[1] + 2 : len(source)-1]
        link_array[x] = link_info[0]
        link_info = make_offer_link(source)
        source = source[link_info[1] + 2 : len(source)-1]
    return link_array

def parse_data(link_array, image_array, promo_quantity, username, sales_array,price_with_ship_array, price_array,raport_id):
    offers_array=[]
    raports_array=[]
    for x in range(len(link_array)):
        if(promo_quantity>0):
            promoted = 1
            promo_quantity = promo_quantity-1
        else:
            promoted = 0
        link_parts = link_array[x].split("-")
        offer_id = link_parts[len(link_parts)-1]
        if(sales_array[x]==0):
            sold_info_array=(0,0)
        else:
            sold_info_array = get_sold_items_quantity(get_source_code(link_array[x]))
        single_print = (offer_id, get_title_from_url(link_array[x], offer_id), price_array[x], price_with_ship_array[x], link_array[x], image_array[x], raport_id, sold_info_array[0], sold_info_array[1], promoted)
        raports_array.append(single_print)
        offers_array.append((offer_id,sold_info_array[1],username))
    return offers_array, raports_array
    
def find_element_position(source, substring):
    position = source.find(substring,0,len(source))
    return position


def make_offer_link(source_code):
    position = find_element_position(source_code,"https://allegro.pl/oferta/")
    text =  source_code[ position : position + 100]
    text = text.split("\" class=\"")
    link_info = (text[0], position)
    return link_info
    
    
def get_page_numbers(source_code):
    text = find_element(source_code, "data-maxpage=\"",10)
    split_text = text.split("\"")
    return int(split_text[0])

def get_sold_items_quantity(source):
    text = find_element(source,"popularity\":{\"label\":", 50)
    sold_info = ()
    text = text[1:len(text)-1]
    if(text[0:3]=="ull" or text[0:4] == "Nikt"):
        sold_info=(0,0)
        return sold_info
    else:
        text2 = text.split(" ")
        sold_info = (int(text2[0]), int(text2[3]))
        return sold_info
 
def get_price(source):
    text = find_element(source,"aria-label=\"cena ", 50)
    text_parts = text.split(" z")
    price_main = text_parts[0].replace(" ","")
    price_sub = text_parts[1].split(" ")[1]
    price=float(price_main+"."+price_sub)
    return price
    
def get_promo_offers_on_page_quantity(source):
    position = find_element_position(source, "Oferty promowane" )
    if(position==-1):
        return 0
    source = source[position+5:len(source)-1]
    position = find_element_position(source, "Oferty" )
    link_source = source[0:position+1]
       
    link_parts = link_source.split("href")
    quantity = int((len(link_parts)-1)/2)
    return quantity
 
def get_offers_with_no_sales_quantity_on_page(source):
    quantity = 0
    position=0
    while position!=-1:
        position = find_element_position(source, "],\\\"bidInfo\\\":\\\"\\\",\\\"timingInfo")
        if(position!=-1):
            quantity=quantity+1
        source = source[position+5:len(source)-1]
    return quantity
    
    
def get_offers_array_sales_on_page(source, offers_quantity):
    sales_array=[0 for i in range(offers_quantity)]
    for x in range(offers_quantity):
        position = find_element_position(source, "bidInfo")
        text = source[position:position+100]
        source = source[position+12:len(source)-1]
        text_parts = text.split("bidInfo\\\\\":\\\\\"")
        if(text_parts[1][0]!="\\"):
            sales_array[x]=1
        else:
            sales_array[x]=0
    return sales_array
        
def get_title_from_url(url, offer_id):
    url_without_offer_id = url.split(str(offer_id))
    url_without_offer_id = url_without_offer_id[0].split("oferta/")
    title=url_without_offer_id[1].replace("-"," ")
    list1 = list(title)
    list1[0] = title[0].upper()
    for x in range(len(title)-2):
        if(title[x]==" "):
            list1[x+1] = title[x+1].upper()
            
    title = ''.join(list1[0:len(list1)-1])    
    return title
       
def init(username, conn):
    if(add_user_to_database(username,conn)==False):
        print("Nie ma takiego uzytkownika!")
        return
    current_time = datetime.now().strftime("%d. %m.%Y.%H.%M").lstrip("0").replace(" 0", "")
    raport_id = int(DataBase.insert_raport(current_time, conn, username))

    start = time.time()
   
    navigate_to_user_wall(username, conn,raport_id)
    end = time.time()
    print(end - start)
