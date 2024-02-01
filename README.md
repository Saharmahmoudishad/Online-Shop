# Online-Shop
erd:https://dbdiagram.io/d/656c217d56d8064ca044e198
run redis and celery to use celery for managing task
1.python manage.py runserver
2.redis-server
3.python -m celery -A django_celery worker
