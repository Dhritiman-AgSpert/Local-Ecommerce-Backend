# Install postgresql and create db in Windows
- download .exe from https://www.enterprisedb.com/downloads/postgres-postgresql-downloads
- double click the .exe to install the application. follow the instructions in the installation wizard. Note the installation directory, password and port (keep it 5432, recommended).
- To add PostgreSQL to the path:
    - Open the System Properties control panel and select the Advanced tab. Alternatively, run` SystemPropertiesAdvanced.exe.`
    - Select Environment Variables to open the environment variables editor.
    - Select the Path variable under System variables, and select Edit.
    - Add the path that you specified as the installation directory during installation, appended with `\bin`. By default, the value is `c:\program files\postgresql\15\bin`, where 15 is the version of PostgreSQL that you installed.
- to create a db, open a terminal and run `psql -U postgres`
    - enter the password
    - run `CREATE DATABASE agvefrdb;` to create db
    - run `\q` to quit

# Installation the backend application in Windows:
- create a folder say `dev`
- enter the folder `cd dev`
- create python virtual environment `python3.10.11.exe -m venv venv`
- activate the venv `.\venv\Scripts\activate`
- install poetry `pip install poetry`
- clone the repo ```git clone https://github.com/AgVefr/AgVefrBackend.git```
- enter the created directory `cd AgVefrBackend`
- install the application `poetry install`
- create .env file in the current folder with the following content:
```
ADMIN_EMAIL = any@email.com
DATABASE_URL = postgresql://postgres:<password>@localhost:5432/agvefrdb
secret_key = <use `openssl rand -hex 32` to generate secret key>
```
- create migrations using `alembic revision --autogenerate -m "migration <serial number>"`
- apply migrations using `alembic upgrade head`
- start the app `uvicorn src.main:app --reload --host 0.0.0.0 --port 8000`