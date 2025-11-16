import allure

from selenium.common import TimeoutException

from ui.pages.base_page import BasePage
from ui.locators.elements import PaymentLocators as Locators


class Payment(BasePage):
    """
        Class for payment page.
        Parameters:
            base_url (str): base url of the web application
            driver (webdriver): instance of webdriver
        """
    def __init__(self, base_url: str, driver):
        super().__init__(url=f"{base_url}/payment", driver=driver)

    @allure.step("Ввод названия карты")
    def enter_card_name(self, card_name, wait_time=5):
        try:
            card_name_field = self.wait_for_element(locator=Locators.CARD_NAME_ENTER, timeout=wait_time)
        except TimeoutException:
            raise Exception("Отсутствует поле ввода названия карты")
        card_name_field.clear()
        card_name_field.send_keys(card_name)

    @allure.step("Ввод номера карты")
    def enter_card_number(self, card_number, wait_time=5):
        try:
            card_number_field = self.wait_for_element(locator=Locators.CARD_NUMBER_ENTER, timeout=wait_time)
        except TimeoutException:
            raise Exception("Отсутствует поле ввода номера карты")
        card_number_field.clear()
        card_number_field.send_keys(card_number)

    @allure.step("Ввод CVC")
    def enter_cvc(self, cvc, wait_time=5):
        try:
            cvc_field = self.wait_for_element(locator=Locators.CVC_ENTER, timeout=wait_time)
        except TimeoutException:
            raise Exception("Отсутствует поле ввода CVC")
        cvc_field.clear()
        cvc_field.send_keys(cvc)

    @allure.step("Ввод месяца истечения срока действия карты")
    def enter_expiry_month(self, expiry_month, wait_time=5):
        try:
            month_field = self.wait_for_element(locator=Locators.EXPIRY_MONTH_ENTER, timeout=wait_time)
        except TimeoutException:
            raise Exception("Отсутствует поле ввода месяца истечения срока действия карты")
        month_field.clear()
        month_field.send_keys(expiry_month)

    @allure.step("Ввод года истечения срока действия карты")
    def enter_expiry_year(self, expiry_year, wait_time=5):
        try:
            year_field = self.wait_for_element(locator=Locators.EXPIRY_YEAR_ENTER, timeout=wait_time)
        except TimeoutException:
            raise Exception("Отсутствует поле ввода года истечения срока действия карты")
        year_field.clear()
        year_field.send_keys(expiry_year)

    @allure.step("Нажатие кнопки 'Pay and confirm order'")
    def pay_and_confirm_order(self, wait_time=5):
        try:
            cart_button = self.wait_for_element(locator=Locators.PAY_AND_CONFIRM_ORDER, timeout=wait_time)
        except TimeoutException:
            raise Exception("Отсутствует кнопка 'Pay and confirm order'")
        cart_button.click()
