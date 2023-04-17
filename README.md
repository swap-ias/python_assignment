# Description
This project include features like:

- fetch stock data from provider alpha vantage with a batch and insert into databsae
- API to get stock info
- API to average price of a period

## Libraries
- python 3.8
- sqlalchemy as ORM framework
- alembic as migration tool
- FastAPI as web framework
- MySQL 8.0 as database

## How to Setup
### Prepare environment
1. (Optional)install python 3.8, recommended using virtual environment.
2. install Docker desktop

### Start application
1. get your API key from alpha vantage website, create a *.env* file from *.env.template* file, place it in root folder. Then paste API key to ALPHA_VANTAGE_API_KEY.
2. run the command ```make up``` or ```docker-compose up```. It will both start app server and mysql.
3. migrate local database with command ```make migrate-local```

You can confirm the app is started with accessing: http://localhost:5001/api/docs

Note: In MacOS Ventura, the port 5000 is occupied, so the app is bind with 5001 port.
### Insert financial data
You need to run ```python get_raw_data.py``` in docker environment.
1. execute ```make enter-server```
2. execute ```python get_raw_data.py```

### Access API with OpenAPI
Access http://localhost:5001/api/docs

or using curl:
```agsl
curl -X 'GET' \
  'http://localhost:5001/api/financial_data?symbol=IBM&limit=5&page=1' \
  -H 'accept: application/json'

curl -X 'GET' \
  'http://localhost:5001/api/financial_data?start_date=2023-04-01&end_date=2023-04-10&symbol=IBM&limit=5&page=1' \
  -H 'accept: application/json'

curl -X 'GET' \
  'http://localhost:5001/api/statistics?start_date=2023-03-10&end_date=2023-04-10&symbol=IBM' \
  -H 'accept: application/json'
```


# Q&A

### 1. Reasons of using ORM framework SQLAlchemy, and migration tool Alembic
Comparing with using plain SQL, using ORM frameworks has advantages to avoid SQL string concatenating, which could be buggy and reason of SQL Injection.
Also the framework can help to optimize SQL in certain cases. Alembic allows better version management of migration scripts and other features.


### 2. How to save API Key securely
Basically we should avoid having the API Key hard coded in source code.

In local environment, it is saved in ```.env``` file, which is ignored by Git. The API Key will be loaded as environment variable.

In dev and prd environment, we can save the API key in secured storage, for example AWS Secrets Manager. And when the server docker container started, we inject the API key from the secrets storage into environment variable.
