import re
from PIL import Image
from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
options = Options()
options.add_experimental_option("detach", True)
options.add_argument("--disable-notifications")
options.add_argument("--disable-popup-blocking")
url = "https://www.bing.com/search?q=kredyty&form=QBLH&sp=-1&ghc=1&lq=0&pq=kre&sc=10-3&qs=n&sk=&cvid=5A47F23174004E24A5C9D02313534A32&ghsh=0&ghacc=0&ghpl="
#url="https://www.google.com/search?client=firefox-b-d&q=kredyt"

stalaWalczakaWidht = 1.243333
stalaWalczakaHeight = 1.54098

def SetUp():
    # f = open("demofile2.txt", "a")
    # f.write("Now the file has more content!")
    # f.close()
    options = Options()
    options.add_experimental_option("detach", True)
    options.add_argument("--start-maximized")
    # blocking notficiation on chrome driver
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-popup-blocking")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),
                              options=options)
    driver.get(url)
    if(url.__contains__("google")):
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="L2AGLb"]'))).click()
        driver.save_screenshot("dupa.png")
        elements = driver.find_elements(By.XPATH, "//*[contains(text(), 'Sponsorowane')]")
        for i, element in enumerate(elements):
            parent = element.find_element(By.XPATH, ("./.."))
            print(parent.location['y'])
            x = element.location["x"]
            y = element.location["y"]
            x = x + 49
            y = y + 49
            if(i!=0):
                driver.execute_script("window.scrollTo(0, '%d');" %(parent.location['y']-100))
                value = driver.execute_script("return window.pageYOffset;")
                driver.save_screenshot("dupa.png")
                y=125
                print(value)
                print(parent.location['y'])
            img = Image.open("dupa.png")

            x1 = x+(parent.size['width']*stalaWalczakaWidht)
            y1 = y+(parent.size['height'] * stalaWalczakaHeight)
            img = img.crop((x, y, x1, y1))                                   ##Left Top right bottom
            img.save("Reklama_Nr_" + str(i) + ".png")
            img.close()
            href = re.findall(r"http\S*[ \n]", parent.text)
            for g in href:
                f = open("hfrefGoogle.txt", "a")
                f.write(g+"\n")
                f.close()

    else:
        AcceptCookies(driver)
        elements = driver.find_elements(By.XPATH, "//*[contains(text(), 'Reklama')]")
        driver.save_screenshot("dupa.png")
        for i, element in enumerate(elements):
            parent = element.find_element(By.XPATH, ("./../../.."))
            x = element.location["x"]+15
            y = element.location["y"]-40
            driver.save_screenshot("dupa.png")
            if i != 0:
                driver.execute_script("window.scrollTo(0, '%d');" % (parent.location['y'] - 100))
                value = driver.execute_script("return window.pageYOffset;")
                driver.save_screenshot("dupa.png")
                y = 115
                print(value)
                print(parent.location['y'])
            img = Image.open("dupa.png")
            x1 = x + (parent.size['width'] * stalaWalczakaWidht)
            y1 = y + (parent.size['height'] * stalaWalczakaHeight)
            img = img.crop((x, y, x1, y1))  ##Left Top right bottom
            img.save("Reklama_Nr_" + str(i) + ".png")
            img.close()
            href = re.findall(r"http\S*[ \n]", parent.text)




def AcceptCookies(driver) -> None:
    AcceptText = ["Akceptuj","AcceptCookies","Zaakceptuj wszystko","Przejdź do serwisu",
                  "Zaakceptuj wszystko", "AKCEPTUJĘ I PRZECHODZĘ DO SERWISU",]
    for i in AcceptText:
        try:
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
                (By.XPATH, f"//*[text()='{i}']/ancestor-or-self::button"))).click()
        except TimeoutException:
            print(f"I can't find : {i} -> on this website")
        else:
            break

SetUp()
