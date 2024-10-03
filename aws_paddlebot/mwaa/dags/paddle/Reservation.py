from paddle.Util import Util
class Reservation:
    def __init__(self, code, time, court, name1, name2, name3):
        util = Util(0)  # 1 for tennis, 0 for paddle
        self.code = code
        self.time = util.calc_time(time)
        self.court = court
        self.names = [name1, name2, name3, "Member filler/hold 1"]  # Pre-filled with placeholder name
