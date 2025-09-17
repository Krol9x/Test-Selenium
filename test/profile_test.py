import os
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


sample_photo_path = os.path.join(os.getcwd(), "test_files", "profilowe_1.jpg")
sample_photo_path  = os.path.abspath(sample_photo_path )

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

def test_edit_profile(selenium_driver):
    driver = selenium_driver
    login_admin(driver)


    driver.get("http://127.0.0.1:5000/admin/profile")


    full_name = "Test User"
    headline = "Software Developer"
    about = "This is a test profile."
    email = "testuser@example.com"
    phone = "+48123456789"
    location = "Warsaw, Poland"


    driver.find_element(By.NAME, "full_name").clear()
    driver.find_element(By.NAME, "full_name").send_keys(full_name)
    driver.find_element(By.NAME, "headline").clear()
    driver.find_element(By.NAME, "headline").send_keys(headline)
    driver.find_element(By.NAME, "about").clear()
    driver.find_element(By.NAME, "about").send_keys(about)
    driver.find_element(By.NAME, "email").clear()
    driver.find_element(By.NAME, "email").send_keys(email)
    driver.find_element(By.NAME, "phone").clear()
    driver.find_element(By.NAME, "phone").send_keys(phone)
    driver.find_element(By.NAME, "location").clear()
    driver.find_element(By.NAME, "location").send_keys(location)


    photo_input = driver.find_element(By.NAME, "photo")
    driver.execute_script(
        "arguments[0].removeAttribute('hidden'); arguments[0].style.display='block';", photo_input
    )
    driver.execute_script("arguments[0].removeAttribute('disabled');", photo_input)
    photo_input.send_keys(sample_photo_path)


    driver.find_element(By.CSS_SELECTOR, "form.form input[type='submit']").click()


    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "full_name"))
    )


    assert driver.find_element(By.NAME, "full_name").get_attribute("value") == full_name
    assert driver.find_element(By.NAME, "headline").get_attribute("value") == headline
    assert driver.find_element(By.NAME, "about").text == about
    assert driver.find_element(By.NAME, "email").get_attribute("value") == email
    assert driver.find_element(By.NAME, "phone").get_attribute("value") == phone
    assert driver.find_element(By.NAME, "location").get_attribute("value") == location


    img_elements = driver.find_elements(By.CSS_SELECTOR, ".admin-pic img")
    assert len(img_elements) > 0
