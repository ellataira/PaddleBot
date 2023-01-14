import schedule

import time

from Bot import book_paddle_automated
from Reservation import Reservation


def court1():
    CODE = "35780"
    DAY = ["1", "19"]  # [month, day]
    TIME = "15:00"
    COURT_INDEX = "2"
    NAME0 = "Taira, Kelly"
    NAME1 = "Krause, Ron"
    NAME2 = "Hoyt, Mark"

    res1 = Reservation(CODE, DAY, TIME, COURT_INDEX, NAME0, NAME1, NAME2)
    book_paddle_automated(res1)

def court2():
    CODE = "35780"
    DAY = ["1", "19"]  # [month, day]
    TIME = "15:00"
    COURT_INDEX = "2"
    NAME0 = "Taira, Kelly"
    NAME1 = "Krause, Ron"
    NAME2 = "Hoyt, Mark"


def main():

    """ Here we are using the schedule module to run this code every day at 9 AM"""

schedule.every().day.at("16:17:00").do(court1)
schedule.every().day.at("16:17:15").do(court2)

while 1:
    schedule.run_pending()
    time.sleep(1)
