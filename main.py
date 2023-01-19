from datetime import date

import sys

from Bot import book_paddle_automated
from Reservation import Reservation

def make_res(res):
    print("attempting to reserve: \n" +
          "day: " + res.day + " at " + res.time +
          "\nfor court " + res.court +
          "\nunder " + res.name1 + ", " + res.name2 + ", " + res.name3 +
          "\ncode: " + res.code + "\n")

    court = book_paddle_automated(res)
    """if reservation failed, try one more time """
    print("first attempt: " + court + "\n")

    if (court == "fail"):
        print("attempt failed, retrying...")
        court = book_paddle_automated(res)

    print("final status: " + court + "\n---------------------------------")

def court1():
    CODE = "35780"
    DAY = ["1", "26"]  # [month, day]
    TIME = "13:30"
    COURT_INDEX = "2"
    NAME0 = "Taira, Kelly"
    NAME1 = "Krause, Ron"
    NAME2 = "Hoyt, Mark"

    res1 = Reservation(CODE, DAY, TIME, COURT_INDEX, NAME0, NAME1, NAME2)
    make_res(res1)


def court2():
    CODE = "23580"
    DAY = ["1", "26"]  # [month, day]
    TIME = "13:30"
    COURT_INDEX = "2" ## once a court is filled, it is no longer in the court list <td>s (it has become <th>),
                        # so the next open court will always have an index of 1
    NAME0 = "Flodin, TJ"
    NAME1 = "Lundak, Dan"
    NAME2 = "Condon, Sean"

    res2 = Reservation(CODE, DAY, TIME, COURT_INDEX, NAME0, NAME1, NAME2)
    make_res(res2)

sys.stdout = open('/Users/ellataira/Desktop/PaddleBot/paddle_bot_out.txt', 'w')
print(str(date.today()) + "\n\n")
court1()
court2()
sys.stdout.close()
