import numpy
from scan.Scanner import init
from data.Connection import get_connection
from analize.Raport import generate_raport
from analize.Analize import get_sales_difference
def scan():
    username="sport_i_styl"
    init(username, get_connection())

def raport():
    username="krawiectwoKM"
    min_items = 5
    generate_raport(min_items,username)

def sales_raport():
    username="krawiectwoKM"
    print(get_sales_difference(username))
if __name__ == "__main__":
    #scan()
    raport()
    #sales_raport()