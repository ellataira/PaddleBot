from Util import Util


class Reservation :
    def __init__(self, username, password, timeslot, court, duration ):

        util = Util(0)  # 1 for paddle

        self.username = username
        self.password = password
        self.timeslot = util.calc_time(timeslot)
        self.court = court
        self.duration = util.calc_duration(duration)

