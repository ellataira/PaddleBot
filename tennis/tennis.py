
from selenium.webdriver.support.select import Select
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


def book_tennis_automated(res):
    USERID = res.username # TODO
    PASSWORD = res.password
    TIMESLOT = res.timeslot
    COURT = res.court
    DURATION = res.duration
    DAYS_ADV = res.days_in_advance


    """ Initialising a Chrome instance """
    driver = webdriver.Chrome(ChromeDriverManager().install())

    """ Enter the URL of the website"""
    driver.get("https://sites.onlinecourtreservations.com/reservations")
    driver.implicitly_wait(5)

    """ select location """
    select_location = Select(driver.find_element(By.NAME, "facility_num"))
    select_location.select_by_value("188") # 188 corresponds to 'RFTC'
    select_location_button = driver.find_element(By.NAME, "btnSubmit")
    select_location_button.click()

    """sign in """
    sign_in = driver.find_element(By.XPATH, "/html/body/div[1]/form/p[1]/table[1]/tbody/tr/td[2]/nav/ul/li[2]/a")
    sign_in.click()

    username = driver.find_element(By.NAME, "user_id")
    username.send_keys(USERID)

    pw = driver.find_element(By.NAME, "password")
    pw.send_keys(PASSWORD)

    enter = driver.find_element(By.XPATH, '//*[@id="CheckUser"]')
    enter.click()

    """navigate to time slot view """
    # use util method to find correct row by dict
    timeslot_path = '/html/body/div[1]/form/p[2]/table/tbody/tr[{}]/td[1]'.format(TIMESLOT)
    timeslot_view = driver.find_element(By.XPATH, timeslot_path)
    timeslot_view.click()

    """find date and court"""
    # date = 1 (today) + days in advance
    # e.g. to book for one week ahead, date = 1 + 7 = 8
    book_on_date = "/html/body/form/p[2]/table/tbody/tr[{}]".format(str(int(DAYS_ADV) + 1))
    book_on_date_at_court = book_on_date + '/td[{}]'.format(str(int(COURT) + 1))

    timeslot = driver.find_element(By.XPATH, book_on_date_at_court)
    timeslot.click()

    """fill in reservation details """
    select_duration = Select(driver.find_element(By.NAME, "Duration"))
    select_duration.select_by_value(DURATION)

    submit_res = driver.find_element(By.ID, "SaveReservation")
    submit_res.click()

    driver.quit()
    return "complete"

    """
    TODO: 
    navigate to time slot and click to see calendar     
        > 6:00
    find row by date 
        > 8/23 = row 5 , etc. 
        today's row is at tr[1]
            /html/body/form/p[2]/table/tbody/tr[1]
        so, for one week in advance, go to  (today + 7)
            /html/body/form/p[2]/table/tbody/tr[8]

    find court 

        c3 with no prior bookings: /html/body/form/p[2]/table/tbody/tr[5]/td[4]
        c3 with prior booking: /html/body/form/p[2]/table/tbody/tr[4]/td[4]
        c4 no prior: /html/body/form/p[2]/table/tbody/tr[5]/td[5]
        c4 prior: /html/body/form/p[2]/table/tbody/tr[4]/td[5]

        /td[1 + court_no] 

    click 

    fill in res details 

    """
