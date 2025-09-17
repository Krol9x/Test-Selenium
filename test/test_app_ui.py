import os
import time
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException

@pytest.fixture
def driver():
    chrome_options = Options()

    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")


    chromedriver_path = os.path.join(os.path.dirname(__file__), "chromedriver", "chromedriver.exe")
    service = ChromeService(executable_path=chromedriver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    yield driver
    driver.quit()

def test_login_success(driver):
    driver.get("http://127.0.0.1:5000/login")
    time.sleep(1)
    driver.find_element(By.NAME, "email").send_keys("hubert.krol0000@gmail.com")
    driver.find_element(By.NAME, "password").send_keys("admin123")
    driver.find_element(By.NAME, "submit").click()
    time.sleep(1)
    assert "admin" in driver.current_url

def test_login_failure(driver):
    driver.get("http://127.0.0.1:5000/login")
    time.sleep(1)
    driver.find_element(By.NAME, "email").send_keys("wrong@example.com")
    driver.find_element(By.NAME, "password").send_keys("wrongpass")
    driver.find_element(By.NAME, "submit").click()
    time.sleep(1)
    try:
        flash_message = driver.find_element(By.CLASS_NAME, "flash")
        assert "wrong" in flash_message.text.lower()
    except NoSuchElementException:
        pytest.fail("Brak komunikatu o błędzie przy niepoprawnym logowaniu")

def test_admin_requires_login(driver):

    driver.get("http://127.0.0.1:5000/admin")
    time.sleep(1)
    assert "login" in driver.current_url, "Niezalogowany użytkownik nie został przekierowany na login"

def test_logout(driver):

    driver.get("http://127.0.0.1:5000/login")
    time.sleep(1)
    driver.find_element(By.NAME, "email").send_keys("hubert.krol0000@gmail.com")
    driver.find_element(By.NAME, "password").send_keys("admin123")
    driver.find_element(By.NAME, "submit").click()
    time.sleep(1)


    assert "admin" in driver.current_url


    driver.get("http://127.0.0.1:5000/logout")
    time.sleep(1)


    assert driver.current_url.endswith("/") or "login" in driver.current_url