from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models


class User(AbstractUser):
    username = models.CharField(
        'Имя пользователя', db_index=True, max_length=150, unique=True,
        validators=[RegexValidator(
            regex=r'^[\w.@+-]+$',
            message='Недопустимый символ в имени пользователя'
        )]
    )
    email = models.EmailField('Электронная почта', db_index=True, unique=True)
    first_name = models.CharField('Имя', max_length=150, blank=True)
    last_name = models.CharField('Фамилия', max_length=150, blank=True)
    bio = models.TextField('О себе', blank=True)

    ADMIN = 'admin'
    MODERATOR = 'moderator'
    USER = 'user'

    USER_ROLES_CHOICES = [
        (ADMIN, 'Администратор'),
        (MODERATOR, 'Модератор'),
        (USER, 'Пользователь'),
    ]

    role = models.CharField(
        'Роль',
        max_length=9,
        choices=USER_ROLES_CHOICES,
        default='user'
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('id',)

    def __str__(self):
        return self.username

    @property
    def is_admin(self):
        return self.role == self.ADMIN

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    @property
    def is_user(self):
        return self.role == self.USER
