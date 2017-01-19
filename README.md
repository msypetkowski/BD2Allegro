# BD2 Internet Shop

Project made for BD2 classes.

## SYNOPSIS



To start server:
```sh
$ ./manage.py runserver
```

After changes in model run(these changes will become a new migration):
```sh
$ ./manage.py makemigrations ShopApp
```

To create database tables:
```sh
$ ./manage.py migrate
```

To create new superuser (interactive command):
```sh
$ ./manage.py createsuperuser
```


## DEBUG

To run shell:
```sh
$ ./manage.py shell
```

Print SQL data of given mogration:
```sh
$ ./manage.py sqlmigrate ShopApp XXXX
```

When server is running type in web browser:
to see homepage:
```url
localhost:8000
```
to login as site administrator:
```url
localhost:8000/admin
```
