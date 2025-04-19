from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
import time

# Prompt the user for email and password
email = input("Enter your email or phone number: ")
password = input("Enter your password: ")

# Prompt the user for the account URL and number of reports
account_url = input("Enter the account URL you want to report: ")
report_count = int(input("Enter the number of reports you want to send: "))

# Set up Firefox options
options = Options()
options.add_argument("--headless")  # Run in headless mode
options.set_preference("general.useragent.override", "Mozilla/5.0 (Android 10; Mobile; rv:112.0) Gecko/112.0 Firefox/112.0")

# Set path to Firefox binary and geckodriver
firefox_binary = "/data/data/com.termux/files/usr/bin/firefox"
geckodriver_path = "/data/data/com.termux/files/usr/bin/geckodriver"

# Initialize the WebDriver
driver = webdriver.Firefox(options=options, executable_path=geckodriver_path, firefox_binary=firefox_binary)

# Navigate to Facebook login page
driver.get("https://www.facebook.com/")

# Log in
time.sleep(2)
driver.find_element(By.ID, "email").send_keys(email)
driver.find_element(By.ID, "pass").send_keys(password)
driver.find_element(By.NAME, "login").click()
time.sleep(4)

# Navigate to the account to report
driver.get(account_url)
time.sleep(2)

# Reporting loop
for i in range(report_count):
    # Click the three dots
    driver.find_element(By.XPATH, '//div[@aria-label="Actions for this post"]').click()
    time.sleep(1)

    # Click "Find support or report post"
    driver.find_element(By.XPATH, '//span[text()="Find support or report post"]').click()
    time.sleep(1)

    # Click "It's inappropriate"
    driver.find_element(By.XPATH, '//span[text()="It\'s inappropriate"]').click()
    time.sleep(1)

    # Click "Submit"
    driver.find_element(By.XPATH, '//span[text()="Submit"]').click()
    time.sleep(1)

    # Click "Done"
    driver.find_element(By.XPATH, '//span[text()="Done"]').click()
    time.sleep(2)

# Close the browser
driver.quit()
