# -*- coding: utf-8 -*-
"""
Created on Tue Sep 16 23:50:09 2025

@author: huber
"""

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture
def selenium_driver():
    driver = webdriver.Chrome()
    driver.implicitly_wait(5)
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
def test_add_and_delete_link(selenium_driver):
    driver = selenium_driver
    login_admin(driver)


    driver.get("http://127.0.0.1:5000/admin/links")


    title = "Test Link"
    url = "https://example.com"

    driver.find_element(By.NAME, "name").send_keys(title)
    driver.find_element(By.NAME, "url").send_keys(url)
    driver.find_element(By.NAME, "submit").click()


    link_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.XPATH, f"//ul[@class='table']/li[.//h3[contains(text(), '{title}')]]//a")
        )
    )


    assert link_element.get_attribute("href").rstrip("/") == url.rstrip("/")

    delete_button = driver.find_element(By.XPATH,
        f"//ul[@class='table']/li[.//h3[text()='{title}']]//button[contains(text(),'Delete')]"
    )
    delete_button.click()

    WebDriverWait(driver, 10).until(
        lambda d: len(d.find_elements(By.XPATH, f"//ul[@class='table']/li[.//h3[text()='{title}']]")) == 0
    )