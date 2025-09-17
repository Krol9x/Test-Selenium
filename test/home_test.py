import pytest
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
chromedriver_path = os.path.join(os.path.dirname(__file__), "chromedriver", "chromedriver.exe")


@pytest.fixture
def selenium_driver():
    service = Service(chromedriver_path)
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(service=service, options=options)
    yield driver
    driver.quit()



@pytest.mark.usefixtures("selenium_driver")
def test_links_section_and_open(selenium_driver):
    driver = selenium_driver
    driver.get("http://127.0.0.1:5000/")


    links_section = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//section[h2[text()='Links']]"))
    )
    driver.execute_script("arguments[0].scrollIntoView(true);", links_section)


    link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//section[h2[text()='Links']]//a"))
    )
    href = link.get_attribute("href")
    assert href, "Link nie ma atrybutu href!"


    driver.execute_script("window.open(arguments[0]);", href)
    driver.switch_to.window(driver.window_handles[-1])


    time.sleep(2)
    assert href.split("//")[-1].split("/")[0] in driver.current_url, f"Nie otworzył się poprawny link: {driver.current_url}"


    driver.close()
    driver.switch_to.window(driver.window_handles[0])
    
def test_course_certificate_link(selenium_driver):
    driver = selenium_driver
    driver.get("http://127.0.0.1:5000/")


    courses_section = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//section[h2[text()='Courses']]"))
    )
    driver.execute_script("arguments[0].scrollIntoView(true);", courses_section)


    cert_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//section[h2[text()='Courses']]//a[text()='Certyfikat']"))
    )
    href = cert_link.get_attribute("href")
    assert href, "Certyfikat link nie ma atrybutu href!"


    driver.execute_script("window.open(arguments[0]);", href)
    driver.switch_to.window(driver.window_handles[-1])


    time.sleep(2)
    assert href in driver.current_url, f"Nie otworzył się poprawny certyfikat: {driver.current_url}"


    driver.close()
    driver.switch_to.window(driver.window_handles[0])
    
@pytest.mark.usefixtures("selenium_driver")
def test_portfolio_download(selenium_driver, tmp_path):
    driver = selenium_driver

    download_dir = str(tmp_path)
    driver.command_executor._commands["send_command"] = (
        "POST",
        "/session/$sessionId/chromium/send_command",
    )
    driver.execute(
        "send_command",
        {
            "cmd": "Page.setDownloadBehavior",
            "params": {"behavior": "allow", "downloadPath": download_dir},
        },
    )

    driver.get("http://127.0.0.1:5000/")

    portfolio_section = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//section[h2[text()='Portfolio']]"))
    )
    driver.execute_script("arguments[0].scrollIntoView(true);", portfolio_section)


    file_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//section[h2[text()='Portfolio']]//a"))
    )
    href = file_link.get_attribute("href")
    assert href, "Portfolio file link nie ma href!"


    file_link.click()

    time.sleep(3)

    downloaded_files = os.listdir(download_dir)
    assert downloaded_files, "Żaden plik nie został pobrany z portfolio!"
    print("📂 Pobrane pliki:", downloaded_files)


    assert any(f.endswith(".zip") for f in downloaded_files), "Brak pobranego ZIP-a!"
    
@pytest.mark.usefixtures("selenium_driver")
def test_responsiveness(selenium_driver):
    driver = selenium_driver
    driver.get("http://127.0.0.1:5000/")

    sizes = [
        (1920, 1080),
        (1024, 768),   
        (375, 667),   
    ]

    for width, height in sizes:
        driver.set_window_size(width, height)
        time.sleep(1)  
        print(f"Test responsywności dla: {width}x{height}")

        menu_visible = driver.find_elements(By.CSS_SELECTOR, ".main-sections")
        assert menu_visible, f"Menu niewidoczne przy rozmiarze {width}x{height}"
