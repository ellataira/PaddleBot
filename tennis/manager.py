import yaml
import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from datetime import date, datetime
import traceback
import logging
import sys


class Reservation:
    """
    Represents a court reservation with all necessary information to book
    """

    def __init__(self, name, username, password, timeslot, court, duration, days_in_advance, config):
        self.name = name
        self.username = username
        self.password = password
        self.raw_timeslot = timeslot
        self.court = court
        self.raw_duration = duration
        self.days_in_advance = days_in_advance

        # Calculate values based on configuration
        sport_type = config['settings']['sport_type']
        self.timeslot = str(config['time_slots'][sport_type].get(timeslot, "1"))
        self.duration = str(config['durations'].get(duration, "2"))

    def __str__(self):
        return (f"Reservation '{self.name}':\n"
                f"  Username: {self.username}\n"
                f"  Time: {self.raw_timeslot} (value: {self.timeslot})\n"
                f"  Court: {self.court}\n"
                f"  Duration: {self.raw_duration} hours (value: {self.duration})\n"
                f"  Days in advance: {self.days_in_advance}")


class ReservationManager:
    """Manages loading configuration and booking reservations"""

    def __init__(self, config_path=None):
        """
        Initialize the reservation manager

        Args:
            config_path: Path to the YAML configuration file (auto-detect if None)
        """
        self.log_file = "reservations.log"

        # Set up initial logging
        self._setup_logging()

        # Find config file - check different possible locations
        if not config_path:
            possible_paths = [
                'tennis_config.yaml',           # Current directory
                '../tennis_config.yaml',        # Parent directory
                '../../tennis_config.yaml',     # Two levels up
            ]

            for path in possible_paths:
                if os.path.exists(path):
                    config_path = path
                    break

            if not config_path:
                self.logger.error("No configuration file found")
                raise FileNotFoundError("No configuration file found")

        # Load configuration
        self.config = self._load_config(config_path)
        self.website_url = self.config['settings']['website']

        # Load reservations
        self.reservations = self._load_reservations()

    def _setup_logging(self):
        """Set up logging configuration"""
        # Reset log file
        if os.path.exists(self.log_file):
            # Clear the log file but keep it
            with open(self.log_file, 'w') as f:
                f.write(f"=== Tennis Reservation Log Started: {datetime.now()} ===\n\n")

        # Configure logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(self.log_file),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        self.logger.info(f"Logger initialized")

    def _load_config(self, config_path):
        """Load configuration from YAML file"""
        try:
            with open(config_path, 'r') as file:
                self.logger.info(f"Loaded configuration from {config_path}")
                return yaml.safe_load(file)
        except Exception as e:
            self.logger.error(f"Error loading configuration: {str(e)}")
            raise

    def _load_reservations(self):
        """Create Reservation objects from config"""
        reservations = []
        for res_config in self.config['reservations']:
            if res_config.get('enabled', True):
                reservation = Reservation(
                    name=res_config['name'],
                    username=res_config['username'],
                    password=res_config['password'],
                    timeslot=res_config['timeslot'],
                    court=res_config['court'],
                    duration=res_config['duration'],
                    days_in_advance=res_config['days_in_advance'],
                    config=self.config
                )
                reservations.append(reservation)
                self.logger.info(f"Loaded reservation: {reservation.name}")
        return reservations

    def _find_available_cell(self, driver, day_index, court_num, timeslot_value):
        """
        Find the correct cell for booking using direct XPath strategy.
        Only returns a cell if it's clearly available (open and pointer classes).

        Args:
            driver: Selenium webdriver
            day_index: Index of the day (1 = today, 2 = tomorrow, etc.)
            court_num: Court number (1-12)
            timeslot_value: Time slot value from configuration

        Returns:
            WebElement: The cell element to click for booking
            None: If cell is not available for any reason
        """
        self.logger.info(f"Finding cell for day {day_index}, court {court_num}, timeslot {timeslot_value}")

        try:
            # Try direct XPath approach
            xpath = f"/html/body/form/p[2]/table/tbody/tr[{day_index}]/td[{court_num + 1}]"
            wait = WebDriverWait(driver, 5)
            cell = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))

            # Get cell attributes
            class_attr = cell.get_attribute("class")
            title_attr = cell.get_attribute("title") or cell.get_attribute("oldtitle") or ""

            self.logger.info(f"Found cell with class: {class_attr}")
            self.logger.info(f"Cell title/oldtitle: {title_attr}")

            # Only return the cell if it's available (open and pointer classes)
            if "open" in class_attr and "pointer" in class_attr:
                self.logger.info("Cell is available for booking")
                return cell
            else:
                # If the cell is not available for any reason, return None
                if "G" in class_attr:
                    self.logger.info("Cell is already booked")
                elif "restricted" in class_attr:
                    self.logger.info("Cell is restricted")
                else:
                    self.logger.info(f"Cell is not available: {class_attr}")
                return None

        except Exception as e:
            self.logger.error(f"Error finding cell: {str(e)}")
            return None

    def _check_for_booked_cells_by_user(self, driver, username):
        """
        Check the page for any cells booked by the specified user

        Args:
            driver: Selenium webdriver
            username: Username to check for

        Returns:
            bool: True if any cells are found booked by the user, False otherwise
        """
        self.logger.info(f"Checking for cells booked by: {username}")

        try:
            # Find all cells with G class (booked cells)
            all_cells = driver.find_elements(By.CSS_SELECTOR, "td")
            self.logger.info(f"Found {len(all_cells)} total cells")

            # Check each cell for the username in title/oldtitle
            for cell in all_cells:
                class_attr = cell.get_attribute("class") or ""
                if "G" in class_attr:
                    title = cell.get_attribute("title") or cell.get_attribute("oldtitle") or ""
                    self.logger.info(f"Found booked cell with title: {title}")

                    # Check if this cell is booked by our user
                    if username.lower() in title.lower():
                        self.logger.info(f"Found cell booked by {username}")
                        return True

            self.logger.info(f"No cells found booked by {username}")
            return False

        except Exception as e:
            self.logger.error(f"Error checking for booked cells: {str(e)}")
            return False

    def book_reservation(self, reservation):
        """
        Book a single reservation and check if it was successful

        Args:
            reservation: Reservation object to book

        Returns:
            bool: True if booking was successful, False otherwise
        """
        self.logger.info(f"Attempting to book reservation: {reservation.name}")
        self.logger.info(f"User: {reservation.username}, Court: {reservation.court}, Time: {reservation.raw_timeslot}")

        driver = None
        try:
            # Set up Chrome driver with options
            chrome_options = Options()
            if 'CI' in os.environ:
                chrome_options.add_argument('--headless')
                chrome_options.add_argument('--no-sandbox')
                chrome_options.add_argument('--disable-dev-shm-usage')

            driver = webdriver.Chrome(options=chrome_options)
            driver.set_page_load_timeout(30)  # Set timeout to avoid hanging
            driver.implicitly_wait(5)

            # Open reservation website
            driver.get(self.website_url)

            # Sign in
            sign_in = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "/html/body/div[1]/form/p[1]/table[1]/tbody/tr/td[2]/nav/ul/li[2]/a"))
            )
            sign_in.click()

            username_field = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.NAME, "user_id"))
            )
            username_field.send_keys(reservation.username)

            password_field = driver.find_element(By.NAME, "password")
            password_field.send_keys(reservation.password)

            login_button = driver.find_element(By.XPATH, '//*[@id="CheckUser"]')
            login_button.click()

            # Navigate to time slot view
            timeslot_path = f'/html/body/div[1]/form/p[2]/table/tbody/tr[{reservation.timeslot}]/td[1]'
            timeslot_view = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, timeslot_path))
            )
            timeslot_view.click()

            # Wait for page to load
            WebDriverWait(driver, 10).until(
                lambda d: len(d.find_elements(By.CSS_SELECTOR, "td")) > 0
            )

            # First check if the user already has a booking
            if self._check_for_booked_cells_by_user(driver, reservation.username):
                self.logger.info(f"User {reservation.username} already has a booking. Failing out.")
                if driver:
                    driver.quit()
                return False

            # Find the cell for booking
            days_ahead = int(reservation.days_in_advance) + 1
            court_column = int(reservation.court)

            # Find the cell - will return None if already booked or restricted
            cell = self._find_available_cell(driver, days_ahead, court_column, reservation.timeslot)

            # If no available cell found, fail immediately
            if cell is None:
                self.logger.info(
                    f"Court {reservation.court} at time {reservation.raw_timeslot} is not available. Marking as failure.")
                if driver:
                    driver.quit()
                return False

            # Attempt to book the cell
            try:
                # Try both regular click and JavaScript click
                try:
                    cell.click()
                except:
                    driver.execute_script("arguments[0].click();", cell)

                # Fill in reservation details
                select_duration = Select(WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.NAME, "Duration"))
                ))
                select_duration.select_by_value(reservation.duration)

                submit_res = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.ID, "SaveReservation"))
                )
                submit_res.click()

                # Look for confirmation message first
                confirmation_found = False
                try:
                    confirmation = WebDriverWait(driver, 5).until(
                        EC.presence_of_element_located((By.XPATH, "//td[contains(text(), 'Reservation Scheduled')]"))
                    )
                    self.logger.info(f"Confirmation message: {confirmation.text}")
                    confirmation_found = True
                except:
                    self.logger.warning("No confirmation message found. Will check by looking for booked cells.")

                # If confirmation found, return success
                if confirmation_found:
                    self.logger.info("Booking confirmed via confirmation message")
                    if driver:
                        driver.quit()
                    return True

                # If no confirmation, click on the time slot view again to check for booked cells
                try:
                    WebDriverWait(driver, 10).until(
                        lambda d: len(d.find_elements(By.CSS_SELECTOR, "td")) > 0
                    )

                    if self._check_for_booked_cells_by_user(driver, reservation.username):
                        self.logger.info(f"Verification successful: Found cell booked by {reservation.username}")
                        if driver:
                            driver.quit()
                        return True
                    else:
                        self.logger.warning(f"Verification failed: No cells found booked by {reservation.username}")
                except Exception as e:
                    self.logger.error(f"Error during final verification: {str(e)}")

                # If we got here, no confirmation was found
                self.logger.warning("Booking likely failed - no confirmation and no booked cells found")
                if driver:
                    driver.quit()
                return False

            except Exception as e:
                self.logger.error(f"Error during booking process: {str(e)}")
                if driver:
                    driver.quit()
                return False

        except Exception as e:
            self.logger.error(f"Error in booking process: {str(e)}")
            if driver:
                try:
                    driver.quit()
                except:
                    pass
            return False

    def book_all_reservations(self):
        """Book all enabled reservations"""
        self.logger.info(f"Starting reservation process on {date.today()}")
        results = {}

        for reservation in self.reservations:
            success = self.book_reservation(reservation)
            results[reservation.name] = "Success" if success else "Failed"

        self.logger.info("Reservation results:")
        for name, result in results.items():
            self.logger.info(f"  {name}: {result}")

        return results


def make_res(reservation, manager):
    """Legacy compatibility function"""
    print(f"Attempting to reserve: \n" +
          f"time: {reservation.raw_timeslot}\n" +
          f"for court {reservation.court}\n" +
          f"under {reservation.username}\n" +
          f"pw: {reservation.password}\n" +
          f"days in advance: {reservation.days_in_advance}\n")

    return manager.book_reservation(reservation)