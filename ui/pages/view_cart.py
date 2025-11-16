import allure

from selenium.common import TimeoutException

from ui.pages.base_page import BasePage
from ui.locators.elements import ViewCartLocators as Locators


class ViewCart(BasePage):
    """
    Class for payment page.
    Parameters:
        base_url (str): base url of the web application
        driver (webdriver): instance of webdriver
    """
    def __init__(self, base_url: str, driver):
        super().__init__(url=f"{base_url}/view_cart", driver=driver)

    @allure.step("Переход к оформлению заказа")
    def proceed_to_checkout(self, wait_time=5):
        try:
            cart_button = self.wait_for_element(locator=Locators.PROCEED_TO_CHECKOUT, timeout=wait_time)
        except TimeoutException:
            raise Exception("Отсутствует кнопка 'Proceed to checkout'")
        cart_button.click()
