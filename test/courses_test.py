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

def test_add_and_delete_course(selenium_driver):
    driver = selenium_driver
    login_admin(driver)


    driver.get("http://127.0.0.1:5000/admin/courses")
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.NAME, "title"))
    )


    title = "Test Course"
    provider = "Example Provider"
    date_completed = "01-01-2025"
    credential_url = "https://example.com/certificate"
    notes = "Test notes for course."


    driver.find_element(By.NAME, "title").send_keys(title)
    driver.find_element(By.NAME, "provider").send_keys(provider)
    driver.find_element(By.NAME, "date_completed").send_keys(date_completed)
    driver.find_element(By.NAME, "credential_url").send_keys(credential_url)
    driver.find_element(By.NAME, "notes").send_keys(notes)
    driver.find_element(By.CSS_SELECTOR, "form.form input[type='submit']").click()


    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located(
            (By.XPATH, f"//ul[@class='table']/li/div/strong[text()='{title}']")
        )
    )


    delete_form = driver.find_element(
        By.XPATH, f"//ul[@class='table']/li/div/strong[text()='{title}']/../../form"
    )
    delete_form.submit()


    WebDriverWait(driver, 10).until(
        EC.invisibility_of_element_located(
            (By.XPATH, f"//ul[@class='table']/li/div/strong[text()='{title}']")
        )
    )


    course_table = driver.find_elements(
        By.XPATH, f"//ul[@class='table']/li/div/strong[text()='{title}']"
    )
    assert len(course_table) == 0
