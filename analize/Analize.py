from data.Connection import get_connection
from data.Select import select_all_offers
from data.Select import select_all_raports
from data.Select import select_raports_by_offer_id

def get_sales_difference(username):
    conn = get_connection()
    raports = select_all_raports(conn, username)
    info = []
    old_date = raports[0][7]
    old_hour = raports[0][8]
    for x in range (len(raports)-1):
        info =[]
        items = 0
        money = 0.0
        #TODO: add new table raports with date and id attributes
        while(raports[x][7]==old_date and raports[x][8]==old_hour):
            items = items + raports[x][10]
            money = money + items*raports[x][3]
            x=x+1
            if(x==len(raports)-1):
                break
        old_date = raports[x][7]
        old_hour = raports[x][8]
        print(items)
         
             