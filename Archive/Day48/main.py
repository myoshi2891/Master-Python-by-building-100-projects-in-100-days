from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

service = Service(ChromeDriverManager().install())

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(service=service, options=chrome_options)

driver.get("https://www.python.org/")

wait = WebDriverWait(driver, 15)
# price_dollars = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "span.a-price-whole")))
# price_cents = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "span.a-price-fraction")))
# print(f"The price of the product is ${price_dollars.text}.{price_cents.text}")

search_bar = driver.find_element(By.NAME, value="q")
# print(f"Entering 'Python' into the search bar...{search_bar.get_attribute("placeholder")}")

button = driver.find_element(By.ID, value='submit')
# print(button.size)

documentation_link = driver.find_element(By.CSS_SELECTOR,value=".documentation-widget a")
# print(documentation_link.text)

footer_link = driver.find_element(By.XPATH,'//*[@id="container"]/li[4]/ul/li[8]/a')
# print(footer_link.text)

event_times = driver.find_elements(By.CSS_SELECTOR, value='.event-widget time')
event_names = driver.find_elements(By.CSS_SELECTOR, value='.event-widget li a')
events = {}
for n in range(len(event_times)):
    events[n] = {
        'time': event_times[n].text,
        'name': event_names[n].text,
    }

print(events)
driver.quit()
