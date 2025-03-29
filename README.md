# Time_Tracker
Проект RESTful для учёта отработанных часов в проекте
## Содержание

- [Установка](#установка)
- [Использование](#использование)

## Установка

1. Клонируйте репозиторий:

```bash
   git clone https://github.com/DanielNegusto/time_tracker.git
   cd time_tracker
```

2. Создайте и активируйте виртуальное окружение:

```bash
python -m venv myenv
source venv/bin/activate  # для Linux/Mac
venv\Scripts\activate  # для Windows
```

3. Убедитесь что у вас установлен Just, если нет Скачайте его с официального репозитроия 

4. Запустите команду 
```bash
  just up 
```
У вас подтянутся зависимости
Запустится локально сервер
по адресу http://localhost:8000/
Также создаётся суперпользователь с помощью него можно зайти в админку 
username - admin
password - admin
# Использование:

## Аутентификация
1. Для того что бы взаимодействовать с проектом нужен token
POST запрос
http://localhost:8000/users/token/
пример запроса:
{
   "username": "admin",
    "password": "admin",
}
2. Для того что бы зарегистрировать пользователя 
POST запрос
http://localhost:8000/users/register/
пример запроса:
{
   "username": "user",
   "password": "test",
}
## Проекты
Сначала добавьте в заголовки запроса
Authorization Token <ваш_токен>
### Эндпоинты
1. GET запрос
http://localhost:8000/projects/
получаем список всех проектов
2. POST запрос
http://localhost:8000/projects/
пример запроса:
{
   "name": "Testname",
   "description": "test",
}
Создаётся проект
3. POST запрос
http://localhost:8000/add_time/
пример запроса:
{
   "project_id": id_проекта,
    "hours": часы проекта,
    "date": "dd.mm.yyyy" дата добавления
}
Добавляет отработанные часы для проекта
4. POST запрос
http://localhost:8000/report/<id_проекта>/
пример запроса:
{
   "start_date": "dd.mm.yyyy", дата начала отчета
     "end_date": "dd.mm.yyyy" дата конца отчёта
}
получаем список со словарём в которм id пользователя и его отработанные часы
## Важно: отчёт может просматривать только админ или модератор для того что бы сделать пользователя модератором 
в админке нужно сделать поле is_moderator True

## Линтеры
В проекте также реализованы линтеры flake8 и black для запуска используется команда 
```bash
    just lint
```