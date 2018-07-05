from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import Select

import time
import json
import random
import io
import phosphorus_config


try:
    to_unicode = unicode
except NameError:
    to_unicode = str


def random_sleep():
    sleepLength = (random.randint(0, 3))
    print "Sleep for ", sleepLength, "seconds"
    time.sleep(sleepLength)


option = webdriver.ChromeOptions()
option.add_argument("--incognito")


browser = webdriver.Chrome(
    executable_path='/usr/local/bin/chromedriver', chrome_options=option)


browser.get(phosphorus_config.startUrl)

# Wait 20 seconds for page to load
try:
    timeout = 20
    WebDriverWait(browser, timeout).until(EC.visibility_of_element_located(
        (By.XPATH, "//img[@src='/public/logo.gif']")))
except TimeoutException:
    print("Timed out waiting for page to load")
    browser.quit()


# find_elements_by_xpath returns an array of selenium objects.
user_box = browser.find_element_by_xpath("//input[@name='user']")
user_box.send_keys(phosphorus_config.libraryCode)

pin_box = browser.find_element_by_xpath("//input[@name='pass']")
pin_box.send_keys(phosphorus_config.pin)

login_button = browser.find_element_by_xpath("//input[@type='submit']")
login_button.click()

try:
    timeout = 20
    WebDriverWait(browser, timeout).until(EC.visibility_of_element_located(
        (By.XPATH, "//*[@id='mircheader']/div[1]/div[2]/div[1]/a/img")))
except TimeoutException:
    print("Timed out waiting for page to load1")
    browser.refresh()
    try:
        timeout = 20
        WebDriverWait(browser, timeout).until(EC.visibility_of_element_located(
            (By.XPATH, "//*[@id='mircheader']/div[1]/div[2]/div[1]/a/img")))
    except TimeoutException:
        print("Timed out waiting for page to load2")
        browser.quit()

random_sleep()

dropdown = browser.find_element_by_xpath(
    "/html/body/div/div[2]/div[2]/form[1]/a/table[2]/tbody/tr[4]/td[2]/select")
select = Select(dropdown)

visText = "gninro"
endVisText = "gnitaR"

# select by visible text
select.select_by_visible_text(
    'M' + visText[::-1] + "st" + "ra"[::-1] + ' ' + endVisText[::-1])


keepLooping = True

try:
    timeout = 20
    WebDriverWait(browser, timeout).until(EC.visibility_of_element_located(
        (By.XPATH, "//*[@id='mircheader']/div[1]/div[2]/div[1]/a/img")))
except TimeoutException:
    print("Timed out waiting for page to load3")
    browser.refresh()
    try:
        timeout = 20
        WebDriverWait(browser, timeout).until(EC.visibility_of_element_located(
            (By.XPATH, "//*[@id='mircheader']/div[1]/div[2]/div[1]/a/img")))
    except TimeoutException:
        print("Timed out waiting for page to load4")
        keepLooping = False


browser.execute_script("SetSort('StarRating')")

try:
    timeout = 20
    WebDriverWait(browser, timeout).until(EC.visibility_of_element_located(
        (By.XPATH, "//*[@id='mircheader']/div[1]/div[2]/div[1]/a/img")))
except TimeoutException:
    print("Timed out waiting for page to load3")
    browser.refresh()
    try:
        timeout = 20
        WebDriverWait(browser, timeout).until(EC.visibility_of_element_located(
            (By.XPATH, "//*[@id='mircheader']/div[1]/div[2]/div[1]/a/img")))
    except TimeoutException:
        print("Timed out waiting for page to load4")
        keepLooping = False


random_sleep()


class PhosphorusData:
    def __init__(self, name="", ticker="", starRating=0, price=0.0, fairValueEstimate=0.0, uncertainty="", considerBuy=0.0, considerSell=0.0, economicMoat="", stewardshipRating=""):
        self.name = name
        self.ticker = ticker
        self.starRating = starRating
        self.price = price
        self.fairValueEstimate = fairValueEstimate
        self.uncertainty = uncertainty
        self.considerBuy = considerBuy
        self.considerSell = considerSell
        self.economicMoat = economicMoat
        self.stewardshipRating = stewardshipRating


jsonData = []

while keepLooping:
    table_id = browser.find_element_by_xpath(
        "/html/body/div/div[2]/div[2]/form[1]/a/table[4]")
    # get all of the rows in the table
    rows = table_id.find_elements(By.TAG_NAME, "tr")

    for row in rows:
        msd = PhosphorusData()
        # Get the columns (all the column 2)
        cellData = row.find_elements(By.TAG_NAME, "td")

        for index, cell in enumerate(cellData):
            if index == 2:
                # href = cell.find_element_by_tag_name("a");
                href = ""
                children = cell.find_elements_by_xpath(".//*")
                for index, child in enumerate(children):
                    href = child.get_attribute("href")

                msd.name = cell.text
                try:
                    ticker = href.split("?")[1].replace("ticker=", "")
                    # print ticker
                    msd.ticker = ticker
                except:
                    pass

            try:
                if index == 4:
                    imgData = cell.find_element(By.TAG_NAME, "img")
                    if imgData:
                        starSrc = imgData.get_property("src")

                        if "5stars" in starSrc:
                            msd.starRating = 5
                        elif "4stars" in starSrc:
                            msd.starRating = 4
                        elif "3stars" in starSrc:
                            msd.starRating = 3
                        elif "2stars" in starSrc:
                            msd.starRating = 2
                        elif "1stars" in starSrc:
                            msd.starRating = 1
                        else:
                            msd.starRating = 0

            except:
                # if msd.name and msd.name != "" and msd.name != "Stock Name" and msd.name != "S&P 500":
                #     keepLooping = False;
                # else:
                pass

            if msd.name and msd.name != "Stock Name" and msd.name != "S&P 500":
                if index == 6 and cell.text != "--":
                    msd.fairValueEstimate = float(cell.text)

                if index == 8 and cell.text != "--":
                    msd.price = float(cell.text)

                if index == 12 and cell.text != "--":
                    msd.uncertainty = cell.text

                if index == 14 and cell.text != "--":
                    msd.economicMoat = cell.text

        if msd.name and msd.name != "Stock Name" and msd.name != "S&P 500":
            jsonObject = {}
            jsonObject["name"] = msd.name
            jsonObject["ticker"] = msd.ticker
            jsonObject["starRating"] = msd.starRating
            jsonObject["price"] = msd.price
            jsonObject["fairValueEstimate"] = msd.fairValueEstimate
            jsonObject["uncertainty"] = msd.uncertainty
            jsonObject["considerBuy"] = msd.considerBuy
            jsonObject["considerSell"] = msd.considerSell
            jsonObject["economicMoat"] = msd.economicMoat
            jsonObject["stewardshipRating"] = msd.stewardshipRating

            print(jsonObject)

            jsonData.append(jsonObject)

    random_sleep()

    try:
        browser.find_element_by_link_text("Next 25").click()
    except:
        browser.refresh()
        time.sleep(15)
        try:
            browser.find_element_by_link_text("Next 25").click()
        except:
            print "Breaking loop, ended processing"
            keepLooping = False

    if keepLooping:
        try:
            timeout = 20
            WebDriverWait(browser, timeout).until(EC.visibility_of_element_located(
                (By.XPATH, "//*[@id='mircheader']/div[1]/div[2]/div[1]/a/img")))
        except TimeoutException:
            print("Timed out waiting for page to load9")
            browser.refresh()
            try:
                timeout = 20
                WebDriverWait(browser, timeout).until(EC.visibility_of_element_located(
                    (By.XPATH, "//*[@id='mircheader']/div[1]/div[2]/div[1]/a/img")))
            except TimeoutException:
                print("Timed out waiting for page to load10")
                keepLooping = False

timestr = time.strftime("%Y%m%d-%H%M%S")

with open('phosphorus_rating/' + timestr + '.json', 'w') as outfile:
    json.dump(jsonData, outfile, indent=4)


browser.quit()
