import allure

from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class BasePage:
    """
    Base class for all pages.
    Parameters:
        url (str): URL of the page
        driver (WebDriver): Instance of WebDriver
    """
    def __init__(self, url, driver):
        self.url = url
        self.driver = driver

    @allure.step("Открытие страницы")
    def load_page(self):
        self.driver.get(self.url)

    @allure.step("Ожидание загрузки элемента")
    def wait_for_element(self, locator, timeout: int):
        return WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located(locator))

    @allure.step("Получение куки пользователя")
    def get_user_cookie(self):
        return self.driver.get_cookie(name="sessionid")

    @allure.step("Добавление куки пользователя")
    def add_cookies(self, cookie):
        self.driver.add_cookie(cookie)

    @allure.step("Открытие страницы")
    def get_page(self, page_url):
        self.driver.get(page_url)

    @allure.step("Получение url текущей страницы")
    def get_current_url(self):
        return self.driver.current_url

    @allure.step("Закрытие модального окна с согласием на использование персональных данных")
    def close_person_data_modal(self):
        try:
            button = WebDriverWait(self.driver, 1).until(
                EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Соглашаюсь']"))
            )
            button.click()
        except TimeoutException:
            pass
