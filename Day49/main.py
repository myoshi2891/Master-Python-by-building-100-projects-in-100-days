import os
from time import sleep

from dotenv import load_dotenv
from selenium import webdriver
from selenium.common.exceptions import (
    NoSuchElementException,
    TimeoutException,
)
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

load_dotenv()  # Load environment variables from.env file

ACCOUNT_EMAIL = os.getenv("ACCOUNT_EMAIL", "")
ACCOUNT_PASSWORD = os.getenv("ACCOUNT_PASSWORD", "")
GYM_URL = os.getenv("GYM_URL", "")

service = Service(ChromeDriverManager().install(), log_path="chromedriver.log")


chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

user_data_dir = os.path.join(os.getcwd(), "chrome_profile")
chrome_options.add_argument(f"--user-data-dir={user_data_dir}")
driver = webdriver.Chrome(service=service, options=chrome_options)

print(GYM_URL)
driver.get(GYM_URL)

wait = WebDriverWait(driver, 2)


def retry(func, retries=7, description=None):
    for i in range(retries):
        print(f"Retrying ({i + 1}/{retries})")
        try:
            return func()
        except TimeoutException:
            if i == retries - 1:
                raise
            sleep(1)


def login():
    wait.until(lambda driver: driver.find_element(By.ID, value="login-button"))
    login = driver.find_element(By.ID, value="login-button")
    login.click()

    email_input = wait.until(
        lambda driver: driver.find_element(By.ID, value="email-input")
    )
    email_input.clear()
    email_input.send_keys(ACCOUNT_EMAIL)

    password_input = driver.find_element(By.ID, value="password-input")
    password_input.clear()
    password_input.send_keys(ACCOUNT_PASSWORD)

    submit_button = driver.find_element(By.ID, value="submit-button")
    submit_button.click()

    wait.until(EC.presence_of_element_located((By.ID, "schedule-page")))


def book_class(booking_button):
    booking_button.click()
    wait.until(lambda d: booking_button.text == "Booked")

retry(login, description="login")

class_cards = driver.find_elements(By.CSS_SELECTOR, "div[id^='class-card-']")

booked_count = 0
waitlist_count = 0
already_booked_count = 0
processed_classes = []

for card in class_cards:
    day_group = card.find_element(
        By.XPATH, "./ancestor::div[contains(@id, 'day-group-')]"
    )
    day_title = day_group.find_element(By.TAG_NAME, "h2").text

    if "Tue" in day_title or "Thu" in day_title:
        time_text = card.find_element(By.CSS_SELECTOR, "p[id^='class-time-']").text
        if "6:00 PM" in time_text:
            class_name = card.find_element(By.CSS_SELECTOR, "h3").text
            button = card.find_element(By.CSS_SELECTOR, "button[id^='book-button-']")

            class_info = f"{class_name} on {day_title}"

            if button.text == "Booked":
                print(f"Already Booked: {class_name} on {day_title}")
                already_booked_count += 1
                processed_classes.append(f"[Booked] {class_info}")
            elif button.text == "Waitlisted":
                print(f"Already on Waitlisted: {class_name} on {day_title}")
                already_booked_count += 1
                processed_classes.append(f"[Waitlisted] {class_info}")
            elif button.text == "Book Class":
                # button.click()
                retry(lambda: book_class(button), description="Booking")
                booked_count += 1
                print(f"You Booked: {class_name} on {day_title}")
                processed_classes.append(f"[New Booking] {class_info}")
                sleep(0.5)
            elif button.text == "Join Waitlist":
                # button.click()
                retry(lambda: book_class(button), description="Waitlisting")
                waitlist_count += 1
                print(f"You Joined Waitlist: {class_name} on {day_title}")
                processed_classes.append(f"[New Waitlist] {class_info}")
                sleep(1)  # Wait for the class to be booked


# Print summary
# print("\n--- BOOKING SUMMARY ---")
# print(f"Classes booked: {booked_count}")
# print(f"Waitlists joined: {waitlist_count}")
# print(f"Already booked/waitlisted: {already_booked_count}")
# print(f"Total Tuesday 6pm classes processed: {booked_count + waitlist_count + already_booked_count}")

# # Print detailed class list
# print("\n--- DETAILED CLASS LIST ---")
# for class_detail in processed_classes:
#     print(f"  • {class_detail}")

# tuesday_6pm = driver.find_element(By.ID, value="class-name-spin-2025-10-07-1800")
# book_class_button = driver.find_element(By.ID, value="book-button-spin-2025-10-07-1800")

# try:
#     book_class_button.click()
#     print("🤗: ✓ Booked: Spin Class on Tue, class booked successfully!")
# except ElementClickInterceptedException:
#     print("Unable to book class, please check your schedule.")

total_booked = already_booked_count + booked_count + waitlist_count
print(f"\n--- Total Tuesday/Thursday 6pm classes: {total_booked} ---")
print("\n--- VERIFYING ON MY BOOKINGS PAGE ---")


def get_my_bookings():
    my_bookings_link = driver.find_element(By.ID, "my-bookings-link")
    my_bookings_link.click()

    wait.until(EC.presence_of_element_located((By.ID, "my-bookings-page")))

    cards = driver.find_elements(By.CSS_SELECTOR, "div[id*='card-']")
    if not cards:
        raise TimeoutException("No bookings found on My Bookings page.")
    return cards


verified_count = 0

all_cards = retry(get_my_bookings, description="get_my_bookings")

if all_cards:
    for card in all_cards:
        try:
            when_paragraph = card.find_element(By.XPATH, ".//p[strong[text()='When:']]")
            when_text = when_paragraph.text

            if ("Tue" in when_text or "Thu" in when_text) and "6:00 PM" in when_text:
                class_name = card.find_element(By.TAG_NAME, "h3").text
                print(f"Verified: {class_name}")
                verified_count += 1
        except NoSuchElementException:
            print("Unable to verify class in My Bookings page.")

print("\n--- VERIFICATION RESULT ---")
print(f"Expected: {total_booked} bookings")
print(f"Found: {verified_count} bookings")

if total_booked == verified_count:
    print("✅ SUCCESS: All bookings verified!")
else:
    print(f"❌ MISMATCH: Missing {total_booked - verified_count} bookings")
