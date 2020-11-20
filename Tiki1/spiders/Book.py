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

    def start_requests(self):
        urlRelative = 'https://tiki.vn/bestsellers/sach-truyen-tieng-viet/c316'
        count = 1
        for page in range(1, 5):
            count = count + 1
            url = urlRelative + "?" + "p=" + str(page)

            print('page - ', count)
            yield scrapy.Request(url, self.parse)

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
        frame_list = response.xpath('//div[@class="product-listing"]/div[@class="bestseller-cat"]/div[@class="bestseller-cat-list"]/div[@class="bestseller-cat-item"]')
        # table = response.xpath('//div[@class="product-listing"]/div[@class="bestseller-cat"]/div[@class="bestseller-cat-list"]/div[@class="bestseller-cat-item"]')


        for j in frame_list:
            # name = j.xpath('.//div[@class="product-col-2"]/div[@class="infomation"]/p/a')

            frame["NAME"] = j.xpath('.//div[@class="product-col-2"]/div[@class="infomation"]/p/a/text()').get()
            frame["AUTHOR"] = j.xpath('.//div[@class="product-col-2"]/div[@class="infomation"]/p[@class="author"]/text()').get()
            frame["REVIEWS"] = j.xpath('.//div[@class="product-col-2"]/div[@class="infomation"]/p[@class="review"]/text()').get()
            frame["PRICE_SALE"] = j.xpath('.//div[@class="product-col-2"]/div[@class="infomation"]/p[@class="price-sale"]/text()').get()
            frame["PRICE_SALE"] = frame["PRICE_SALE"].split(' ')[0]
            frame["PRICE_REGULAR"] = j.xpath('.//div[@class="product-col-2"]/div[@class="infomation"]/p[@class="price-sale"]/span[@class="price-regular"]/text()').get()
            frame["DISCOUNT"] = j.xpath('.//div[@class="product-col-2"]/div[@class="infomation"]/p[@class="price-sale"]/span[@class="sale-tag sale-tag-square"]/text()').get()

            TIKINOW = j.xpath('//div[@class="product-col-2"]/div[@class="infomation"]/p/a/i/@class').get()
            TIKINOW = re.findall("tikinow",TIKINOW)
            frame["TIKINOW"] = TIKINOW

            #frame["RATES"] = j.find_elements_by_xpath('.//div[@class="product-col-2"]/div[@class="infomation"]/p[@class="rating"]/span[@class="rating-content"]/span')[0].get_attribute('style')
            RATES = j.xpath('.//div[@class="product-col-2"]/div[@class="infomation"]/p[@class="rating"]/span[@class="rating-content"]/span/@style').get()
            RATES = RATES.split(':')[-1].replace(";", '')
            frame["RATES"] = RATES
            #


            # price sale /html/body/div[10]/div/div/div[2]/div/div[3]/div[1]/div[3]/div/p[5]
            # price regular /html/body/div[10]/div/div/div[2]/div/div[3]/div[1]/div[3]/div/p[5]/span[1]
            # discount /html/body/div[10]/div/div/div[2]/div/div[3]/div[1]/div[3]/div/p[5]/span[2]
            # general /html/body/div[10]/div/div/div[2]/div/div[3]

            yield {
                "NAME" : frame["NAME"],
                "AUTHOR" : frame["AUTHOR"],
                "REVIEWS": frame["REVIEWS"],
                "PRICE_SALE":frame["PRICE_SALE"],
                "PRICE_REGULAR":frame["PRICE_REGULAR"],
                "DISCOUNT":frame["DISCOUNT"],
                "TIKINOW":frame["TIKINOW"],
                "RATES":frame["RATES"]

            }




        pass
