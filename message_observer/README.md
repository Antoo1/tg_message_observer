# telegram chat messages remover
    1. remove all your message from any group you have
    2. make exceptions for some chats

## Корневой URL:
/

## Репозиторий:
* TODO

## Авторы


## Язык реализации
python 3.12

## Описание сервиса
# todo

# Разработка

## Установка зависимостей

Создать виртаульное окружение через pyenv:

```bash
$ cd 
$ pyenv virtualenv 3.12 telegram_message_remover
$ pyenv local telegram_message_remover
```
Установить необходимые пакеты:

```bash
(telegram_message_remover)$ pip install -U setuptools pip pipenv wheel
(telegram_message_remover)$ pipenv install
(telegram_message_remover)$ pipenv install --dev
```

```bash
$ docker-compose up
```

# Запуск тестов

```bash
$ python -m pytest -vvs
```


# Запуск анализатора кода Flake

```bash
$ python -m flake8 -v
```


# Установка pre-commit hook

```bash
$ pre-commit install
```