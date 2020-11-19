import time

import scrapy
import json
from lxml import etree
from Tiki1.items import Tiki1Item
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
import re

BROWSER_EXE = '/Applications/Firefox.app/Contents/MacOS/firefox'
GEKODRIVER = '/usr/local/Cellar/geckodriver/0.27.0/bin/geckodriver'
FirefoxBinary = FirefoxBinary(BROWSER_EXE)


class BookSpider(scrapy.Spider):
    name = 'Book'
    allowed_domains = ['tiki.vn/bestsellers/sach-truyen-tieng-viet/c316?p=1']
    start_urls = ['https://tiki.vn/bestsellers/sach-truyen-tieng-viet/c316?p=1']

    custom_settings = {
        "DOWNLOADER_MIDDLEWARES": {
            "Tiki1.middlewares.RotateProxyMiddleware": 300,
            "Tiki1.middlewares.RotateAgentMiddleware": 301,
           # "Tiki1.middlewares.Tiki1Middleware": 302
        },
        "ITEM_PIPELINES": {
            "Tiki1.pipelines.Tiki1Pipeline": 300
        }

    }




    def parse(self, response):
        options = webdriver.FirefoxOptions()

        start_urls = ['https://tiki.vn/bestsellers/sach-truyen-tieng-viet/c316?p=1']
        driver = webdriver.Firefox(firefox_options=options)
        frame = Tiki1Item()

        # traverse each page
        driver.get('https://tiki.vn/bestsellers/sach-truyen-tieng-viet/c316?p=1')
        # Implicit wait
        driver.implicitly_wait(10)
        # Explicit wait
        wait = WebDriverWait(driver, 5)
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "bestseller-cat-item")))

            #frame_xpath = '//div[@class="bestseller-cat"]/div[@class="bestseller-cat-list"]/div[@class="bestseller-cat-item"]'
        frame_list = driver.find_elements_by_xpath('//div[@class="product-listing"]/div[@class="bestseller-cat"]/div[@class="bestseller-cat-list"]/div[@class="bestseller-cat-item"]')
        print(len(frame_list))


        for j in frame_list:
            # name = j.find_elements_by_xpath('.//div[@class="product-col-2"]/div[@class="infomation"]/p/a')[0]
            # frame["NAME"] = name.text
            frame["NAME"] = j.find_elements_by_xpath('.//div[@class="product-col-2"]/div[@class="infomation"]/p/a')[0].text
            frame["AUTHOR"] = j.find_elements_by_xpath('.//div[@class="product-col-2"]/div[@class="infomation"]/p[@class="author"]')[0].text
            frame["REVIEWS"] = j.find_elements_by_xpath('.//div[@class="product-col-2"]/div[@class="infomation"]/p[@class="review"]')[0].text
            frame["PRICE_SALE"] = j.find_elements_by_xpath('.//div[@class="product-col-2"]/div[@class="infomation"]/p[@class="price-sale"]')[0].text.split(' ')[0]
            frame["PRICE_REGULAR"] = j.find_elements_by_xpath('.//div[@class="product-col-2"]/div[@class="infomation"]/p[@class="price-sale"]/span[@class="price-regular"]')[0].text
            frame["DISCOUNT"] = j.find_elements_by_xpath('.//div[@class="product-col-2"]/div[@class="infomation"]/p[@class="price-sale"]/span[@class="sale-tag sale-tag-square"]')[0].text

            TIKINOW = j.find_elements_by_xpath('//div[@class="product-col-2"]/div[@class="infomation"]/p/a/i')[0].get_attribute('class')
            TIKINOW = re.findall("tikinow",TIKINOW)
            frame["TIKINOW"] = TIKINOW

            #frame["RATES"] = j.find_elements_by_xpath('.//div[@class="product-col-2"]/div[@class="infomation"]/p[@class="rating"]/span[@class="rating-content"]/span')[0].get_attribute('style')
            RATES = j.find_elements_by_xpath('.//div[@class="product-col-2"]/div[@class="infomation"]/p[@class="rating"]/span[@class="rating-content"]/span')[0].get_attribute('style')
            RATES = RATES.split(' ')[-1].replace(";", '')
            frame["RATES"] = RATES



            # price sale /html/body/div[10]/div/div/div[2]/div/div[3]/div[1]/div[3]/div/p[5]
            # price regular /html/body/div[10]/div/div/div[2]/div/div[3]/div[1]/div[3]/div/p[5]/span[1]
            # discount /html/body/div[10]/div/div/div[2]/div/div[3]/div[1]/div[3]/div/p[5]/span[2]
            # general /html/body/div[10]/div/div/div[2]/div/div[3]

            yield frame



        pass
