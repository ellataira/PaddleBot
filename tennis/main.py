from datetime import date
import sys
from data import data
from tennis import book_tennis_automated


def make_res(res):
    print("attempting to reserve: \n" +
          "time: " + res.timeslot +
          "\nfor court " + res.court +
          "\nunder " + res.username  +
          "\npw: " + res.password + "\n")

    court = book_tennis_automated(res)
    """if reservation failed, try one more time """
    print("first attempt: " + court + "\n")

    if (court == "fail"):
        print("attempt failed, retrying...")
        court = book_tennis_automated(res)

    print("final status: " + court + "\n---------------------------------")

def court1():
    ## court data in .gitignore file which contains Reservation.py()s of booking info
    make_res(data.COURT1)


def court2():
    make_res(data.COURT2)

sys.stdout = open('/tennis/tennis_bot_out.txt', 'w')
print(str(date.today()) + "\n\n")
court1()
# court2()
sys.stdout.close()
