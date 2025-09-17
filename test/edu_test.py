# -*- coding: utf-8 -*-
"""
Created on Tue Sep 16 23:49:14 2025

@author: huber
"""

import time
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os


chromedriver_path = os.path.join(os.path.dirname(__file__), "chromedriver", "chromedriver.exe")

@pytest.fixture
def selenium_driver():
    service = Service(chromedriver_path)
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(service=service, options=options)
    yield driver
    driver.quit()

def login_admin(driver):
    driver.get("http://127.0.0.1:5000/login")
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.NAME, "email"))
    )
    driver.find_element(By.NAME, "email").send_keys("hubert.krol0000@gmail.com")
    driver.find_element(By.NAME, "password").send_keys("admin123")
    driver.find_element(By.NAME, "submit").click()
    WebDriverWait(driver, 10).until(
        EC.url_contains("/admin")
    )

def test_add_and_delete_education(selenium_driver):
    driver = selenium_driver
    login_admin(driver)


    driver.get("http://127.0.0.1:5000/admin/education")
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.NAME, "school"))
    )

    school = "Test University"
    degree = "Bachelor of Testing"
    start_date = "01-09-2025" 
    end_date = "30-06-2029" 
    description = "Description for education test."
    

    driver.find_element(By.NAME, "school").send_keys(school)
    driver.find_element(By.NAME, "degree").send_keys(degree)
    driver.find_element(By.NAME, "start_date").send_keys(start_date)
    driver.find_element(By.NAME, "end_date").send_keys(end_date)
    driver.find_element(By.NAME, "description").send_keys(description)
    

    driver.find_element(By.CSS_SELECTOR, "form.form input[type='submit']").click()


    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located(
            (By.XPATH, f"//ul[@class='table']/li/div/strong[text()='{school}']")
        )
    )


    delete_form = driver.find_element(
        By.XPATH, f"//ul[@class='table']/li/div/strong[text()='{school}']/../../form"
    )
    delete_form.submit()


    WebDriverWait(driver, 10).until(
        EC.invisibility_of_element_located(
            (By.XPATH, f"//ul[@class='table']/li/div/strong[text()='{school}']")
        )
    )


    education_table = driver.find_elements(
        By.XPATH, f"//ul[@class='table']/li/div/strong[text()='{school}']"
    )
    assert len(education_table) == 0
