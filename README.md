# Instructions

These instructions have been tested on Ubuntu 18.04 using Python 3.6 from bash

## Create virtual environment

```
$ python3 -m venv .venv
$ . .venv/bin/activate
$ pip install -r requirements.txt
```

### Start development server in console

```
(.venv) $ FLASK_APP=./src/acme/bookr/api.py flask run --host=0.0.0.0
```

### Start development server in Docker

```
(.venv) $ docker build -t bookr:latest . && docker run -d -p 5000:5000 --name=bookr-flask bookr
```

### Run tests

```
(.venv) $ pytest src/acme/bookr/tests
```

API tests work against port 5000 and will run against the development server running either
from the console or in Docker.
