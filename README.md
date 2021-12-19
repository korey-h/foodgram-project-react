# praktikum
### Описание
Проект собирает рецепты блюд от пользователей и помогает сформировать корзину для покупок ингредиентов для выбранных рецептов. 
Доступ и управление к данным возможен по API. Структура API описна в в файле docs/redoc.yaml
, после развертывания проекта описание доступно по адресу <host_IP>/api/docs/

### Технологии
django 3.0.5
python 3.8
docker 3.8
postgresql 12.4
Gunicorn 20.0.4

### Развертывание проекта
- установите на сервер проекта Docker и docker-compose 
- создайте папку для проекта и скопируйте в нее папки из репозитория: infra, frontend, docs
- запустите терминал (bash), перейдите в папку infra проекта и выполните команду
docker-compose up

- после завершения сборки контейнеров docker (появятся сообщения done) поочереди выполнить команды:
    + docker-compose exec web python manage.py makemigrations --noinput
    + docker-compose exec web python manage.py migrate --noinput
    + docker-compose exec web python manage.py collectstatic --no-input
 - при первом запуске проекта потребуется создать суперпользователя:
     - docker-compose exec web bash
     - python manage.py createsuperuser

### Авторы

Егор при поддержке Яндекс.Практикума

![Actions Status](https://github.com/korey-h/foodgram-project-react/actions/workflows/main.yml/badge.svg)
