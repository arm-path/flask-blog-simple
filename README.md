
# Сайт: Пример простого блога на Flask.

### О проекте:

Реализован в учебных целях после прохождения учебных видео курсов, и прочтения учебных материалов.

### Функционал:

1. Авторизация пользователя в системе. (flask-security).
2. Создание, редактирование постов и тегов.
3. Представление поста и списока постов, поиск по постам.
4. Фильтрация по тегам.
5. Административная панель. (flask-admin, flask-security).

### Внешний вид:
Каталог <b>README \ images \ ...</b>

### Начало работы:

#### 1. Установить зависимости:
> pip install -r requirements.txt
#### 2. Внести изменения в файл configuration.py.
#### 3. Применить миграции и создать таблицы:
> flask db init \
> flask db migrate -m 'Initial migrate' \
> flask db upgrade \
#### 4. Создать пользователя, Консоль python:
> from app import app, user_datastore \
> from models import db, User, Role \
> user_datastore.create_user(email='test@example.com', password='password') \
> db.session.commit()
#### 5. Запустить сервер flask.
> python main.py
