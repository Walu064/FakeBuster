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

def AcceptCookies(driver) -> None:
    AcceptText = ["Zaakceptuj wszystko","Przejdź do serwisu", "Zaakceptuj wszystko", "AKCEPTUJĘ I PRZECHODZĘ DO SERWISU"]
    for i in AcceptText:
        try:
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
                (By.XPATH, f"//*[text()='{i}']/ancestor-or-self::button"))).click()
        except TimeoutException:
            print(f"I can't find : {i} -> on this website")
        else:
            break


def YouTubeSS(driver, seconds_to_wait: int):
    
    current_seconds = datetime.datetime.now().second

    wait = WebDriverWait(driver, seconds_to_wait)
    try:

        div_element = wait.until(EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'Film zostanie wyświetlony po reklamach')]")))

    except TimeoutException:
        # sorry for that xD
        driver.save_screenshot("photo" + str(current_seconds) + ".png")

    x = 50
    y = 100
    width = 1200
    height = 600
    
    # Open the screenshot image using Pillow
    image = Image.open("photo" + str(current_seconds) + ".png")
    
    # Crop the image using the defined coordinates
    cropped_image = image.crop((x, y, x+width, y+height))
    
    # Save the cropped image
    cropped_image.save("ad_photo_croped_" + str(current_seconds) + ".png")

    os.remove("photo" + str(current_seconds) + ".png")

def Detect() -> None:

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

    url = "https://www.youtube.com/watch?v=d4t7XUL_vHA"

    driver.get(url)
  
    AcceptCookies(driver)
   
    YouTubeSS(driver, 5)
    YouTubeSS(driver, 2)
    YouTubeSS(driver, 2)
    YouTubeSS(driver, 2)
    YouTubeSS(driver, 2)
    

    

    

    # YouTube(driver)

    # ScreenShot(driver, ["ad", "ad_", "ad-", "-ad-"])

    # driver.quit()

def main():
   
    Detect()

if __name__ == "__main__":
    main()
