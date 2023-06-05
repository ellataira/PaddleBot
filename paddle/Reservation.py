from tennis.Util import Util


class Reservation :
    def __init__(self, code, day, time, court, name1, name2, name3):

        util = Util(0)  # 1 for tennis, 0 for paddle

        self.code = code
        self.day = util.calc_day_val(day)
        self.time = util.calc_time(time)
        self.court = court
        self.name1 = name1
        self.name2 = name2
        self.name3 = name3
        self.name4 = "Member filler/hold 1"

