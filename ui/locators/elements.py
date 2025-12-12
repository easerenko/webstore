from selenium.webdriver.common.by import By


class AuthPageLocators:
    """
    Локаторы страницы авторизации
    """
    # Локатор для поля ввода логина:
    LOGIN_ENTER = (By.CSS_SELECTOR, ".login-form [name='email']")
    # Локатор для поля ввода пароля:
    PASSWORD_ENTER = (By.CSS_SELECTOR, ".login-form [name='password']")
    # Локатор для кнопки входа:
    LOGIN_BUTTON = (By.CSS_SELECTOR, ".login-form [type='submit']")


class HomePageLocators:
    """
    Локаторы домашней страницы
    """
    # Локатор для кнопки "Add to Cart":
    ADD_TO_CART = (By.XPATH, "(//a[contains(@class, 'add-to-cart')])[1]")
    # Локатор для кнопки "Cart":
    ENTER_CART = (By.XPATH, "//a[@href='/view_cart']")


class ViewCartLocators:
    """
    Локаторы страницы корзины
    """
    # Локатор для кнопки "Proceed To Checkout":
    PROCEED_TO_CHECKOUT = (By.XPATH, "//a[contains(text(), 'Proceed To Checkout')]")


class CheckoutLocators:
    """
    Локаторы страницы проверки заказа
    """
    # Локатор для кнопки "Place Order":
    PLACE_ORDER = (By.XPATH, "//a[contains(text(), 'Place Order')]")


class PaymentLocators:
    """
    Локаторы страницы оплаты
    """
    # Локатор для кнопки "Pay and Confirm Order":
    PAY_AND_CONFIRM_ORDER = (By.XPATH, "//button[@data-qa='pay-button']")
    # Локатор для поля ввода наименования карты:
    CARD_NAME_ENTER = (By.CSS_SELECTOR, "#payment-form [name='name_on_card']")
    # Локатор для поля ввода номера карты:
    CARD_NUMBER_ENTER = (By.CSS_SELECTOR, "#payment-form [name='card_number']")
    # Локатор для поля ввода CVC:
    CVC_ENTER = (By.CSS_SELECTOR, "#payment-form [name='cvc']")
    # Локатор для поля ввода месяца истечения срока действия карты:
    EXPIRY_MONTH_ENTER = (By.CSS_SELECTOR, "#payment-form [name='expiry_month']")
    # Локатор для поля ввода года истечения срока действия карты:
    EXPIRY_YEAR_ENTER = (By.CSS_SELECTOR, "#payment-form [name='expiry_year']")


class PaymentDoneLocators:
    """
    Локаторы страницы завершения заказа
    """
    # Локатор для заголовка "Order Placed!":
    ORDER_PLACED = (By.XPATH, "//*[contains(text(), 'Order Placed!')]")
