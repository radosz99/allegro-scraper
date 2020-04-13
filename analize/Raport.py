from fpdf import FPDF
from PIL import Image
import requests
import random
import math
import os
import matplotlib.pyplot as plt
from data.Connection import get_connection
from data.Select import select_all_offers
from data.Select import select_raports_by_offer_id
from data.Select import select_user_raports
from matplotlib.ticker import FuncFormatter
from io import BytesIO
from datetime import datetime
from matplotlib.backends.backend_pdf import PdfPages
import numpy as np

def generate_raport(min_items, username):
    conn = get_connection()
    pdf = FPDF()
    pdf.add_font('FreeSansBold', '', 'Allegro_scanner/analize/freesansbold.ttf', uni=True)
    pdf.add_font('FreeSans', '', 'Allegro_scanner/analize/freesans.ttf', uni=True)
    pdf.add_page() 
    pdf.set_font('freesansbold', size = 36)
    pdf.ln(15)
    pdf.cell(190, 10, 'Raport sprzedażowy', 0, 0, 'C')
    pdf.set_font('freesans', size = 20)
    pdf.ln(15)
    pdf.cell(190, 10, username, 0, 0, 'C')
    pdf.ln(65)
    pdf.cell(190, 10, 'Daty poszczególnych raportów:', 0, 0, 'C')
    pdf.ln(15)

    raports = select_user_raports(conn,username)
    for raport in raports:
        print(get_string_date(raport))
        pdf.cell(70)
        pdf.set_font('freesansbold', size = 13)
        pdf.cell(100, 10, str(raport[0])+' - ')
        pdf.ln(0.0001)
        pdf.cell(80)
        pdf.set_font('freesans', size = 13)
        pdf.cell(200, 10, get_string_date(raport))
        pdf.ln(10)



    pdf.add_page()  
    pdf.set_font("Arial", style = 'B', size = 13)
   
    real_counter=0
    shift=0
    select_offers = select_all_offers(conn, username, min_items)
    th = pdf.font_size  
    for x in range (len(select_offers)):
        print(str(int(x/len(select_offers)*100))+"%")

        offer_id = str(select_offers[x]).split("'")[0]
        offer_id = offer_id.replace("(","")
        offer_id = offer_id.replace(",","")
        offer_id = offer_id.replace(")","")
        select_raports = select_raports_by_offer_id(conn,offer_id)
        date_list=[]
        sold_items_list=[]
        for y in range (len(select_raports)):
            date_list.append(str(select_raports[y][6]))
            sold_items_list.append(select_raports[y][8])
        

        response = requests.get(select_raports[0][5])
        img = Image.open(BytesIO(response.content))
        img.save("test"+str(x)+".png", "png")
        
        width, height = img.size
        width = int(width/8)
        height = int(height/8)
        pdf.image("test"+str(x)+".png",20, 10+shift, width,height,'PNG')
        #+ '\t' +single_raport_info[8]
        pdf.set_font("Arial", style = 'B', size = 13)
        if(x==0):
            pdf.ln(3)
        pdf.cell(30)
        pdf.cell(200, 10, txt=select_raports[0][1])
        shift = shift+5*th
        pdf.ln(5*th)
        os.remove("test"+str(x)+".png")

        pdf.set_font("Arial", style = 'B', size = 9)
        pdf.cell(5)
        pdf.cell(200, 10, txt="Numer oferty: ")
        pdf.set_font("Arial", style = 'I', size = 9)
        pdf.ln(0.001)
        pdf.cell(30)
        pdf.cell(200, 10, txt=str(select_raports[0][0]))
        pdf.ln(th)
            
        pdf.set_font("Arial", style = 'B', size = 9)
        pdf.cell(5)
        pdf.cell(200, 10, txt="Cena: ")
        pdf.set_font("Arial", style = 'I', size = 9)
        pdf.ln(0.001)
        pdf.cell(30)
        pdf.cell(200, 10, txt=str(select_raports[0][2])+" PLN")
        pdf.ln(th)
            
        pdf.set_font("Arial", style = 'B', size = 9)
        pdf.cell(5)
        pdf.cell(200, 10, txt="Cena z wysylka: ")
        pdf.set_font("Arial", style = 'I', size = 9)
        pdf.ln(0.001)
        pdf.cell(30)
        pdf.cell(200, 10, txt=str(select_raports[0][3])+" PLN")
        pdf.ln(th)

        sponsored="NIE"
        if(select_raports[0][9]==1):
            sponsored="TAK"
                
        pdf.set_font("Arial", style = 'B', size = 9)
        pdf.cell(5)
        pdf.cell(200, 10, txt="Sponsorowana: ")
        pdf.set_font("Arial", style = 'I', size = 9)
        pdf.ln(0.001)
        pdf.cell(30)
        pdf.cell(200, 10, txt=sponsored)
        pdf.ln(th)
                    
        pdf.ln(10*th)
        shift=shift+14*th
            

        minim = min(sold_items_list[0:len(sold_items_list)])
        minim = int(minim*0.99)
        maxim = max(sold_items_list[0:len(sold_items_list)])
        maxim = int(maxim*1.02)
        diff = maxim-minim
        if(diff<10):
            maxim = maxim+10-diff
        plt.bar(date_list[0:len(date_list)], sold_items_list[0:len(sold_items_list)],0.4)

        plt.xlabel('Numery raportow', labelpad=4, fontsize=13)
        plt.ylabel('Sprzedanych egzemplarzy', labelpad=18, fontsize=13)
        plt.ylim(int(minim), int(maxim))
        plt.gcf().set_size_inches(11.09, 6.05)
        xlocs, xlabs = plt.xticks()
        for i, v in enumerate(sold_items_list[0:len(sold_items_list)]):
            plt.text(xlocs[i]-(0.01*len(str(v))), v + v/2000, str(v))
        plt.savefig('plot'+str(real_counter)+'.png')
        plt.cla()
            
        pdf.image('plot'+str(real_counter)+'.png',70, 10+shift-16*th, 132,62,'PNG')
        os.remove('plot'+str(real_counter)+'.png')
        #plt.show()
            
        temp_item=sold_items_list[len(sold_items_list)-1]
        sold_items_list.clear()
        sold_items_list.append(temp_item)
        temp_item=date_list[len(date_list)-1]
        date_list.clear()
        date_list.append(temp_item)
        if((x+1)%3==0):
            pdf.add_page()
            pdf.ln(3)
            shift=0
        else:
            pdf.line(10, shift+10, 200, shift+10)
            shift = shift+10
            pdf.ln(10)
        
        real_counter=real_counter+1
    
    pdf.output("raport_" +username+".pdf")


def get_string_date(integers_date):
    string_date=""
    if(len(str(integers_date[3]))<2):
        string_date=string_date+'0'+str(integers_date[3])
    else:
        string_date=string_date+str(integers_date[3])
    string_date=string_date+"."
    if(len(str(integers_date[4]))<2):
        string_date=string_date+'0'+str(integers_date[4])
    else:
        string_date=string_date+str(integers_date[4])
    string_date=string_date+"."+str(integers_date[5])+" "
    if(len(str(integers_date[6]))<2):
        string_date=string_date+'0'+str(integers_date[6])
    else:
        string_date=string_date+str(integers_date[6])
    string_date=string_date+":"
    if(len(str(integers_date[7]))<2):
        string_date=string_date+'0'+str(integers_date[7])
    else:
        string_date=string_date+str(integers_date[7])
    return string_date
