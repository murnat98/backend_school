# Backend school

### Prerequisities

* [PostgreSQL](https://www.postgresql.org/download/) - PostgreSQL 10.10+
* [Python](https://www.python.org/downloads/) - Python 3.6.8+
* [Pip](https://pip.pypa.io/en/stable/installing/) - Pip 9.0.1+

### Installation

#### Install the requirements

Run following instructions

```
cd /path/to/project/
python3.6 -m venv env
source /env/bin/activate
pip install -r requirements.txt
```

#### Create config.ini

* Create database and add the information of database in the config.ini file
* Create configuration file *config.ini* in the project root for database config with the following content

```
[DEFAULT]

secret_key = `secret key for django`

[DATABASE]

name =
user =
password =
host =
port =
```

#### Run the tests

```
./manage.py test
```

#### Run the project

Run the following commands in the project root

```
./manage.py migrate
gunicorn -b 0.0.0.0:8080 backend_school.wsgi
```
