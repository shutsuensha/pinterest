### Next steps

### Web server
uvicorn app.main:app --reload

### Postgre
psql -U evalshine -d pinterest

### Migrations
alembic revision --autogenerate -m "init"
alembic upgrade head