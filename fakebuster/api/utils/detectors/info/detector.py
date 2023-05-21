import os
import sys
import time
from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

cwd = os.path.dirname(os.path.realpath(__file__))
api_dir = os.path.dirname(os.path.dirname(os.path.dirname(cwd)))
sys.path.append(api_dir)

from models import AdvertModel, DefaultRequestModel
from conf.config import SCREENSHOTS_DIR


options = webdriver.ChromeOptions()
options.add_argument("--incognito")
options.add_argument("--disable-extensions")
options.add_argument("--enable-javascript")
options.add_argument("--enable-images")
options.add_argument("--enable-popup-blocking")
options.add_argument("--start-maximized")
options.add_argument("--disable-web-security")
options.add_argument("--no-sandbox")
options.add_argument("--ignore-certificate-errors")
cwd = os.getcwd()


def collect(url: str) -> str:
    driver = webdriver.Chrome(options=options)
    
    dr = connect(driver, url)
    AcceptCookies(driver)
    if dr is not None:
        try:
            print("Znaleziono strone")
            time.sleep(3)
            total_height = driver.execute_script("return document.body.scrollHeight")

            for i in range(1, total_height,10):
                driver.execute_script("window.scrollTo(0, {});".format(i))
                time.sleep(0.02)  # Czekaj na 0.01 sekundy

            elements = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.XPATH,
                                                     "//div[contains(., 'REKLAMA') or contains(., 'Sponsorowane') or contains(., 'Reklama')]"))
            )
            try:
                elements_img = WebDriverWait(driver, 10).until(
                    EC.presence_of_all_elements_located((By.XPATH, "//div[@id='optad-360']"))
                )
                parent_elements = [element.find_element(By.XPATH, "./..") for element in elements_img]

                for i in parent_elements:
                    print(i.get_attribute('id'))

                elements.extend(parent_elements)
            except Exception as e:
                print(e)

            dir_path = str(time.time_ns())
            if not os.path.exists(f'{SCREENSHOTS_DIR}\\{dir_path}'):
                os.makedirs(f'{SCREENSHOTS_DIR}\\{dir_path}')

            list_to_return = []
            for i, element in enumerate(elements):
                print(f"Znaleziono div z id: {element.get_attribute('id')}", end=' --> ')
                if element.get_attribute('id'):
                    try:
                        print('screenshot ', end='--> ')
                        element.screenshot(f'{SCREENSHOTS_DIR}\\{dir_path}\element_{i}_screenshot.png')
                    
                    except Exception as e:
                        print(e)
                    
                    else:
                        print('save')
                        obj = AdvertModel(
                            url="https://www.google.com/",
                            name="",
                            destination_url=[],
                            words=[],
                            screenshot_ads=f'{SCREENSHOTS_DIR}\\{dir_path}\element_{i}_screenshot.png'
                        )
                        list_to_return.append(obj)
                        
            driver.quit()
            return list_to_return
            
        except Exception as e:
            print(e)
            return []
    else:
        print("Nie uydało się załadować zawartości strony.")
        return []


def connect(driver, url: str):
    driver.get(url)
    try:
        # Czekaj do 13 sekund, aż tag <body> stanie się widoczny
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

        return driver

    except Exception as e:
        print("Nie udało się załadować zawartości strony.")
        print(e)
        return None


def AcceptCookies(driver) -> None:
    AcceptText = ["Akceptuj", "Przejdź do serwisu", "Zgadzam się", "AcceptCookies", "Zaakceptuj wszystko",
                  "Przejdź do serwisu",
                  "Zaakceptuj wszystko",
                  "AKCEPTUJĘ I PRZECHODZĘ DO SERWISU",
                  "PRZECHODZĘ DO SERWISU",
                  "Akceptuję", "AKCEPTUJĘ"]
    time.sleep(3)
    for i in AcceptText:
        try:
            WebDriverWait(driver, 0.1).until(EC.element_to_be_clickable(
                (By.XPATH, f"//*[text()='{i}']/ancestor-or-self::button"))).click()
        except TimeoutException:
            print(f"I can't find : {i} -> on this website")
        else:
            break


def info_detect(data : DefaultRequestModel) -> list[AdvertModel]:
    return collect(data.url)
