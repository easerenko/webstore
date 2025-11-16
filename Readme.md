# Настройка проекта

### Для создания виртуального окружения выполнить команду в терминале:
    python -m venv venv

### Для активации выполнить команду:
    для Linux и MacOS:
        source venv/bin/activate
    для Windows:
        venv\Scripts\activate.bat

# Установка зависимостей
### Для установки зависимостей, выполнить команду в терминале:
    pip install -r requirements.txt

### Для обновления списка зависимостей, выполнить команду в терминале:
    pip freeze > requirements.txt

### Web Driver
    для Windows:
        Скачать Selenium WebDriver с сайта https://chromedriver.chromium.org/downloads  
        (обязательно выбрать версию соотвествующую вашему браузеру)
    для Linux и MacOS:
        драйвер автоматически найдеться в системе

# Запуск автотестов
## Для запуска api авто-тестов, выполнить команду в терминале:
    python -m pytest tests/api/*

### Для запуска ui авто-тестов, выполнить команду в терминале:
    Для запусков автотестов на ui через терминал нужно передать путь к драйверу:
    python3 -m pytest -v --driver Chrome --driver-path ~/chrome tests/*

    Например:
    python3 -m pytest -v --driver Chrome --driver-path drivers/chromedriver tests/ui/test_ui.py
    python3 -m pytest -v tests/ui/test_ui.py

### Примечание:
    для Windows:
        Скачать webdriver и положить в дирректорию "derivers"
