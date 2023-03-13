from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from users.models import User

from .validators import year_validator


class Category(models.Model):
    name = models.CharField(max_length=256, verbose_name="Название категории")
    slug = models.SlugField(unique=True, max_length=50,
                            verbose_name="Слаг категории")

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=256, verbose_name="Название жанра")
    slug = models.SlugField(unique=True, max_length=50,
                            verbose_name="Слаг жанра")

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(max_length=256,
                            verbose_name="Название произведения")
    year = models.IntegerField(
        validators=[year_validator],
        verbose_name="Год выхода произведения"
    )
    genre = models.ManyToManyField(Genre,
                                   verbose_name="Жанр произведения")
    category = models.ForeignKey(Category,
                                 related_name='titles', blank=True, null=True,
                                 on_delete=models.CASCADE,
                                 verbose_name="Категория произведения")
    description = models.TextField(blank=True, null=True,
                                   verbose_name="Описание произведения")

    class Meta:
        ordering = ['id']
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class Review(models.Model):
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='reviews'
    )
    text = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews'
    )
    score = models.IntegerField(
        default=1,
        validators=[
            MaxValueValidator(10),
            MinValueValidator(1)
        ],
        error_messages={
            'Внимание': 'Возможно оценить по шкале от 1 до 10!'
        }
    )
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author', ],
                name='unique_review'
            )
        ]
        ordering = ('pub_date',)
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'


class Comment(models.Model):
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments',
        verbose_name="Комментарий к отзыву"
    )
    text = models.TextField(verbose_name="Текст комментария")
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments',
        verbose_name="Автор комментария"
    )
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
