from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from time import sleep
import pytest


@pytest.fixture
def driver():
    # драйвер Firefox
    driver = webdriver.Firefox()
    driver.maximize_window()

    # фикстура
    driver.get("https://itcareerhub.de/ru")

    yield driver

    # Закрытие браузера
    driver.quit()


def test_payment_methods_screenshot(driver):
    sleep(3)
    payment_link = driver.find_element(By.LINK_TEXT, "Способы оплаты")
    payment_link.click()
    sleep(3)
    driver.save_screenshot("./payment_methods.png")
# проверочка
    print(f"Текущий URL: {driver.current_url}")
    assert "payment" in driver.current_url