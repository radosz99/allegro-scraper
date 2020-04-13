from fpdf import FPDF
from PIL import Image
import requests
import random
import math
import os
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
from io import BytesIO
from datetime import datetime
from matplotlib.backends.backend_pdf import PdfPages
import numpy as np


import DataBase

def generate_raport():
        
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", style = 'B', size = 13)
    path = "test"
    conn = DataBase.get_connection()
    raport_info = DataBase.select_all_prints(conn)[0:10]
    old_offer_id = raport_info[0][0]
    real_counter=0
    shift=0
    date_list=[]
    sold_items_list=[]
    th = pdf.font_size
    
    for x in range(len(raport_info)):
        print(str(int(x/len(raport_info)*100))+"%")
        if(x<len(raport_info)):
            date_list.append(raport_info[x][7][0:5])
            sold_items_list.append(raport_info[x][10])
            
            if(raport_info[x][0]==old_offer_id and x!=0):
                continue
            old_offer_id=raport_info[x][0]
            
        
        if(x!=0):
            #print("Dodany wykres, x = " + str(x) + ", real = " + str(real_counter))
            pdf.set_font("Arial", style = 'B', size = 9)
            pdf.cell(5)
            pdf.cell(200, 10, txt="Wystawca: ")
            pdf.set_font("Arial", style = 'I', size = 9)
            pdf.ln(0.001)
            pdf.cell(30)
            pdf.cell(200, 10, txt=raport_info[x-1][2])
            pdf.ln(th)
            
            pdf.set_font("Arial", style = 'B', size = 9)
            pdf.cell(5)
            pdf.cell(200, 10, txt="Numer oferty: ")
            pdf.set_font("Arial", style = 'I', size = 9)
            pdf.ln(0.001)
            pdf.cell(30)
            pdf.cell(200, 10, txt=raport_info[x-1][0])
            pdf.ln(th)
            
            pdf.set_font("Arial", style = 'B', size = 9)
            pdf.cell(5)
            pdf.cell(200, 10, txt="Cena: ")
            pdf.set_font("Arial", style = 'I', size = 9)
            pdf.ln(0.001)
            pdf.cell(30)
            pdf.cell(200, 10, txt=str(raport_info[x-1][3])+" PLN")
            pdf.ln(th)
            
            pdf.set_font("Arial", style = 'B', size = 9)
            pdf.cell(5)
            pdf.cell(200, 10, txt="Cena z wysylka: ")
            pdf.set_font("Arial", style = 'I', size = 9)
            pdf.ln(0.001)
            pdf.cell(30)
            pdf.cell(200, 10, txt=str(raport_info[x-1][4])+" PLN")
            pdf.ln(th)

            sponsored="NIE"
            if(raport_info[x-1][11]==1):
                sponsored="TAK"
                
            pdf.set_font("Arial", style = 'B', size = 9)
            pdf.cell(5)
            pdf.cell(200, 10, txt="Sponsorowana: ")
            pdf.set_font("Arial", style = 'I', size = 9)
            pdf.ln(0.001)
            pdf.cell(30)
            pdf.cell(200, 10, txt=sponsored)
            pdf.ln(th)
            
            pdf.ln(9*th)
            shift=shift+14*th
            

            minim = min(sold_items_list[0:len(sold_items_list)-1])
            minim = int(minim*0.99)
            maxim = max(sold_items_list[0:len(sold_items_list)-1])
            maxim = int(maxim*1.02)
            diff = maxim-minim
            if(diff<10):
                maxim = maxim+10-diff
            plt.bar(date_list[0:len(date_list)-1], sold_items_list[0:len(sold_items_list)-1],0.4)

            plt.xlabel('Daty raportow', labelpad=4, fontsize=13)
            plt.ylabel('Sprzedanych egzemplarzy', labelpad=18, fontsize=13)
            plt.ylim(int(minim), int(maxim))
            plt.gcf().set_size_inches(11.09, 6.05)
            xlocs, xlabs = plt.xticks()
            for i, v in enumerate(sold_items_list[0:len(sold_items_list)-1]):
                plt.text(xlocs[i]-(0.01*len(str(v))), v + v/2000, str(v))
            plt.savefig('plot'+str(real_counter)+'.png')
            plt.cla()
            
            pdf.image('plot'+str(real_counter)+'.png',70, 10+shift-16*th, 132,62,'PNG');
            os.remove('plot'+str(real_counter)+'.png')
            #plt.show()
            
            temp_item=sold_items_list[len(sold_items_list)-1]
            sold_items_list.clear()
            sold_items_list.append(temp_item)
            temp_item=date_list[len(date_list)-1]
            date_list.clear()
            date_list.append(temp_item)
            if((real_counter)%3==0):
                pdf.add_page()
                pdf.ln(3)
                shift=0
            else:
                pdf.line(10, shift+10, 200, shift+10)
                shift = shift+10
                pdf.ln(10)
                
            if(x>=len(raport_info)):
                break
            
        response = requests.get(raport_info[x][6])
        img = Image.open(BytesIO(response.content))
        img.save(path+str(x)+".png", "png")
        
        width, height = img.size
        width = int(width/8)
        height = int(height/8)
        pdf.image(path+str(x)+".png",20, 10+shift, width,height,'PNG');
        #+ '\t' +single_raport_info[8]
        pdf.set_font("Arial", style = 'B', size = 13)
        if(x==0):
            pdf.ln(3)
        pdf.cell(30)
        pdf.cell(200, 10, txt=raport_info[x][1])
        shift = shift+5*th
        pdf.ln(5*th)
        os.remove(path+str(x)+".png")
        real_counter=real_counter+1
    
    pdf.output("raport.pdf")



    
if __name__ == '__main__':
    generate_raport()

