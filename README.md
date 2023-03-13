![example workflow](https://github.com/SidVi990/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)
# API_YaMDb

## Описание:
Проект доступен по адресу: https://ya-mdb.sytes.net

«YaMDb» предоставляет информацию о различных произведениях (фильмы, книги, музыка). Пользователи могут просматривать информацию о произведении или читать рецензии. Для зарегестрированных пользователей доступна возможность ставить оценки, писать рецензии и оставлять комментарии.

YaMDb не предоставляет доступа к самим произведениям, а лишь хранит информацию о них.

## Стек технологий:
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)

![DjangoREST](https://img.shields.io/badge/DJANGO-REST-ff1709?style=for-the-badge&logo=django&logoColor=white&color=ff1709&labelColor=gray)

![JWT](https://img.shields.io/badge/JWT-black?style=for-the-badge&logo=JSON%20web%20tokens)

![Git](https://img.shields.io/badge/git-%23F05033.svg?style=for-the-badge&logo=git&logoColor=white)

![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)

## Как запустить проект:

- Склонируйте репозитрий на свой компьютер

- Создайте .env файл в директории infra/, в котором должны содержаться следующие переменные:

> DB_ENGINE=django.db.backends.postgresql

> DB_NAME= # название БД\ 

> POSTGRES_USER= # имя пользователя

> POSTGRES_PASSWORD= # пароль для доступа к БД

> DB_HOST=db

> DB_PORT=5432

- Из папки `infra/` соберите образ при помощи docker-compose `$ docker compose up -d --build`

- Создайте и примените миграции `$ docker-compose exec web python manage.py makemigrations`, а затем `$ docker-compose exec web python manage.py migrate`

- Соберите статику `$ docker-compose exec web python manage.py collectstatic --no-input`

- Для доступа к админке не забудьте создать суперюзера `$ docker-compose exec web python manage.py createsuperuser`

## Документация к проекту

Документация для API после установки доступна по адресу `http://localhost/redoc`

## Регистрация

Выполните POST-запрос к `http://localhost/api/v1/auth/signup/` передав поля username и email.

API вышлет код подтверждения на вашу электронную почту.
Он понадобится на следующем этапе.

## Аутентификация

Выполните POST-запрос к `http://localhost/api/v1/auth/token/` передав поля username и confirmation_code.
Код можно получить по электронной почте из предыдущего этапа.

API вернет JWT-токен в формате:
```
{
    'Ваш токен': "ХХХХХХХХХХХ"
}
```

При отправке запроcов передавайте токен в заголовке `Authorization: Bearer <токен>`

## Как работает API_YaMDb

Пример GET-запроса для получения списка всех произведений:
```
url = 'http://localhost/api/v1/titles/'
```
Ответ API_Yatube:
```
Статус- код 200

{
  "count": 0,
  "next": "string",
  "previous": "string",
  "results": [
      { ... }
  ]
}
```
Пример POST-запроса для добавления нового отзыва:
```
url = 'hhttp://localhost/api/v1/titles/{title_id}/reviews/'
data = {
            "text": "string",
            "score": 1
        }
headers = {'Authorization': 'Bearer your_token'}
```
Ответ API_Yatube:
```
Статус- код 200

[
  {
    "id": 0,
    "text": "string",
    "author": "string",
    "score": 1,
    "pub_date": "2019-08-24T14:15:22Z"
  }
]
```

## Авторы

[Александр Федорович](https://github.com/Aleksandr140590)

[Виктор Назипов](https://github.com/VRN-lab)

[Евгений Малый](https://github.com/SidVi990)
