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

#### 4. Запустить docker, зайти в PowerShell и выполнить следующие команды для развертывания карты ПФО локально (OSM):

> $img = "osrm/osrm-backend:latest"
> docker run -t -v "${pwd}/data:/data" osrm/osrm-backend osrm-extract -p /opt/car.lua /data/volga-fed-district-251203.osm.pbf
> docker run -t --rm -v "${pwd}//data:/data" osrm/osrm-backend osrm-partition /data/volga-fed-district-251203.osrm
> docker run -t --rm -v "${PWD}:/data" osrm/osrm-backend osrm-customize /data/volga-fed-district-251203.osrm
> docker run -t -i --rm -p 5000:5000 -v "${PWD}:/data" osrm/osrm-backend osrm-routed --algorithm mld /data/volga-fed-district-251203.osrm


### 5. Запустить проект

python manage.py runserver



### Основные ссылки:

#### Админка
localhost:8000/admin 


#### Swagger
localhost:8000/swagger
