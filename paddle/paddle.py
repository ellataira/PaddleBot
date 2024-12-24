from selenium.webdriver.support.select import Select
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.chrome.options import Options

from Reservation import Reservation


# from webdriver_manager.chrome import ChromeDriverManager


def book_paddle_automated(res: Reservation):
    """Initializing a Chrome instance in headless mode"""
    options = Options()
    options.add_argument("--headless")  # Enable headless mode
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=options)
    """Automates the paddle court booking process using Selenium."""

    # Initialize a Chrome instance (you can use ChromeDriverManager for automatic setup)
    # driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    try:
        # Enter the URL of the website
        driver.get(
            "https://www.registration-software.net/cgi-bin/scheduling/rfparks/schedule.cgi"
        )

        # Select the correct day from the drop-down menu
        select_day = Select(driver.find_element(By.NAME, "selected_day"))
        all_options = select_day.options
        days = [
            option.get_attribute("value")
            for option in all_options
            if option.get_attribute("value").isdigit()
        ]
        value = days[
            res.days_in_advance + 1
        ]  # add 1 b/c select dropdown first element = "Show another day"

        select_day.select_by_value(value)

        # Locate the time slot and court based on user input
        tbody_xpath = "/html/body/center[2]/table/tbody/tr[2]/td[2]/center/table/tbody"
        row_xpath = f"{tbody_xpath}/tr[{res.time}]/td[{res.court}]/p/a"
        driver.find_element(By.XPATH, row_xpath).click()

        # Fill in reservation details
        for i, name in enumerate(res.names):
            driver.find_element(By.ID, f"myInput{i}").send_keys(name)

        # Enter the member code again as a password
        password = driver.find_element(By.NAME, "password")
        password.send_keys(res.code)

        # Submit the reservation
        submit_res = driver.find_element(By.NAME, "submit_paypal")
        submit_res.click()

        # Check if the reservation was successful
        try:
            driver.find_element(By.XPATH, "//*[contains(text(),'Success')]")
            result = "complete"
        except NoSuchElementException as e:
            raise e

    except (NoSuchElementException, TimeoutException) as e:
        # Handle any exceptions that occur during execution
        raise e

    finally:
        # Always close the browser window
        driver.quit()

    return result
