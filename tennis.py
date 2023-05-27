
from selenium.webdriver.support.select import Select
from selenium import webdriver
from selenium.webdriver.common.by import By


def book_tennis_automated(res):
    USERID = res.user # TODO
    PASSWORD = res.pw


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

    """select correct day from drop-down menu --- uses variable DAY """
    # TODO

    """calculating coordinate of item in table """
    # TODO
    tbody_xpath = "/html/body/center[2]/table/tbody/tr[2]/td[2]/center/table/tbody"
    row_xpath = tbody_xpath + "/tr[" + TIME_INDEX + "]/"
    row_col_xpath = row_xpath + "td[" + COURT_INDEX + "]/p/a"

    """click court-time combination"""
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
    driver.implicitly_wait(5)

    """check if the reservation passed """
    try :
        driver.find_element(By.XPATH, "//*[contains(text(),'Success')]")
    except:
        return "fail"

    driver.quit()
    return "complete"

