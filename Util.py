from datetime import date

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select


class Util:

    def calc_time(time):
        NUM_ROWS = 12  ## including top rows with date selector and column names
        """ROW-TO-TIME-SLOT KEY, indexed at 1 (tr)
        """
        times = {"": 1,
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

        return str(times[time])

    def calc_day_val(day):
        start = 218  # 218 is value for jan 14, 2023 -- not sure how else to deal with select
        m, d = int(day[0]), int(day[1])

        months = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 20, 31]

        if m == 1:
            return str(start + (d - 14))

        start += 17  # end month of january
        for i in range(1, m - 1):
            start += months[i]

        start += d
        return str(start)
