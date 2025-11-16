import secrets
import string
from random import choice

from faker import Faker

Faker.seed()
fake = Faker(locale="ru_RU")


class Fake:

    @staticmethod
    def name() -> str:
        """
        Генерация имени

        :return: Имя
        """
        return fake.name()

    @staticmethod
    def email() -> str:
        """
        Генерация почты

        :return: Почта
        """
        return fake.email()

    @staticmethod
    def password(length: int) -> str:
        """
        Генерация пароля

        :return: Пароль
        """
        alphabet = string.ascii_letters + string.digits + string.punctuation
        password = ''.join(secrets.choice(alphabet) for _ in range(length))

        return password

    @staticmethod
    def title() -> str:
        """
        Генерация звания

        :return: звание
        """
        title = ["Mr", "Mrs", "Miss"]
        return choice(title)

    @staticmethod
    def birth_date() -> str:
        """
        Генерация дня рождения

        :return: день рождение
        """
        return choice(range(1, 30))

    @staticmethod
    def month() -> str:
        """
        Генерация месяца рождения

        :return: месяц рождения
        """
        # return choice(range(1, 13))
        return fake.month()

    @staticmethod
    def year() -> str:
        """
        Генерация года рождения

        :return: год рождения
        """
        return fake.year()

    @staticmethod
    def address() -> str:
        """
        Генерация адреса

        :return: адрес
        """
        return fake.address()

    @staticmethod
    def country() -> str:
        """
        Генерация страны

        :return: страна
        """
        return fake.country()

    @staticmethod
    def zipcode() -> str:
        """
        Генерация индекса

        :return: индекс
        """
        return fake.postcode()

    @staticmethod
    def city() -> str:
        """
        Генерация города

        :return: город
        """
        return fake.city()

    @staticmethod
    def mobile_number() -> str:
        """
        Генерация номера телефона

        :return: номер телефона
        """
        return fake.phone_number()

    @staticmethod
    def card_number() -> str:
        """
        Генерация номера карты

        :return: Номер карты
        """
        return fake.credit_card_number()

    @staticmethod
    def card_cvc() -> str:
        """
        Генерация CVC

        :return: CVC
        """
        return fake.credit_card_security_code()
