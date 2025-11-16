import logging
import allure


@allure.title("Тест метода получения списка товаров")
def test_product_list(api):
    resp = api.get_product_list()

    logging.info("Проверка получения статус-кода 200")
    assert resp.status_code == 200

    logging.info(f"Проверка наличия списка товаров в ответе: {resp.json()}")
    assert "products" in resp.json()


@allure.title("Тест метода получения списка брендов")
def test_brand_list(api):
    resp = api.get_brand_list()

    logging.info("Проверка получения статус-кода 200")
    assert resp.status_code == 200

    logging.info(f"Проверка наличия списка брендов в ответе: {resp.json()}")
    assert "brands" in resp.json()


@allure.title("Тест метода поиска товара")
def test_search_product(api):
    search_product = "Tshirts"

    resp = api.search_product(search_product)

    logging.info("Проверка получения статус-кода 200")
    assert resp.status_code == 200

    logging.info(
        f"Проверка наличия искомого товара {search_product} в ответе: "
        f"{resp.json()["products"][0]["category"]["category"]}"
    )
    assert "Tshirts" in resp.json()["products"][0]["category"]["category"]


@allure.title("Тест метода подтверждения существования учетной записи")
def test_verify_login(api, verify_login):
    resp = api.verify_login(email="delichamir@gmail.com", password="delichPWD")

    logging.info("Проверка получения статус-кода 200")
    assert resp.status_code == 200

    logging.info(f"Проверка наличия текста 'User exists!' в ответе: {resp.json()['message']}")
    assert "User exists!" in resp.json()['message']


@allure.title("Тест создания учетной записи")
def test_create_and_verify_login(api, create_user, verify_login):
    resp = verify_login

    logging.info("Проверка получения статус-кода 200")
    assert resp.status_code == 200

    logging.info(f"Проверка наличия текста 'User exists!' в ответе: {resp.json()['message']}")
    assert "User exists!" in resp.json()['message']


@allure.title("Тест метода создания учетной записи")
def test_create_user(api, create_user):
    resp = create_user

    logging.info("Проверка получения статус-кодов 200 или 201")
    assert resp.status_code in [200, 201]

    logging.info(f"Проверка наличия текста 'User created!' в ответе: {resp.json()['message']}")
    assert "User created!" in resp.json()['message']


@allure.title("Тест метода обновления учетной записи")
def test_update_user(api, create_user, user_info):
    user_info["name"] = "new_name"
    resp = api.update_user(user_data=user_info)

    logging.info("Проверка получения статус-кода 200")
    assert resp.status_code == 200

    logging.info(f"Проверка наличия текста 'User updated!' в ответе: {resp.json()['message']}")
    assert "User updated!" in resp.json()['message']
