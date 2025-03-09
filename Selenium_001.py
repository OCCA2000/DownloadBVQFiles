# -*- coding: utf-8 -*-
"""
Created on Tue Jun 27 17:00:30 2023

@author: jhono
"""

import json
from typing import IO

from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

BASE_URL = "https://fly.kinectair.com"
FILE_NAME = "urls.json"


def open_and_verify_url(data: dict, driver: WebDriver, wait: WebDriverWait):
    url_split = data["url"].split("/")
    url = (BASE_URL + "/{0}/{1}").format(url_split[4], url_split[5])
    driver.get(url)
    container_e: WebElement = wait.until(ec.visibility_of_element_located((By.XPATH, '//*[@id="tripContainer"]')))
    data['isAvailable'] = verify_error_container(container_e)


def verify_error_container(element: WebElement):
    try:
        element.find_element(By.XPATH, '//*[@id="tripContainer"]/jhi-trip/jhi-trip-error/div/div/p')
        return False
    except:
        return True


def save_on_file(json_data: list, file_name: str):
    f2: IO = open(file_name, mode="a")
    f2.write(json.dumps(json_data))
    f2.close()


def init():
    index = 1
    data_s: list = []
    try:
        driver: WebDriver = webdriver.Chrome()
        wait: WebDriverWait = WebDriverWait(driver, 9999999999)
        driver.maximize_window()

        f: IO = open("urls.json", mode="r")
        data: list = json.load(f)[220:400]
        print("Total Elements: {0}".format(len(data)))
        for url_data in data:
            print("Count Number: {0}".format(index))
            index += 1
            open_and_verify_url(url_data, driver, wait)
            data_s.append(url_data)
        f.close()
        save_on_file(data_s, FILE_NAME)
    except:
        print("Index Fail In: {0}".format(index))
        save_on_file(data_s, FILE_NAME)


if _name_ == '__main__':
    init()