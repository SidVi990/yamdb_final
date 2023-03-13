from django.conf import settings
from django.core.mail import send_mail


def send_email(email, confirmation_code, username):
    send_mail(
        'Код подтверждения',
        'Ваш код подтверждения для регистрации на сайте YaMDb.com.\n'
        'Он понадобится вам для аутентификации.\n'
        f'Код подтверждения: {confirmation_code}\n'
        f'Имя пользователя: {username}',
        settings.EMAIL_YAMDB,
        [email],
        fail_silently=False,
    )
