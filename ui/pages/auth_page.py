import allure

from selenium.common import TimeoutException

from ui.pages.base_page import BasePage
from ui.locators.elements import AuthPageLocators as Locators


class LoginPage(BasePage):
    """
    Class for authentication page.
    Parameters:
        base_url (str): base url of the web application
        driver (webdriver): instance of webdriver
    """
    def __init__(self, base_url, driver):
        super().__init__(url=f"{base_url}/login", driver=driver)

    @allure.step("Ввод логина")
    def enter_username(self, username, wait_time=5):
        try:
            username_field = self.wait_for_element(locator=Locators.LOGIN_ENTER, timeout=wait_time)
        except TimeoutException:
            raise Exception("Отсутствует поле ввода логина")
        username_field.clear()
        username_field.send_keys(username)

    @allure.step("Ввод пароля")
    def enter_password(self, password,  wait_time=5):
        try:
            password_field = self.wait_for_element(locator=Locators.PASSWORD_ENTER, timeout=wait_time)
        except TimeoutException:
            raise Exception("Отсутствует поле ввода пароля")
        password_field.clear()
        password_field.send_keys(password)

    @allure.step("Нажатие кнопки входа")
    def click_login_button(self,  wait_time=5):
        try:
            login_button = self.wait_for_element(locator=Locators.LOGIN_BUTTON, timeout=wait_time)
        except TimeoutException:
            raise Exception("Отсутствует кнопка входа")
        login_button.click()

    @allure.step("Сохранение скриншота")
    def save_screenshot(self, file_path: str):
        self.driver.save_screenshot(file_path)
