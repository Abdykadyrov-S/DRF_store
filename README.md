* Создание и активация виртуальной среды:
```shell
python -m venv venv
```
(Windows)
```shell
venv\Scripts\activate.bat
```
(Mac/Linux)
```shell
source venv/bin/activate
```

* Создаем файл ".env" с полями:
```python
SECRET_KEY=c$$pl9@x(=w9x*3!z4dajkyx0(ne%^%1&yrv9(x#8t#v&-ssn3
DB_USER=postgres
DB_NAME=postgres
DB_USER_PASSWORD=123456
DB_HOST=postgres-db
DB_PORT=5432
```



* Делаем развертываение через Docker командой:
```shell
docker-compose up --build
```