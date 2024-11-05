## TO DO


## Features
- user registration
- user verification via email
- user authentication via JWT and Cookies
- user logout
- user reset password via email
- user avatars
- users create pins with media - images/videos
- users add tags to pin
- users get all pins
- users get detail pin and related pins by tags
- users can view profiles with pins created by user
- users can add comments to pin
- users can add image to comment
- users can reply to comments


## Redis
sudo systemctl start redis-server
sudo systemctl status redis-server

## Celery
celery -A app.celery_tasks.celery.c_app worker --loglevel=INFO


## Postgres
sudo systemctl start postgresql
sudo systemctl status postgresql
psql -U evalshine -d pinterest


## Alembic
alembic revision --autogenerate -m "init"
alembic upgrade head


## Web server
uvicorn app.app:app --reload