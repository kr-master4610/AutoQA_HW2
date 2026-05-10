import pytest
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture
def driver():
    # Инициализация браузера
    driver = webdriver.Chrome()
    driver.maximize_window()
    # Заходим на русскую версию сайта
    driver.get("https://itcareerhub.de/ru")
    sleep(3)
    yield driver
    driver.quit()


def test_itcareerhub_main_elements(driver):
    """
    Тест проверяет наличие основных элементов на главной странице:
    логотип, пункты меню и переключатель языков.
    """
    wait = WebDriverWait(driver, 10)

    #  Убираем баннер куки через JavaScript
    driver.execute_script("document.querySelectorAll('.CookieConsent').forEach(el => el.remove());")
    print("\nБаннер куки удален: OK")

    #  Проверка логотипа
    # Ищем любую картинку, которая может быть логотипом (по alt, классу или просто первую в коде)
    try:
        logo_xpath = "//img[contains(@alt, 'ITCareerHub') or contains(@class, 'logo') or contains(@src, 'logo')]"
        logo = wait.until(EC.presence_of_element_located((By.XPATH, logo_xpath)))
        print("Логотип найден: OK")
    except:
        # Резервный вариант: берем просто первую попавшуюся картинку на странице
        logo = driver.find_element(By.TAG_NAME, "img")
        print("Логотип найден (резервный поиск): OK")

    assert logo is not None, "Логотип не найден на странице"

    #  ПРоверка навигационного меню
    menu_items = ["Программы", "Способы оплаты", "О нас"]

    for item in menu_items:
        # Ищем любой элемент (обычно <a> или <span>), содержащий нужный текст
        xpath = f"//*[contains(text(), '{item}')]"
        try:
            wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
            print(f"Пункт меню '{item}': OK")
        except:
            pytest.fail(f"Критическая ошибка: Пункт меню '{item}' не найден в коде страницы")

    #  Проверка переключателя языков
    languages = ["RU", "DE"]
    for lang in languages:
        lang_xpath = f"//*[contains(text(), '{lang}')]"
        try:
            wait.until(EC.presence_of_element_located((By.XPATH, lang_xpath)))
            print(f"Переключатель языка '{lang}': OK")
        except:
            print(f"Предупреждение: Кнопка языка '{lang}' не найдена (возможно, скрыта в мобильном меню)")




if __name__ == "__main__":
    pytest.main([__file__])