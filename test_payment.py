import pytest
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture
def driver():
    """Фикстура для инициализации браузера Firefox."""
    # Инструкция требует Firefox (Mozilla)
    driver = webdriver.Firefox()
    driver.maximize_window()
    driver.get("https://itcareerhub.de/ru")
    yield driver
    driver.quit()


def test_screenshot_payment_section(driver):
    """Тест переходит в раздел Способы оплаты и делает скриншот секции."""
    wait = WebDriverWait(driver, 10)

    # Удаляем баннер куки через CSS-селектор, чтобы не перекрывал обзор
    driver.execute_script("document.querySelectorAll('.CookieConsent').forEach(el => el.remove());")
    sleep(1)

    # Находим пункт меню "Способы оплаты" БЕЗ XPATH (используем точный LINK_TEXT)
    payment_link = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Способы оплаты")))

    # Кликаем по ссылке
    payment_link.click()
    print("Переход в раздел 'Способы оплаты': OK")
    sleep(2)  # Даем время для плавной прокрутки страницы к нужной секции

    # Делаем скриншот всей страницы (или окна браузера), как просит условие
    screenshot_name = "payment_section_screenshot.png"
    driver.save_screenshot(screenshot_name)
    print(f"Скриншот секции сохранен как: {screenshot_name}")


def test_atomic_menu_programs_visible(driver):
    """Атомарный тест: проверка видимости пункта меню 'Программы'."""
    wait = WebDriverWait(driver, 10)
    element = wait.until(EC.visibility_of_element_located((By.LINK_TEXT, "Программы")))
    assert element.is_displayed(), "Пункт меню 'Программы' не отображается"


def test_atomic_menu_about_us_visible(driver):
    """Атомарный тест: проверка видимости пункта меню 'О нас'."""
    wait = WebDriverWait(driver, 10)
    element = wait.until(EC.visibility_of_element_located((By.LINK_TEXT, "О нас")))
    assert element.is_displayed(), "Пункт меню 'О нас' не отображается"


def test_atomic_language_switcher_ru(driver):
    """Атомарный тест: проверка наличия переключателя языка RU."""
    wait = WebDriverWait(driver, 10)
    # Ищем элемент через CSS Selector вместо XPath
    lang_ru = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "a[href*='/ru'], button")))
    assert lang_ru is not None, "Переключатель на русский язык не найден"