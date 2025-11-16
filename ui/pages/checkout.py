import allure

from selenium.common import TimeoutException

from ui.pages.base_page import BasePage
from ui.locators.elements import CheckoutLocators as Locators


class Checkout(BasePage):
    """
    Class for checkout page.
    Parameters:
        base_url (str): base url of the web application
        driver (webdriver): instance of webdriver
    """
    def __init__(self, base_url: str, driver):
        super().__init__(url=f"{base_url}/checkout", driver=driver)

    @allure.step("Нажатие кнопки оформления заказа")
    def place_order(self, wait_time=5):
        try:
            cart_button = self.wait_for_element(locator=Locators.PLACE_ORDER, timeout=wait_time)
        except TimeoutException:
            raise Exception("Отсутствует кнопка оформления заказа")
        cart_button.click()
