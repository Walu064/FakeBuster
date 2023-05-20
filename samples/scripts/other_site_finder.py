import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Uruchom przeglądarkę i otwórz stronę
options = webdriver.ChromeOptions()
options.add_argument("--incognito")
options.add_argument("--disable-extensions")
options.add_argument("--enable-javascript")
options.add_argument("--enable-images")
options.add_argument("--disable-web-security")  # Wyłącz funkcje ochrony przeglądarki
options.add_argument("--no-sandbox")
options.add_argument("--ignore-certificate-errors")

driver = webdriver.Chrome(options=options)
driver.get('https://www.onet.pl/')

try:
    time.sleep(20)
    # Czekaj do 10 sekund na pojawienie się elementu na stronie
    divs = WebDriverWait(driver, 30).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div"))
    )
    print(divs)
    for div in divs:
        if 'reklama' in div.text.lower():
            print(f"Znaleziono div z id: {div.get_attribute('id')}")

    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'adslot-top'))
    )

    element.screenshot('element_screenshot.png')

finally:
    # Zamknij przeglądarkę
    driver.quit()