import time
from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

# Put in your reg here
REGISTRATION = "12L1591"
# Month for appointment: January, February, March etc.
TARGET_MONTH = "March"
# Time in seconds between sending request to NCT page
TIME_BETWEEN_RUNS: int = 5
# Get chromedriver from here depending on your Chrome version:
# https://googlechromelabs.github.io/chrome-for-testing/#stable
# You need to unzip it, right click on chromedriver and hit "open" for your Mac to trust it
DRIVER_PATH = "/Users/leonidioffe/Applications/ChromeApps/chromedriver-mac-arm64/chromedriver"

# Only need to accept cookies first time we load the page
need_to_accept_cookies = True

options = Options()
options.add_argument('--headless')
service = Service(executable_path=DRIVER_PATH)

# Create a new instance of the Chromedriver
driver = webdriver.Chrome(service=service, options=options)

# Boolean refresh_driver is True when we are looking for the first element
# on the page and False for all the others, cause every refresh wipes all elements found so far
def find_element_by_selector(element_id, selector, refresh_driver):
    max_retries = 10
    retries = 0
    element = None
    if refresh_driver:
        driver.refresh()
    while retries < max_retries:
        try:
            if selector.upper() == "ID":
                element = driver.find_element(By.ID, element_id)
            elif selector.upper() == "NAME":
                element = driver.find_element(By.NAME, element_id)
            elif selector.upper() == "CLASS_NAME":
                element = driver.find_element(By.CLASS_NAME, element_id)
            elif selector.upper() == "TAG_NAME":
                element = driver.find_element(By.TAG_NAME, element_id)
            elif selector.upper() == "XPATH":
                element = driver.find_element(By.XPATH, element_id)
            elif selector.upper() == "CSS_SELECTOR":
                element = driver.find_element(By.CSS_SELECTOR, element_id)
        except NoSuchElementException as e:
            # handle exception here, or log it for later analysis
            retries += 1
            time.sleep(1)
        else:
            # code execution successful, break out of the loop
            break
    return element


def get_first_appointment_date():
    # Navigate to the NCT website
    driver.get("https://www.ncts.ie/")

    # Page to accept cookies
    # Wait for the cookies page to come up to accept it
    global need_to_accept_cookies
    if need_to_accept_cookies:
        accept_button = find_element_by_selector("bs-gdpr-cookies-modal-accept-btn", "ID", False)
        accept_button.click()
        need_to_accept_cookies = False

    # Page 1 - landing page
    # Locate the input field using the aria-label attribute and insert a value
    registration_input = find_element_by_selector("input[aria-label='Enter Registration']", "CSS_SELECTOR", True)
    registration_input.send_keys(REGISTRATION)

    # Locate the "btnSearchVehicle" button using its id and click it
    search_button = find_element_by_selector("btnSearchVehicle", "ID", False)
    search_button.click()

    # Page 2 Voluntary Test Warning
    label = find_element_by_selector("//label[@for='agreeChk']", "XPATH", True)
    label_text = label.text
    if label_text == "To continue you must accept the Voluntary Test conditions.":
        checkbox = find_element_by_selector("agreeChk", "ID", True)
        checkbox.click()
        checkbox = find_element_by_selector("confirmVehicleYes", "ID", False)
        checkbox.click()

    # Page 3 page to agree with conditions and confirm vehicle
    checkbox = find_element_by_selector("agreeChk", "ID", True)
    checkbox.click()
    checkbox = find_element_by_selector("chkPrivacyRead", "ID", False)
    checkbox.click()
    button = find_element_by_selector("confirmVehicleYes", "ID", False)
    button.click()

    # Page 4 list of appointments
    slot = find_element_by_selector("input[name='SelectedBookingDay'][id='0']", "CSS_SELECTOR", True)
    return slot.get_attribute("value")

count = 1
while True:
    first_slot = get_first_appointment_date()
    print(f"{count} - first_slot: {first_slot}")
    count += 1
    if TARGET_MONTH.lower() in first_slot.lower():
        print("Found an appointment in target month '{}'.".format(TARGET_MONTH))
        # If found, run again and show the browser window
        driver = webdriver.Chrome(service=service)
        need_to_accept_cookies = True
        get_first_appointment_date()
        # Need to sleep long enough to book an appointment online - 600 seconds
        time.sleep(600)
        break
    else:
        print("No appointments found in " + TARGET_MONTH)
        time.sleep(TIME_BETWEEN_RUNS)

# Close the browser window
driver.quit()
