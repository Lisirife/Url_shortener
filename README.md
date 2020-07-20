
# Url shortener

This is website for shortening URLs. Given long URL it produces shortened
version of it.

## Getting Started

This tool uses docker-compose.

Firstly copy and modify settings.

```
$ cp .env.example .env
```

Then to start the application simply run:

```
$ docker-compose up
```

## Running the tests

To run the automated tests for this system:

```
$ docker exec -it url_shortener_app_1 bash
$ python3 manage.py test
```

## Authors

* **Aiste Jureviciene** 
