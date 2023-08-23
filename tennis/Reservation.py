from Util import Util

class Reservation :
    def __init__(self, username, password, timeslot, court, duration, days_in_advance):

        util = Util(1)  # 1 for tennis

        self.username = username
        self.password = password
        self.timeslot = util.calc_time(timeslot)
        self.court = court
        self.duration = util.calc_duration(duration)
        self.days_in_advance = days_in_advance

