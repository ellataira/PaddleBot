
class Util:

    def __init__(self, paddle):
        self.times = {}
        self.init_times(paddle)

    def init_times(self, bin):
        # 0 = paddle, 1 = tennis
        if bin == 1:
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
            "20:00": 29
        }
        if bin == 0:
            self.times = {"": 1,
                 "": 2,
                 "7:30": 3,
                 "9:00": 4,
                 "10:30": 5,
                 "12:00": 6,
                 "13:30": 7,
                 "15:00": 8,
                 "16:30": 9,
                 "18:00": 10,
                 "19:30": 11,
                 "21:00": 12}

    def calc_time(self, time):
        """ROW-TO-TIME-SLOT KEY, indexed at 1 (tr)
        """
        return str(self.times[time])


    def calc_day_val(self, day):
        # start = 218  # 218 is value for jan 14, 2023 -- not sure how else to deal with select
        start = 31  # 218 is value for oct 4, 2023 -- not sure how else to deal with select
        m, d = int(day[0]), int(day[1])

        months = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

        # if m == 1:
        #     return str(start + (d - 14))

        if m == 10: # if october
            return str(start + (d - 4))

        # start += 17  # end month of january --- 31 - 14 = 17

        start += 27 # end month of oct -- 31 - 4 = 27

        if m < 9:
            # finish up 2023 months
            start += months[10]
            start += months[11]
            # then can add 2024 months
            for i in range(0, m - 1):
                start += months[i]

        if m > 10:
            for i in range(10, m - 1):
                start += months[i]

        start += d
        return str(start)


    def calc_duration(self, duration):
        durs = {
            "0.5": 1,
            "1": 2,
            "1.5": 3
        }

        return str(durs[duration])




u = Util(0)
print(u.calc_day_val(["3", "1"]))

