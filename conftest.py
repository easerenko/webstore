import pytest
import logging.config

from os import path
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from settings import config
from api import AutomationApi
from utils.fake import Fake
from ui.pages.auth_page import LoginPage


logging_file_path = path.join(path.dirname(path.abspath(__file__)), "logging.ini")
logging.config.fileConfig(logging_file_path)

# pytest_plugins = [
#     "src.actions.base"
# ]

def pytest_addoption(parser):
    parser.addini("headless", "Headless mode")


@pytest.fixture(scope="session")
def api():
    return AutomationApi(base_url=config()['source']['api_url'])


@pytest.fixture
def user_info():
    fake = Fake()

    data = {
        "name": fake.name(),
        "email": fake.email(),
        "password": fake.password(length=6),
        "title": fake.title(),
        "birth_date": fake.birth_date(),
        "birth_month": fake.month(),
        "birth_year": fake.year(),
        "firstname": fake.name(),
        "lastname": fake.name(),
        "company": fake.name(),
        "address1": fake.address(),
        "address2": fake.address(),
        "country": fake.country(),
        "zipcode": fake.zipcode(),
        "state": fake.city(),
        "city": fake.city(),
        "mobile_number": fake.mobile_number(),
    }
    return data

@pytest.fixture
def card_info():
    fake = Fake()

    data = {
        "card_name": fake.name().upper(),
        "card_number": fake.card_number(),
        "expiry_month": fake.month(),
        "expiry_year": fake.year(),
        "cvc": fake.card_cvc()
    }
    return data

@pytest.fixture
def create_user(api, user_info):
    resp = api.create_user(user_data=user_info)

    yield resp

    api.delete_user(email=user_info["email"], password=user_info["password"])


@pytest.fixture
def verify_login(api, user_info):
    resp = api.verify_login(email=user_info["email"], password=user_info["password"])

    yield resp


@pytest.fixture(scope="session")
def web():
    service = Service(ChromeDriverManager().install())
    browser = webdriver.Chrome(service=service)
    browser.set_window_size(1520, 810)
    # yield browser

    yield LoginPage(base_url=config()['source']['base_url'], driver=browser)
    browser.quit()

@pytest.fixture(scope="session")
def web_auth(api, web):
    fake = Fake()

    user_info = {
        "name": fake.name(),
        "email": fake.email(),
        "password": fake.password(length=8),
        "title": fake.title(),
        "birth_date": fake.birth_date(),
        "birth_month": fake.month(),
        "birth_year": fake.year(),
        "firstname": fake.name(),
        "lastname": fake.name(),
        "company": fake.name(),
        "address1": fake.address(),
        "address2": fake.address(),
        "country": fake.country(),
        "zipcode": fake.zipcode(),
        "state": fake.city(),
        "city": fake.city(),
        "mobile_number": fake.mobile_number(),
    }
    api.create_user(user_data=user_info)

    web.load_page()
    web.enter_username(user_info["email"])
    web.enter_password(user_info["password"])
    web.click_login_button()

    cookies = web.get_user_cookie()
    web.add_cookies(cookies)

    yield web, cookies, user_info

    api.delete_user(email=user_info["email"], password=user_info["password"])
