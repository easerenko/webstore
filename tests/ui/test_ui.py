import logging

import allure
import pytest_check as check

from settings import config
from ui.pages.checkout import Checkout
from ui.pages.home_page import HomePage
from ui.pages.payment import Payment
from ui.pages.view_cart import ViewCart
from ui.locators.elements import PaymentDoneLocators as Locators


@allure.title("Тест аутентификации пользователя")
def test_login(web, create_user, user_info):
    web.load_page()
    web.enter_username(username=user_info["email"])
    web.enter_password(password=user_info["password"])
    web.click_login_button()

    logging.info("Проверка загрузки главной страницы после аутентификации пользователя")
    assert web.get_current_url() == config()['source']['base_url']


@allure.title("Тест куки аутентификации пользователя")
def test_user_cookies(web_auth):
    web, cookies, user_info = web_auth
    web.add_cookies(cookie=cookies)
    web.get_page(page_url=config()['source']['auth_url'])

    logging.info("Проверка загрузки главной страницы при открытии страницы авторизации авторизованным пользователем")
    assert web.get_current_url() == config()['source']['base_url']


@allure.story("Тесты по основным сценариям заказа товара")
class TestOrder:
    @allure.title("Тест сценария полного заказа с оплатой")
    def test_full_order(self, web, web_auth, card_info, base_url=config()['source']['base_url']):
        home_page = HomePage(base_url=base_url, driver=web.driver)
        home_page.add_to_cart()
        home_page.view_cart()

        cart_page = ViewCart(base_url=base_url, driver=web.driver)
        cart_page.proceed_to_checkout()

        checkout_page = Checkout(base_url=base_url, driver=web.driver)
        checkout_page.place_order()

        payment_page = Payment(base_url=base_url, driver=web.driver)
        payment_page.enter_card_name(card_name=card_info["card_name"])
        payment_page.enter_card_number(card_number=card_info["card_number"])
        payment_page.enter_cvc(cvc=card_info["cvc"])
        payment_page.enter_expiry_month(expiry_month=card_info["expiry_month"])
        payment_page.enter_expiry_year(expiry_year=card_info["expiry_year"])
        payment_page.pay_and_confirm_order()

        logging.info("Проверка наличия заголовка 'Order Placed!'")
        check.is_true(
            web.wait_for_element(locator=Locators.ORDER_PLACED, timeout=10),
            msg="Заголовок 'Order Placed!' отсутствует"
        )

        logging.info("Проверка загрузки страницы завершения заказа")
        check.is_in("payment_done", web.get_current_url(), msg="Страница завершения заказа не загрузилась")
