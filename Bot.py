import datetime

from selenium.webdriver.support.select import Select
from selenium import webdriver
from selenium.webdriver.common.by import By


def book_paddle_automated(res):
    CODE = res.code
    DAY = res.day
    TIME_INDEX = res.time
    COURT_INDEX = res.court
    NAME0 = res.name1
    NAME1 = res.name2
    NAME2 = res.name3
    NAME3 = res.name4

    """ Initialising a Chrome instance """
    driver = webdriver.Chrome()

    """ Enter the URL of the website"""
    driver.get("https://www.registration-software.net/cgi-bin/scheduling/rfparks/schedule.cgi")
    driver.implicitly_wait(5)

    """sign in using member code"""
    username = driver.find_element(By.NAME, "general_password")
    username.send_keys(CODE)

    sign_in_button = driver.find_element(By.XPATH, "//input[@type='submit']")
    sign_in_button.click()

    """select correct day from drop-down menu --- uses variable DAY """
    select_day = Select(driver.find_element(By.NAME, "selected_day"))
    select_day.select_by_value(DAY)
    driver.implicitly_wait(5)

    """calculating coordinate of item in table """
    tbody_xpath = "/html/body/center[2]/table/tbody/tr[2]/td[2]/center/table/tbody"
    row_xpath = tbody_xpath + "/tr[" + TIME_INDEX + "]/"
    row_col_xpath = row_xpath + "td[" + COURT_INDEX + "]/p/a"

    """click court-time combination"""
    time_court_toggle = driver.find_element(By.XPATH, row_col_xpath)
    time_court_toggle.click()
    driver.implicitly_wait(5)

    """filling in text slots"""
    name0 = driver.find_element(By.ID, "myInput0")
    name0.send_keys(NAME0)
    name1 = driver.find_element(By.ID, "myInput1")
    name1.send_keys(NAME1)
    name2 = driver.find_element(By.ID, "myInput2")
    name2.send_keys(NAME2)
    name3 = driver.find_element(By.ID, "myInput3")
    name3.send_keys(NAME3)

    password = driver.find_element(By.NAME, "password")
    password.send_keys(CODE)

    submit_res = driver.find_element(By.NAME, "submit_paypal")
    submit_res.click()
    driver.implicitly_wait(10)

    print("complete")
    driver.close()

