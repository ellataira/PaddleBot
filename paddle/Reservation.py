from Util import Util


class Reservation:
    def __init__(
        self,
        code: str,
        time: str,
        court: str,
        name1: str,
        name2: str,
        name3: str,
        name4: str = "Member filler/hold 1",
        days_in_advance: int = 7,
    ):
        util = Util(0)  # 1 for tennis, 0 for paddle
        self.days_in_advance = days_in_advance
        self.code = code
        self.time = util.calc_time(time)
        self.court = court
        self.names = [name1, name2, name3, name4]  # Pre-filled with placeholder name
