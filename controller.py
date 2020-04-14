import numpy
from Allegro_scanner.scan.scanner import init
from Allegro_scanner.data.connection import get_connection
from Allegro_scanner.analize.raport import generate_raport
from Allegro_scanner.analize.analize import get_sales_raport
from Allegro_scanner.analize.analize import get_difference_two_raports
def scan():
    username="blogomania"
    init(username, get_connection())

def raport():
    username="sport_i_styl"
    min_items = 5
    generate_raport(min_items,username)

def sales_raport():
    username="sport_i_styl"
    get_sales_raport(username,True)

def difference_between_raports():
    username = "sport_i_styl"
    print(str(get_difference_two_raports(username,'13.04.2020', '14.04.2020','Spodnie')) + " zł")

if __name__ == "__main__":
    #scan()
    #raport()
    #sales_raport()
    difference_between_raports()