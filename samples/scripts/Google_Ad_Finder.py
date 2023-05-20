import re
from PIL import Image
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver import ChromeOptions, ActionChains
from webdriver_manager.core.utils import File
import cv2
options = Options()
options.add_experimental_option("detach", True)
options.add_argument("--disable-notifications")
options.add_argument("--disable-popup-blocking")
url = "https://www.google.com/search?q=Kredyt&client=firefox-b-d&ei=bshoZJS-OsLRqwGslozQBA&ved=0ahUKEwiUrfzi_YP_AhXC6CoKHSwLA0oQ4dUDCGs&uact=5&oq=Kredyt&gs_lcp=Cgxnd3Mtd2l6LXNlcnAQAzIKCAAQigUQsQMQQzILCAAQgAQQsQMQgwEyCggAEIoFELEDEEMyCAgAEIAEELEDMggIABCABBCxAzIICAAQgAQQsQMyCwgAEIoFELEDEIMBMggIABCABBCxAzIICAAQgAQQsQMyCAgAEIAEELEDOgcIABCKBRBDOg0IABCKBRCxAxCDARBDOgUIABCABDoLCC4QgAQQxwEQ0QM6CwguEIAEELEDEIMBOg0ILhCABBCxAxCDARAKOgcIABCABBAKOgUILhCABDoNCAAQgAQQsQMQgwEQCjobCC4QgAQQsQMQgwEQChCXBRDcBBDeBBDgBBgBSgQIQRgASgUIQBIBMVAAWKgTYPYUaAJwAXgAgAGJAYgB1ASSAQM2LjGYAQCgAQGwAQDAAQHaAQYIARABGBQ&sclient=gws-wiz-serp"


stalaWalczakaWidht=1.243333
stalaWalczakaHeight=1.54098
def SetUp():
    options = Options()
    options.add_experimental_option("detach", True)
    options.add_argument("--start-maximized")
    # blocking notficiation on chrome driver
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-popup-blocking")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),
                              options=options)
    driver.get(url)
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
        (By.XPATH, '//*[@id="L2AGLb"]'))).click()
    driver.save_screenshot("dupa.png")
    elements = driver.find_elements(By.XPATH, "//*[contains(text(), 'Sponsorowane')]")
    a = ActionChains(driver)
    for i, element in enumerate(elements):
        a.move_to_element(element).double_click().perform()
        parent = element.find_element(By.XPATH, ("./.."))
        img = Image.open("dupa.png")
        x = element.location["x"]
        y = element.location["y"]
        x=x+49 ##DRUGA STALA WALCZAKA
        y=y+49
        x1=x+(parent.size['width']*stalaWalczakaWidht)
        y1=y+(parent.size['height'] * stalaWalczakaHeight)
        img = img.crop((x, y, x1,y1 ))                                   ##Left Top right bottom
        img.save("Reklama_Nr_" + str(i) + ".png")
        img.close()
        href = re.findall(r"http\S*[ \n]", parent.text)
        print(href)


SetUp()
