from celery import Celery
from app.celery_tasks.mail import mail, create_message
from asgiref.sync import async_to_sync
from app.config import settings

c_app = Celery()

c_app.conf.update(
    broker_url=settings.REDIS_URL,
    result_backend=settings.REDIS_URL, 
    broker_connection_retry_on_startup=True
)


@c_app.task()
def send_email(recipients: list[str], subject: str, body: str):

    message = create_message(recipients=recipients, subject=subject, body=body)

    async_to_sync(mail.send_message)(message)