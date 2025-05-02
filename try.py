from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Setup
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(options=options)

try:
    # 1. Open the site
    driver.get("https://www.amazon.in")

    # 2. Search for something
    search_box = driver.find_element(By.ID, "twotabsearchtextbox")
    search_box.send_keys("laptop")
    search_box.send_keys(Keys.RETURN)

    # 3. Wait for results and apply a filter (e.g., HP brand)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//span[text()='HP']")))
    hp_filter = driver.find_element(By.XPATH, "//span[text()='HP']")
    hp_filter.click()

    # 4. Wait for filtered results
    time.sleep(3)  # wait for page to load after filter

    # 5. Extract product titles and prices
    products = driver.find_elements(By.XPATH, "//div[@data-component-type='s-search-result']")

    result_list = []
    for product in products[:10]:  # limit to first 10 results
        try:
            title = product.find_element(By.TAG_NAME, "h2").text
            price = product.find_element(By.CLASS_NAME, "a-price-whole").text
            result_list.append((title, price))
        except:
            continue  # skip if price or title not found

    # 6. Display the results
    print("Top 10 HP Laptops on Amazon:\n")
    for i, (title, price) in enumerate(result_list, 1):
        print(f"{i}. {title} - ₹{price}")

finally:
    driver.quit()
