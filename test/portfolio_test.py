import os
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


sample_file_path = os.path.join(os.getcwd(), "test_files", "test.zip")
sample_file_path = os.path.abspath(sample_file_path)


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


def test_add_and_delete_portfolio(selenium_driver):
    driver = selenium_driver
    login_admin(driver)

    driver.get("http://127.0.0.1:5000/admin/portfolio")

    title = "Test Project"
    description = "This is a test project."


    driver.find_element(By.NAME, "title").send_keys(title)
    driver.find_element(By.NAME, "description").send_keys(description)


    file_input = driver.find_element(By.NAME, "file")
    driver.execute_script("arguments[0].removeAttribute('hidden'); arguments[0].style.display='block';", file_input)
    driver.execute_script("arguments[0].removeAttribute('disabled');", file_input)
    file_input.send_keys(sample_file_path)


    driver.find_element(By.CSS_SELECTOR, "form.form input[type='submit']").click()


    new_item = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located(
            (By.XPATH, f"//ul[@class='table']/li/div/strong[text()='{title}']/ancestor::li")
        )
    )


    delete_button = new_item.find_element(By.XPATH, ".//button[@type='submit']")
    delete_button.click()


    WebDriverWait(driver, 20).until(
        EC.staleness_of(new_item)
    )
