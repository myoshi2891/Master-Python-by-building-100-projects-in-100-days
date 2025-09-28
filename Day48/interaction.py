from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC

service = Service(ChromeDriverManager().install())

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(service=service, options=chrome_options)

# driver.get("https://en.wikipedia.org/wiki/Main_Page")

wait = WebDriverWait(driver, 15)
# num = driver.find_element(By.XPATH, '//*[@id="articlecount"]/ul/li[1]/a')
# article_count = driver.find_element(By.CSS_SELECTOR, value="#articlecount a")
# print(f"The number of articles on the main page is {article_count.text}")

# all_portals = driver.find_element(By.LINK_TEXT, value="Content portals")
# all_portals.click()

# search = driver.find_element(By.NAME, value="search")
# search.send_keys("Python", Keys.ENTER)


driver.get("https://secure-retreat-92358.herokuapp.com/")

first_name = driver.find_element(By.NAME, value="fName")
last_name = driver.find_element(By.NAME, value="lName")
email = driver.find_element(By.NAME, value="email")

first_name.send_keys("John")
last_name.send_keys("Doe")
email.send_keys("johndoe@example.com")

submit_button = driver.find_element(By.CSS_SELECTOR, value="form button")
submit_button.click()
driver.quit()
