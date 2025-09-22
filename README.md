# YADRO Lab test
Тестовое задание в проект “Система проверки работоспособности дистрибутивов на основе Yocto”.
Проект для автоматического тестирования Apache

## Описание проекта

Проект состоит из двух основных компонентов:

- Target - контейнер с веб-сервером Apache2, обслуживающим статическую страницу
- Agent - контейнер с набором тестов на Python для проверки работоспособности target

Тесты проверяют:

- запущен ли веб-сервер
- есть ли в логах веб-сервера ошибки за последние Н минут (Н - задается в параметрах docker-compose)
- корректно ли веб-сервер показывает /index, а также как он выдает ошибки на несуществующие страницы

Дополнительно:
- Реализованы смок-тесты для проверки работоспособности штатных пакетов - tar, ln 
- Возможность кастомизации credentials для подключения к target
- Возможность запуска с подключением к внешнему targe

## Требования

- Docker 20.10+
- Docker Compose (v2)
- Python 3.10+ 
- Доступ к портам 8080 и 2222

## Сборка и запуск

1. Склонируйте репозиторий
2. Перейдите в папку проекта
3. Запустите скрипт run.sh
```
./run.sh
```
**В случае возниковения ошибки:**
измените права пользователя и попробуйте снова
```
chmod +x run.sh target/start.sh
```

Чтобы запустить тесты с измененными параметрами (переменными окружения), присвойте им новое значение в строке перед запуском run.sh:
```
HTTP_TIMEOUT=10 ./run_tests_console.sh
```
**Чтобы запустить с подключением к внешнему target измените  TARGET_HOST на IP-адрес или hostname внешнего сервера:**
```
TARGET_HOST=192.168.1.50 \
TARGET_USER=admin \
TARGET_PASS=newsecret456 \
./run.sh
```
## Ожидаемый результат

```
                                                                                                                  
================================================================== test session starts ====================================================================
platform linux -- Python 3.11.2, pytest-8.4.2, pluggy-1.6.0 -- /usr/bin/python3
cachedir: .pytest_cache
rootdir: /app
collected 5 items                                                                                                                                                                    

tests/test_http_pages.py::test_http_pages[/index.html-200] PASSED                                                                                                              [ 20%]
tests/test_http_pages.py::test_http_pages[/nonexistent-404] PASSED                                                                                                             [ 40%]
tests/test_log_recent_errors.py::test_logs_recent_errors PASSED                                                                                                                [ 60%]
tests/test_smoke.py::test_tar_works PASSED                                                                                                                                     [ 80%]
tests/test_smoke.py::test_ln_works PASSED                                                                                                                                      [100%]

================================================================== 5 passed in 0.96s ======================================================================
```


## Ручной запуск
1. Склонировать репозиторий, перейти в папку проекты
2. Сборка Docker-образов
```
docker compose build
```
3. Проверить созданные образы:
```
docker images
```
4. Запустить target (Apache + SSH)
```
docker compose up -d target
```
Проверить, что контейнер работает
```
docker ps
```
Убедиться, что target доступен
HTTP: открыть в браузере http://localhost:8080/index.html
Должно отобразиться: Hello from Apache!
SSH: попробовать подключиться
```
ssh user@localhost -p 2222 # пароль: password
```
5. Запустить agent с тестами:
```
docker compose run --rm agent
```
**Запустить конкретный тест:**
```
docker compose run --rm agent
```
6. Остановка
```
docker compose run --rm agent
```

## Переменные окружения
настраиваются в docker-compose.yml
| Переменная | Описание |
| --- | --- |
| TARGET_HOST | Хост target-контейнера |
| TARGET_SSH_PORT  | SSH порт target |
| TARGET_HTTP_PORT  | HTTP порт target |
| TARGET_USER | SSH пользователь |
| TARGET_PASS | SSH пароль |
| LOG_INTERVAL | Интервал проверки логов (минуты) |
| HTTP_TIMEOUT | Таймаут HTTP запросов (секунды) |
| SSH_MAX_RETRIES | Максимальное количество попыток SSH подключения |
| SSH_RETRY_DELAY | Задержка между попытками SSH (секунды) |

## Структура тестов

**tests/conftest.py**

- Фикстуры для SSH подключения
- Управление конфигурацией

**tests/test_http_pages.py**

- Проверка HTTP статусов
- Валидация содержимого страниц

**tests/test_log_recent_errors.py**

- Анализ логов Apache
- Поиск ошибок за указанный период

**tests/test_smoke.py**

- смок-тесты tar, ln




