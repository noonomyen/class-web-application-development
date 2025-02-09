## Deployment

### Setup

```sh
# root repo and activated venv
pip install -r requirements.txt
```

Set .env file with

```env
IS_SERVERLESS=false
SECRET_KEY=<Random>
SQLALCHEMY_DATABASE_URI=<Your Database>
```

#### MySQL

```sh
python api/blueprints/football_clubs --init-db "mysql://USER:PASS@USER.mysql.pythonanywhere-services.com/DATABASE"
```

#### SQLite

```sh
mkdir -p tmp
python api/blueprints/football_clubs --init-db "sqlite:///tmp/data.db"
```
