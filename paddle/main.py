import traceback
from datetime import date
from paddle import book_paddle_automated
from data import data


def make_res(res):
    print(
        "attempting to reserve 1 week in advance: \n"
        + "\nfor court "
        + res.court
        + "\nunder "
        + str(res.names)
        + "\ncode: "
        + res.code
        + "\n"
    )

    try:
        court = book_paddle_automated(res)
        """if reservation failed, try one more time """
        print("first attempt: " + court + "\n")

    except Exception as e:
        print("attempt failed, retrying...")

        try:
            court = book_paddle_automated(res)
        except Exception as e:
            print("Retry Failed: ", {"error": e})
            raise

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
