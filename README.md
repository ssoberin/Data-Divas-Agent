# Data-Divas-Agent

### Инструкция по запуску бэка:

#### 1. Запустить БД:

docker-compose up -d

#### 2. Установить зависимости:

##### а). Развернуть venv:

python -m venv venv

##### б). Установка зависимостей

pip install -r requirements.txt

#### 3. Зайти в папку back, выполнить команды:

##### а). Применить миграции

python manage.py migrate

##### б). Создать супер-пользователя)

python manage.py createsuperuser

##### в). Создать статические файлы

python manage.py collectstatic --no-input

### 4. Запустить проект

python manage.py runserver



### Основные ссылки:

#### Админка
localhost:8000/admin 


#### Swagger
localhost:8000/swagger