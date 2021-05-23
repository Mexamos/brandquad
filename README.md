# Test task from Brandquad

> `.env` file was specially left in the git for checking test task

## Description

Service for parsing and saving logs

## Installation

Install dependencies:

```bash
poetry install
```

Run database:

```bash
docker-compose up
```

## API

Custom django-admin command:

```bash
python ./brandquad/manage.py parse_logs http://www.almhuette-raith.at/apache-log/access.log 10
```

Arguments:
 - URL for get logs
 - Optional argument, number of log rows for save

## Tests

```bash
python ./brandquad/manage.py test parse_logs
```
