import schedule

import time

from Bot import book_paddle_automated
from Reservation import Reservation

def make_res(res):
    court = book_paddle_automated(res)
    """if reservation failed, try one more time """
    print(court)

    if (court == "fail"):
        print("retrying")
        court = book_paddle_automated(res)

    print("final: " + court)

def court1():
    CODE = "35780"
    DAY = ["1", "19"]  # [month, day]
    TIME = "15:00"
    COURT_INDEX = "1"
    NAME0 = "Taira, Kelly"
    NAME1 = "Krause, Ron"
    NAME2 = "Hoyt, Mark"

    res1 = Reservation(CODE, DAY, TIME, COURT_INDEX, NAME0, NAME1, NAME2)
    make_res(res1)


def court2():
    CODE = "23580"
    DAY = ["1", "19"]  # [month, day]
    TIME = "15:00"
    COURT_INDEX = "1" ## once a court is filled, it is no longer in the court list <td>s (it has become <th>),
                        # so the next open court will always have an index of 1
    NAME0 = "Flodin, TJ"
    NAME1 = "Flynn, Michael"
    NAME2 = "Bedell, Brendan"

    res2 = Reservation(CODE, DAY, TIME, COURT_INDEX, NAME0, NAME1, NAME2)
    make_res(res2)

court1()
court2()

while 1:
    schedule.run_pending()
    time.sleep(1)
