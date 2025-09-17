# -*- coding: utf-8 -*-
import time
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoAlertPresentException


chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")


service = ChromeService(ChromeDriverManager().install())

@pytest.fixture
def selenium_driver():
    driver = webdriver.Chrome(service=service, options=chrome_options)
    yield driver
    driver.quit()

def test_send_contact_message(selenium_driver):
    driver = selenium_driver
    driver.get("http://127.0.0.1:5000/")

    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "div.contact-form form"))
    )

    driver.find_element(By.NAME, "name").send_keys("Test User")
    driver.find_element(By.NAME, "email").send_keys("test@example.com")
    driver.find_element(By.NAME, "content").send_keys("To jest testowa wiadomość.")
    driver.find_element(By.NAME, "submit").click()

    time.sleep(1)

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

def test_receive_and_delete_contact_message(selenium_driver):
    driver = selenium_driver


    login_admin(driver)

    driver.get("http://127.0.0.1:5000/admin/messages")
    time.sleep(3)


    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "ul.message-list li.message-item"))
    )

    messages = driver.find_elements(By.CSS_SELECTOR, "ul.message-list li.message-item")


    found_message = None
    for msg in messages:
        if "Test User" in msg.text and "test@example.com" in msg.text:
            found_message = msg
            break

    assert found_message is not None, "Nie znaleziono testowej wiadomości w panelu admina"


    delete_btn = found_message.find_element(By.CSS_SELECTOR, "button.danger")
    delete_btn.click()
    try:
        WebDriverWait(driver, 3).until(EC.alert_is_present())
        alert = driver.switch_to.alert
        alert.accept()
    except NoAlertPresentException:
        pass


    WebDriverWait(driver, 10).until(EC.staleness_of(found_message))


    driver.refresh()
    messages_after = driver.find_elements(By.CSS_SELECTOR, "ul.message-list li.message-item")
    assert all("Test User" not in m.text for m in messages_after), "Wiadomość nie została usunięta"
