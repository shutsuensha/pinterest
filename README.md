## TO DO

users can add comments to pins
users can likes pins and comments

## Features
user registration
user verification via email
user authentication via JWT and Cookies
user logout
user reset password via email
user avatars
users create pins with media - images/videos
users add tags to pin
users get all pins
users get detail pin and related pins by tags


## Web server
uvicorn app.app:app --reload

## Postgres
sudo systemctl start postgresql
sudo systemctl status postgresql
psql -U evalshine -d pinterest

## Alembic
alembic revision --autogenerate -m "init"
alembic upgrade head

## Redis
sudo systemctl start redis-server
sudo systemctl status redis-server

## Celery
celery -A app.celery_tasks.celery.c_app worker --loglevel=INFO