from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.chrome.options import Options

from Reservation import Reservation

def book_paddle_automated(res: Reservation):
    """Automates the paddle court booking process using Selenium in headless Chrome."""
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=options)

    try:
        # Go to the booking page
        driver.get("https://www.registration-software.net/cgi-bin/scheduling/rfparks/schedule.cgi")

        # Enter the member password
        driver.find_element(By.NAME, "general_password").send_keys(res.code)

        # Submit the reservation
        driver.find_element(By.XPATH, '//input[@type="submit" and @value="Logon"]').click()

        # Wait until the select element is present
        select_day_element = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.NAME, "selected_day"))
        )

        # Use Select to interact with the dropdown
        select_day = Select(select_day_element)
        all_options = select_day.options
        days = [
            option.get_attribute("value")
            for option in all_options
            if option.get_attribute("value").isdigit()
        ]

        # Use +1 offset because the first option is "---Show Another Day---"
        value = days[res.days_in_advance]

        select_day.select_by_value(value)

        # Wait briefly for the page to reload after selecting the day
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "submit_paypal"))
        )

        # Locate the desired court/time slot
        tbody_xpath = "/html/body/center[2]/table/tbody/tr[2]/td[2]/center/table/tbody"
        row_xpath = f"{tbody_xpath}/tr[{res.time}]/td[{res.court}]/p/a"
        driver.find_element(By.XPATH, row_xpath).click()

        # Fill in player names
        for i, name in enumerate(res.names):
            driver.find_element(By.ID, f"myInput{i}").send_keys(name)

        # Enter the member password
        driver.find_element(By.NAME, "password").send_keys(res.code)

        # Submit the reservation
        driver.find_element(By.NAME, "submit_paypal").click()

        # Confirm success
        try:
            driver.find_element(By.XPATH, "//*[contains(text(),'Success')]")
            result = "complete"
        except NoSuchElementException as e:
            raise e

    except (NoSuchElementException, TimeoutException) as e:
        raise e

    finally:
        driver.quit()

    return result
