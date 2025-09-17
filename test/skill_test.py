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

def test_add_and_delete_skill(selenium_driver):
    driver = selenium_driver
    login_admin(driver)


    driver.get("http://127.0.0.1:5000/admin/skills")
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.NAME, "name"))
    )

    skill_name = "Python hubert22"


    driver.find_element(By.NAME, "name").send_keys(skill_name)
    driver.find_element(By.CSS_SELECTOR, "input[type='submit']").click()


    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located(
            (By.XPATH, f"//ul[@class='table']/li/div[contains(text(), '{skill_name}')]")
        )
    )


    delete_button = driver.find_element(
        By.XPATH,
        f"//ul[@class='table']/li[div[contains(text(), '{skill_name}')]]//div[@class='col actions']/form/button"
    )
    delete_button.click()


    WebDriverWait(driver, 10).until(
        EC.invisibility_of_element_located(
            (By.XPATH, f"//ul[@class='table']/li/div[contains(text(), '{skill_name}')]")
        )
    )


    skills_list = driver.find_elements(
        By.XPATH, f"//ul[@class='table']/li/div[contains(text(), '{skill_name}')]"
    )
    assert len(skills_list) == 0
