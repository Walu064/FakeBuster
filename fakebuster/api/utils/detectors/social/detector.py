import os
import sys
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver import ChromeOptions, ActionChains
from PIL import Image
from selenium.common.exceptions import TimeoutException
import time
import datetime
import os
import re

from fakebuster.api.utils.text_processing.ocr import get_text_from_img
cwd = os.path.dirname(os.path.realpath(__file__))
api_dir = os.path.dirname(os.path.dirname(os.path.dirname(cwd)))
sys.path.append(api_dir)

from fakebuster.api.models import AdvertModel, DefaultRequestModel
from fakebuster.api.conf.config import SCREENSHOTS_DIR


# AdvertModel object attrs to fullfuill:
#   - url : advertisement url
#   - words (partially : raw div text)
#   - screenshot_ads : copy img source to SCREENSHOT_DIR and store path
# 
# Other attrs:
#   - name : str = ""
#   - words : list[str] = []
#   - destination_url : list[str] = []

def AcceptCookies(driver) -> AdvertModel:
    AcceptText = ["Zaakceptuj wszystko","Przejdź do serwisu", "Zaakceptuj wszystko", "AKCEPTUJĘ I PRZECHODZĘ DO SERWISU"]
    for i in AcceptText:
        try:
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
                (By.XPATH, f"//*[text()='{i}']/ancestor-or-self::button"))).click()
        except TimeoutException:
            print(f"I can't find : {i} -> on this website")
        else:
            break

def YouTubeSS(driver, seconds_to_wait: int) -> AdvertModel | None:
    
    current_seconds = datetime.datetime.now().second

    wait = WebDriverWait(driver, seconds_to_wait)
    try:

        div_element = wait.until(EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'Film zostanie wyświetlony po reklamach')]")))

    except TimeoutException:
        # sorry for that xD
        driver.save_screenshot(SCREENSHOTS_DIR + "\\" + "photo" + str(current_seconds) + ".png")

    x = 50
    y = 100
    width = 1200
    height = 600
    
    html_croped_image = image.crop((140,600,650,640))

    html_croped_image.save(SCREENSHOTS_DIR + "\\" + "photo_croped" + str(current_seconds) + ".png")
    
    # Open the screenshot image using Pillow
    image = Image.open(SCREENSHOTS_DIR + "\\" + "photo" + str(current_seconds) + ".png")
    
    # Crop the image using the defined coordinates
    cropped_image = image.crop((x, y, x+width, y+height))
    
    # Save the cropped image
    dir_of_image = cropped_image.save(SCREENSHOTS_DIR + "\\" + "ad_photo_croped_" + str(current_seconds) + ".png")

    

    os.remove(SCREENSHOTS_DIR + "\\" + "photo" + str(current_seconds) + ".png")

    ocr_from_ss = get_text_from_img(SCREENSHOTS_DIR + "\\" + "photo_croped" + str(current_seconds) + ".png")
    print(ocr_from_ss)
    url_from_ocr = re.findall(r"\b(?:\w+\.)+\w+(?:/\S+)?\b", ocr_from_ss)
    
    try:
        obj = AdvertModel(
            url = url_from_ocr[0],
            name = '',
            screenshot_ads= dir_of_image,
            words= [],
            destination_url=[]
        )

    except IndexError:
        return None

    else:
        return obj

    

def facebook_detect(data : DefaultRequestModel) -> list[AdvertModel]:
    # TODO: Facebook search engine ads detection
    raise NotImplementedError("Facebook service ads detection method is not implemented yet.")


def linkedin_detect(data : DefaultRequestModel) -> list[AdvertModel]:
    # TODO: LinkedIn search engine ads detection
    raise NotImplementedError("LinkedIn service ads detection method is not implemented yet.")


def youtube_detect(data : DefaultRequestModel) -> list[AdvertModel]:
    options = Options()
    options.add_experimental_option("detach", True)

    # blocking notficiation on chrome driver
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-popup-blocking")
    options.add_argument("--enable-automation")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-browser-side-navigation")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-extensions")
    options.add_argument("--start-maximized")
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--accept-all-cookies")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),
                              options=options)
    
    url = data.url

    driver.get(url)
    list_to_return = []
    AcceptCookies(driver)

    for _ in range(5):
        ad = YouTubeSS(driver, 5)
        if ad:
            list_to_return.append(ad)

    return list_to_return
