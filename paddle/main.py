import traceback
from datetime import date
from paddle import book_paddle_automated
from data import data


def make_res(res):
    print("attempting to reserve: \n" +
          "converted_day: " + str(res.day) + " at " + res.time +
          "\nconverted day to " + res.converted_day +
          "\nfor court " + res.court +
          "\nunder " + res.name1 + ", " + res.name2 + ", " + res.name3 +
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

    court1()
    court2()
