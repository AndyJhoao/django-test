# API Exchanges

## Setup

The first thing to do is to clone the repository:

```sh
$ git clone https://github.com/AndyJhoao/django-test.git
$ cd api-exchange
```

Create a virtual environment to install dependencies in and activate it:

```sh
$ python -m venv venv
$ source venv/bin/activate
```

Then install the dependencies:

```sh
(venv)$ pip install -r requirements.txt
```
Note the `(venv)` in front of the prompt. This indicates that this terminal
session operates in a virtual environment set up by `virtualenv2`.

Create `.env` file and add the variables

Example:
```sh
TOKEN_API =a6aa97395e24a90e3244b48a67e2b3d1ffb78b760804948ec388ae1ae6f9f8e0
URL_API =https://www.banxico.org.mx/SieAPIRest/service/v1/series/SF63528
```

Once `pip` has finished downloading the dependencies:
```sh
v(env)$ cd api-exchange
(venv)$ python manage.py runserver
```
And navigate to diferrent end points MXN TO USD = `http://127.0.0.1:8000/mxn2usd/`.
And USD TO MXN = `http://127.0.0.1:8000/usd2mxn/`

Access to admin console = `http://127.0.0.1:8000/admin`

create a user with group `corredor` because users without this group doesn't access to endpoints.

SUPERUSER : admin
PASSWORD : 123456

`DONT ACCESS`
User 1 without `corredor`: 
Username : `test2`
Password : `prueba123`

`ACCESS`
User 2 with `corredor`: 
Username : `test`
Password : `prueba123`

Cheers.

