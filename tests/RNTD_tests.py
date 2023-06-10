import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains


# Создаем объект Web Driver + игнорируем ошибку сертификата SSL
def get_driver():
    options = webdriver.ChromeOptions()
    options.add_argument('ignore-certificate-errors')
    driver = webdriver.Chrome(chrome_options=options)
    driver.get('https://gisogd.gov.ru/rntd')
    driver.maximize_window()
    wait = WebDriverWait(driver, 30)
    return driver, wait


def test_form_with_name():
    """
    RNTD-01. Работа формы поиска по названию документа
    """
    driver, wait = get_driver()
    action = ActionChains(driver)
    # Устанавливаем значение в поле ввода наименования документа
    wait.until(
        EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Введите наименование или номер']"))).click()
    action.send_keys('гидроизоляционные').perform()
    # Нажимаем на кнопку Найти
    wait.until(
        EC.presence_of_element_located((By.CLASS_NAME, "g-a11y-btn--primary"))).click()
    # Ожидаем загрузки списка документа
    wait.until(
        EC.presence_of_element_located((By.XPATH, "//article['.g-a11y-card-bg']")))
    # Подсчитываем количетво наденных элементов
    element_count = len(
        driver.find_elements(By.XPATH, "//article['.g-a11y-card-bg']"))
    # Ищем названия документов
    element_name = driver.find_elements(By.CLASS_NAME, "ba-mt-4")

    # Проверяем что в названии каждого выведенного документа присутствует введенное значение
    for e in element_name:
        assert e.text.__contains__("гидроизоляционные")
    # Количетво найденых документов больше 0
    assert element_count > 0

    driver.quit()


def test_form_with_number_and_strict():
    """
    RNTD-02. Работа формы поиска по номеру документа и строгом соответствии
    """
    driver, wait = get_driver()
    action = ActionChains(driver)
    # Устанавливаем значение в поле ввода номера документа
    wait.until(
        EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Введите наименование или номер']"))).click()
    action.send_keys('384-ФЗ').perform()
    # Устанавливаем чекбокс "Строгое соответствие"
    wait.until(EC.presence_of_element_located(
        (By.CLASS_NAME, "ba-ml-2"))).click()
    # Нажимаем на кнопку Найти
    wait.until(
        EC.presence_of_element_located((By.CLASS_NAME, "g-a11y-btn--primary"))).click()
    # Ожидаем загрузки списка документа
    wait.until(
        EC.presence_of_element_located((By.XPATH, "//article['.g-a11y-card-bg']")))
    # Подсчитываем количетво наденных элементов
    element_count = len(
        driver.find_elements(By.XPATH, "//article['.g-a11y-card-bg']"))
    # Ищем название номера документа
    element_name = driver.find_elements(By.XPATH, "//span[contains(text(),'384-ФЗ')]")

    # Проверяем что в название документа соответствует веденному значению
    for e in element_name:
        assert e.text == "384-ФЗ"
    # Количетво найденых документов = 1
    assert element_count == 1

    driver.quit()
