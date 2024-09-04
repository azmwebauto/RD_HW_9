cd into ./scraper and create .env from example
~~~
REDIS_PASSWORD = password
REDIS_USER = default
REDIS_HOST = 127.0.0.1
REDIS_PORT = 6378

URL_TO_SERVICE = http://127.0.0.1:8080

SCRAPING_SCHEDULE_IN_MINUTES = 7
MAX_POSTING_LIMIT = 2000
OPENED_FILES_SEMAPHORE_AMOUNT = 1500
~~~

similar with web_app
~~~
POSTGRES_USER = postgres
POSTGRES_PASSWORD = password
POSTGRES_DB = app
POSTGRES_HOST = 127.0.0.1
POSTGRES_PORT = 5432

HOST = 127.0.0.1
PORT = 8080

MAX_CVE_ITEMS = 3000
~~~

To run services just use docker-compose
~~~bash
cd ./web_app
docker-compose up -d --build
~~~
~~~bash
cd ./scraper
docker-compose up -d --build
~~~

OR use ./start.sh bash file
~~~bash
chmod 777 ./start.sh
./start.sh
~~~