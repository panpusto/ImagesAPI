# **Images API**
This app is based on Django REST Framework. It allows users to upload images, generate thumbnails and expiring link depends on their account tier.
---
## Contents
* [Main technologies used](#main-technologies-used)
* [Features implemented](#features-implemented)
* [How to start project locally](#how-to-start-project-locally)
* [URLs](#urls)

---
## **Main technologies used**
- Django and Django REST Framework
- PostgreSQL
- Celery
- Redis
- Pillow
- Docker
- docker-compose
- pytest

***if you interested in details check **requirements.txt** file***

---
## **Features implemented**
- available only for logged in users
- users can upload images via HTTP
- users can list their uploaded images
- admin UI created via django-admin
- admins can create custom account tiers with the following things configurable:
    - thumbnail size
    - presence of the link to original file
    - ability to create expiring link
- three built-in account tiers:
    - users with `Basic` plan after uploading an image get:
        - a link to the thumbnail that's 200px height
    - users with `Premium` plan after uploading an image get:
        - a link to the thumbnail that's 200px height
        - a link to the thumbnail that's 400px height
        - a link to the original file
    - users with `Enterprise` plan after uploading an image get:
        - a link to the thumbnail that's 200px height
        - a link to the thumbnail that's 400px height
        - a link to the original file
        - the ability to generate a link to the uploaded image that expires after several seconds (user can specify any number between 300 and 30000 seconds) and download it
- generated expiring link to download an image works for unauthorized users too
- caching and distributed task queue

---
## **How to start project locally**
The easiest way to start project locally is to run docker-compose.

1. Clone this repo
2. Change directory to repo root folder
3. Run `docker-compose up --build`
4. Make databse migration: `docker-compose exec backend python manage.py migrate`
5. Create superuser: ` docker-compose exec backend python manage.py createsuperuser`
6. Type admin username, email and password.
7. Now you can visit: `127.0.0.1:8000/admin` or `localhost:8000/admin` to log in to admin panel.
---
## **URLs**
- http://127.0.0.1:8000/admin/
- http://127.0.0.1:8000/api-auth/login
- http://127.0.0.1:8000/api/v1/images/
- http://127.0.0.1:8000/api/v1/images/expiring-link
- http://127.0.0.1:8000/api/schema/
- http://127.0.0.1:8000/api/schema/redoc/
- http://127.0.0.1:8000/api/schema/swagger-ui/
