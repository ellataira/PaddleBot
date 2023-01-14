from Bot import book_paddle_automated
from Util import Util


class Reservation :
    def __init__(self, code, day, time, court, name1, name2, name3):
        self.code = code
        self.day = Util.calc_day_val(day)
        self.time = Util.calc_time(time)
        self.court = court
        self.name1 = name1
        self.name2 = name2
        self.name3 = name3
        self.name4 = "Member filler/hold 1"

