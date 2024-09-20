import traceback
from datetime import date
from paddle import book_paddle_automated
from data import data


def make_res(res):
    print("attempting to reserve 1 week in advance: \n" +
          "\nfor court " + res.court +
          "\nunder " + str(res.names) +
          "\ncode: " + res.code + "\n")

    court = book_paddle_automated(res)
    """if reservation failed, try one more time """
    print("first attempt: " + court + "\n")

    traceback.print_exc()

    if (court == "fail"):
        print("attempt failed, retrying...")
        court = book_paddle_automated(res)

    print("final status: " + court + "\n---------------------------------")

def court1():
    ## court data in .gitignore file which contains Reservation.py()s of booking info
    make_res(data.COURT1)

def court2():
    make_res(data.COURT2)


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
