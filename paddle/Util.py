class Util:
    def __init__(self, is_tennis):
        self.times = {}
        self.init_times(is_tennis)

    def init_times(self, is_tennis):
        """Initializes the time slot table for paddle or tennis."""
        if is_tennis:
            self.times = {
                "6:00": 1,
                "6:30": 2,
                "7:00": 3,
                "7:30": 4,
                "8:00": 5,
                "8:30": 6,
                "9:00": 7,
                "9:30": 8,
                "10:00": 9,
                "10:30": 10,
                "11:00": 11,
                "11:30": 12,
                "12:00": 13,
                "12:30": 14,
                "13:00": 15,
                "13:30": 16,
                "14:00": 17,
                "14:30": 18,
                "15:00": 19,
                "15:30": 20,
                "16:00": 21,
                "16:30": 22,
                "17:00": 23,
                "17:30": 24,
                "18:00": 25,
                "18:30": 26,
                "19:00": 27,
                "19:30": 28,
                "20:00": 29,
            }
        else:
            self.times = {
                "7:30": 3,
                "9:00": 4,
                "10:30": 5,
                "12:00": 6,
                "13:30": 7,
                "15:00": 8,
                "16:30": 9,
                "18:00": 10,
                "19:30": 11,
                "21:00": 12,
            }

    def calc_time(self, time):
        """Returns the row index for the given time."""
        return str(self.times[time])
