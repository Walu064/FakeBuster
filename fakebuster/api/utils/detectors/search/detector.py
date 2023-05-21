import os
import sys
import os
import re
from bs4 import BeautifulSoup
import requests
from PIL import Image
from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from utils.text_processing import ocr
cwd = os.path.dirname(os.path.realpath(__file__))
api_dir = os.path.dirname(os.path.dirname(os.path.dirname(cwd)))
sys.path.append(api_dir)

from models import AdvertModel, SearchRequestModel
from conf.config import SCREENSHOTS_DIR


options = Options()
options.add_experimental_option("detach", True)
options.add_argument("--disable-notifications")
options.add_argument("--disable-popup-blocking")
options.add_argument("--start-maximized")
stalaWalczakaWidht = 1.445                                                   ## This is smth like Planck's constant
                                                                                ## needed to resize div from html source
stalaWalczakaHeight = 2.198



# AdvertModel object attrs to fullfuill:
#   - url : advertisement url
#   - words (partially : raw div text)
#   - screenshot_ads : copy img source to SCREENSHOT_DIR and store path
# 
# Other attrs:
#   - name : str = ""
#   - words : list[str] = []
#   - destination_url : list[str] = []

def AcceptCookies(driver) -> None:
    AcceptText = ["Akceptuj","Przejdź do serwisu","Zgadzam się","AcceptCookies","Zaakceptuj wszystko","Przejdź do serwisu",
                  "Zaakceptuj wszystko", "AKCEPTUJĘ I PRZECHODZĘ DO SERWISU",]
    for i in AcceptText:
        try:
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
                (By.XPATH, f"//*[text()='{i}']/ancestor-or-self::button"))).click()
        except TimeoutException:
            print(f"I can't find : {i} -> on this website")
        else:
            break

def bing_detect(data : SearchRequestModel) -> list[AdvertModel]:
    list_to_return = []
    url = data.url
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),
                              options=options)
    driver.get(url)
    driver.save_screenshot("imageToCrop.png")
    AcceptCookies(driver)
    elements = driver.find_elements(By.XPATH, "//*[contains(text(), 'Reklama')]")
    driver.save_screenshot("imageToCrop.png")
    for i, element in enumerate(elements):
        name = "Reklama_Nr_" + str(i) + ".png"
        parent = element.find_element(By.XPATH, ("./../../.."))
        left_border_to_crop = element.location["x"] + 15
        top_border_to_crop = element.location["y"] - 40
        driver.save_screenshot("imageToCrop.png")
        if i != 0:
            driver.execute_script("window.scrollTo(0, '%d');" % (parent.location['y'] - 100))
            driver.save_screenshot("imageToCrop.png")
            top_border_to_crop = 115
        img = Image.open("imageToCrop.png")
        right_border_to_crop = left_border_to_crop + (parent.size['width'] * stalaWalczakaWidht)
        bottom_border_to_crop = top_border_to_crop + (parent.size['height'] * stalaWalczakaHeight)
        img = img.crop((left_border_to_crop, top_border_to_crop, right_border_to_crop, bottom_border_to_crop))  ##Left Top right bottom
        img.save(SCREENSHOTS_DIR + "\\" + name)
        img.close()

        words = ocr.get_text_from_img(Image.open("imageToCrop.png"))
        words_d = str(words).to_list()
        parent = element.find_element(By.XPATH, ("./../../.."))
        childs = parent.find_elements(By.XPATH, (".//*"))
        list_to_return.append(AdvertModel(
            url='',
            name="",
            destination_url=[],
            words=words_d,
            screenshot_ads=SCREENSHOTS_DIR + "\\" + ''
        ))
    return list_to_return



def google_detect(data : SearchRequestModel) -> list[AdvertModel]:
    list_to_return = []
    url = data.url
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),
                              options=options)
    driver.get(url)
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
        (By.XPATH, '//*[@id="L2AGLb"]'))).click()
    driver.save_screenshot("imageToCrop.png")
    elements = driver.find_elements(By.XPATH, "//*[contains(text(), 'Sponsorowane')]")
    print(len(elements))
    
    for i, element in enumerate(elements):
        object_to_list = AdvertModel
        name = "Reklama_Nr_" + str(i) + ".png"
        parent = element.find_element(By.XPATH, ("./.."))
        left_border_to_crop = parent.location["x"]
        top_border_to_crop = parent.location["y"] + 49
        if (i != 0):
            driver.execute_script("window.scrollTo(0, '%d');" % (parent.location['y'] - 100))
            value = driver.execute_script("return window.pageYOffset;")
            top_border_to_crop = 125
        driver.save_screenshot("imageToCrop.png")
        img_to_crop = Image.open("imageToCrop.png")
        right_border_to_crop =  (parent.size['width'] * stalaWalczakaWidht)
        bottom_border_to_crop = (parent.size['height'] * stalaWalczakaHeight)
        if i>5: break
        img_to_crop = img_to_crop.crop((left_border_to_crop, top_border_to_crop, right_border_to_crop, bottom_border_to_crop))  ##Left Top right bottom
        img_to_crop.save(SCREENSHOTS_DIR + "\\" + name)
        img_to_crop.close()
        href = re.findall(r"http\S*[ \n]", parent.text)
        words = ocr.get_text_from_img(img_to_crop)        
        words_d = words.to_list()

        for i in href:
            i = i.replace("\n", "")
        
        list_to_return.append(AdvertModel(
            url = href,
            name = "",
            destination_url = [],
            words = words_d,
            screenshot_ads = SCREENSHOTS_DIR + "\\" + name
        ))

    return list_to_return
