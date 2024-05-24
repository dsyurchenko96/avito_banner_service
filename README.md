# Сервис баннеров

## Описание

Управление баннерами для Авито с помощью FastAPI, деплой в Docker с PostgreSQL.

## Структура проекта

- `banner_service/`:
    - `app/`:
        - `main.py`: Основной файл с настройками приложения и маршрутизацией.
        - `db/`: Модуль с основными настройками базы данных.
        - `models/`: Модели запросов и ответов для CRUD (Pydantic) и модели для базы данных (SQLAlchemy).
        - `routers/`: Папка для обработки запросов API.
        - `test/`: Модуль с тестами и их конфигурацией
- `.pre-commit-config.yaml`: Линтеры в формате pre-commit-hooks.
- `setup.py`: Сборщик модулей для проекта и разрешения конфликтов импорта.
- `Makefile`: Точка запуска контейнеров и работы с БД.
- `compose.yaml`: Файл конфигурации для контейнеров Docker.
- `Dockerfile`: Файл для создания образов Docker.
- `requirements.txt`: Файл с зависимостями.

## Требования

- **Docker**

## Используемые библиотеки

- FastAPI
- Uvicorn
- Pydantic
- SQLAlchemy
- Psycopg2-binary
- pytest

## Установка

1. Клонируйте репозиторий.
2. Запустите Docker.
3. Введите команду ```make```.

## Использование

- Для запуска контейнеров - `make up`.
- Для остановки контейнеров - `make down`.
- Для просмотра базы данных - `make view_db`.
- Для заполнения базы данных - `make populate`. Команда генерирует валидные данные для таблицы, очищая базу данных перед
  заполнением.
- Для запуска тестов - `make test`
- Для очистки контейнеров и образов - `make clean`.
- Для перестройки проекта - `make rebuild`.

Сервер будет развернут на localhost - 0.0.0.0:8000.
