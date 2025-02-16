# Starting a django project using Celery and Redis

## Start Redis

1. install redis (https://github.com/redis-windows/redis-windows).
2. open a command line (CMD).
3. Start Redis using the following command:

```BASH
redis-server.exe
```

## Start Celery Worker

1. Open the first terminal.
2. Navigate to the `crud_project` project directory using the command:
3. Run Celery Worker using the following command in CMD:

```bash
cd crud_project
celery -A crud_project worker -l info --pool=solo
```

## Start Celery Beat

1. Open a second terminal.
2. Navigate to the `crud_project` project directory using the command:
3. Run Celery Beat using the following command:

```bash
cd crud_project
celery -A crud_project beat -l INFO
```

## Create a superuser

```bash
cd crud_project
python manage.py createsuperuser
```

## Create random data in the database

### example 
```BASH 
cd crud_project
python manage.py autofill 10 product
```

### how to use
```bash
cd crud_project
python manage.py autofill <count> <data_table_name>
```

## Start the django project

1. Open a third terminal.
2. Navigate to the `crud_project` project directory using the command:
3. Run the project using the following command:

```bash
cd crud_project
python manage.py runserver
```
