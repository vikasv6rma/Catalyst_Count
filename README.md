
# Catalyst Count

This project is related to upload the csv file with 1GB of data and Details are been fetched related using query building and showing the User Details.


## Run Locally (Python)

Create Virtual Environment:

```bash
  python -m venv venv
```

Activate Virtual Environment in Windows:

```bash
  venv/script/activate
```

Install the given requirements.txt cmd:

```bash
  pip install -r requirements.txt
```

Start the server

```bash
  python manage.py runserver
```

Run the server locally in browser:

```bash
  http://127.0.0.1:8000/
```


## Features
Import given "catalyst.sql" into MySQL Database

- Upload Data (Uploading "companies_sorted.csv" File)
- Query Builder
- Users

NOTE: Column names of table (Table Name:'catalyst_count') in 'catalyst.sql' database should be exactly same as columns names provided in "companies_sorted.csv" file.


## Endpoints

To run the "uploadData" locally:

```bash
  http://127.0.0.1:8000/
```


To run the "queryBuilder" locally:

```bash
  http://127.0.0.1:8000/queryBuilder
```


To run the "users" locally:

```bash
  http://127.0.0.1:8000/users
```



