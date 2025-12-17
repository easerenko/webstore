import json
import os
import sys
import pytest
import logging.config
import traceback

from pathlib import Path
from datetime import datetime
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


def pytest_terminal_summary(terminalreporter, exitstatus):
    stats = terminalreporter.stats
    results = {
        'timestamp': datetime.now().isoformat(),
        'exitstatus': exitstatus,
        'tests': {}
    }

    for status in ['passed', 'failed', 'skipped', 'error']:
        tests = stats.get(status, [])
        results['tests'][status] = [item.nodeid for item in tests]

    with open('test_results.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    terminalreporter.write_line("Результаты сохранены в test_results.json")


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
    web.close_person_data_modal()

    web.enter_username(user_info["email"])
    web.enter_password(user_info["password"])
    web.click_login_button()

    cookies = web.get_user_cookie()
    web.add_cookies(cookies)

    yield web, cookies, user_info

    api.delete_user(email=user_info["email"], password=user_info["password"])


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()

    if rep.when == "call" and rep.failed:
        filename = item.nodeid.split("::")[0]
        excinfo = rep.longrepr

        if hasattr(excinfo, 'traceback'):
            tb_lines = rep.longreprtext.split('\n')
            error_line = None
            for line in reversed(tb_lines):
                if 'File' in line and 'line' in line:
                    try:
                        error_line = int(line.split('line ')[1].split(',')[0])
                        break
                    except:
                        continue

            if error_line is None:
                exc_type, exc_value, exc_tb = sys.exc_info()
                if exc_tb:
                    error_line = exc_tb.tb_lineno
        else:
            error_line = 1

        print(f"::error file={filename} line={error_line} ::❌ ОШИБКА в {filename}:{error_line}")
        print(f"::error ::{rep.longreprtext}")

        lines = rep.longreprtext.split('\n')
        for i, line in enumerate(lines):
            if 'File' in line and 'line' in line:
                try:
                    lineno = int(line.split('line ')[1].split(',')[0])
                    print(f"::error file={filename} line={lineno} ::{line.strip()}")
                except:
                    pass

    # if rep.when == "call" and rep.failed:
    #     nodeid = item.nodeid
    #     filename = nodeid.split("::")[0]
    #     lineno = item.location[1]
    #
    #     print(f"::error file={filename},line={lineno} ::❌ ОШИБКА в {filename}:{lineno}")
    #     print(f"::error ::{rep.longreprtext}")
