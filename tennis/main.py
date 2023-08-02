import traceback
from datetime import date
from data import data
from tennis import book_tennis_automated


def make_res(res):
    print("attempting to reserve: \n" +
          "time: " + res.timeslot +
          "\nfor court " + res.court +
          "\nunder " + res.username  +
          "\npw: " + res.password + "\n")

    traceback.print_exc()

    book_tennis_automated(res)

def court1():
    ## court data in .gitignore file which contains Reservation.py()s of booking info
   make_res(data.COURT1)

def court2():
    make_res(data.COURT2)

def court3():
   make_res(data.COURT3)


if __name__ == "__main__":
    print(str(date.today()) + "\n\n")
    try:
        court1()
    except:
        print("court 1 failed\n")

    try:
        court2()
    except:
        print("court 2 failed\n")

    try:
        court3()
    except:
        print("court 3 failed\n")
