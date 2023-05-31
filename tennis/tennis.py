
from selenium.webdriver.support.select import Select
from selenium import webdriver
from selenium.webdriver.common.by import By


def book_tennis_automated(res):
    USERID = res.username # TODO
    PASSWORD = res.password
    TIMESLOT = res.timeslot
    COURT = res.court
    DURATION = res.duration


    """ Initialising a Chrome instance """
    driver = webdriver.Chrome()

    """ Enter the URL of the website"""
    driver.get("https://sites.onlinecourtreservations.com/reservations")
    driver.implicitly_wait(10)

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

    """ go to date first """
    # skip forward by 1 week
    next_week = driver.find_element(By.ID, "NextWeek")
    next_week.click()

    """calculating coordinate of court-timeslot object in table """
    # select timeslot
    timeslot_path = '/html/body/div[1]/form/p[2]/table/tbody/tr[{}]'.format(TIMESLOT)
    # the court column index is court_number + 1
    timeslot_with_court = timeslot_path + '/td[{}]'.format(str(int(COURT) + 1))

    timeslot = driver.find_element(By.XPATH, timeslot_with_court)
    timeslot.click()
    driver.implicitly_wait(5)

    """fill in reservation details """
    select_duration = Select(driver.find_element(By.NAME, "Duration"))
    select_duration.select_by_value(DURATION)

    submit_res = driver.find_element(By.ID, "SaveReservation")
    submit_res.click()
    driver.implicitly_wait(5)

    """check if the reservation passed """
    try :
        driver.find_element(By.XPATH, "//*[contains(text(),'Success')]")
    except:
        return "fail"

    driver.quit()
    return "complete"

