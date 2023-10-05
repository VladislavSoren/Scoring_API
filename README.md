## Scoring API

### Стек: http, json, Redis

### Результат:

Реализован декларативный язык описания и система валидации запросов к HTTP API сервиса скоринга.

### Модули:

- `api.py` - главный файл с методами обработки `HTTP` запросов (`GET/POST`)
- `config.py` - конфигурационный файл (так же содержит аккаунты для тестирования)
- `fields`:
    - `fields.py` содержит классы полей запросов с внутренними проверками
    - `custom_errors.py` содержит кастомные ошибки валидации полей
- `validators.py` - содержит валидаторы (запросов, авторизации и т.д.)
- `handlers.py` - содержит методы обработки запросов `score_handler/interests_handler`
- `scoring.py` - в нём находятся функции ответов на запросы клиентов `get_score/get_interests`
- `test` - модуль тестирования

### Функционал:

- пользователь отправляет в `POST` запросе валидный `JSON` определенного формата на `локейшн/score`
  и в ответ получает `JSON` с score, либо `JSON` содержащий ошибку.
- пользовательотправляет в `POST` запросе валидный `JSON` определенного формата на `локейшн/interests`
  и в ответ получает `JSON` с interests, либо `JSON` содержащий ошибку.

### Тесты:

В модуле `test`:
  - unit:
    - `test_fields.py`: проверка валидации полей запроса.
    - `test_store.py`: проверка класса работы с БД.
  - integration:
      - `test_api.py`: проверка работы API.

### Инструкции по запуску:

0. `pip install -r requirements.txt`

- Запуск сервера:

1. `cd <Абсолютный путь к директории Scoring_API>`
2. `python api.py`

- Запуск тестов:
  - `docker container create --name redis_test -p 6379:6379 redis`
  - `cd <Абсолютный путь к директории Scoring_API>`
  - Unit: `python -m unittest discover -s test.unit -p "test_*.py"`
  - Integration: `python -m unittest discover -s test.integration -p "test_*.py"`
  - All: `python -m unittest`

* `docker rm redis_test`

### Реaлизован pre-commit для проверки на соответствие PEP8
