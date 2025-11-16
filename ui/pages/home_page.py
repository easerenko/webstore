import allure

from selenium.common import TimeoutException

from ui.pages.base_page import BasePage
from ui.locators.elements import HomePageLocators as Locators


class HomePage(BasePage):
    """
    Class for home page.
    Parameters:
        base_url (str): base url of the web application
        driver (webdriver): instance of webdriver
    """
    def __init__(self, base_url: str, driver):
        super().__init__(url=base_url, driver=driver)

    @allure.step("Добавление товара в корзину")
    def add_to_cart(self, wait_time=5):
        try:
            add_to_cart_button = self.wait_for_element(locator=Locators.ADD_TO_CART, timeout=wait_time)
        except TimeoutException:
            raise Exception("Отсутствует кнопка 'Add to cart'")
        add_to_cart_button.click()

    @allure.step("Переход в корзину")
    def view_cart(self, wait_time=5):
        try:
            cart_button = self.wait_for_element(locator=Locators.ENTER_CART, timeout=wait_time)
        except TimeoutException:
            raise Exception("Отсутствует кнопка 'View cart'")
        cart_button.click()
