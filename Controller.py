import numpy
from scan.Scanner import init
from data.Connection import get_connection
def main():
    username="Allegro"
    init(username, get_connection())

if __name__ == "__main__":
    main()