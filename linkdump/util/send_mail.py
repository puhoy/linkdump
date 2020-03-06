from flask_mail import Message

from linkdump import dramatiq
from linkdump import mail


@dramatiq.actor(max_retries=3)
def _send_mail_task(**kwargs: str):
    mail.send(Message(**kwargs))


