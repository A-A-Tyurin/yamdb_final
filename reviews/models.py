from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from .validators import year_validator

User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=256, verbose_name='name')
    slug = models.SlugField(unique=True, max_length=50, verbose_name='slug')

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=256, verbose_name='name')
    slug = models.SlugField(unique=True, max_length=50, verbose_name='slug')

    class Meta:
        verbose_name = 'Genre'
        verbose_name_plural = 'Genries'

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.TextField(verbose_name='name')
    year = models.IntegerField(validators=[year_validator],
                               verbose_name='year')
    description = models.CharField(max_length=256,
                                   verbose_name='description')
    genre = models.ManyToManyField(Genre, through='TitleGenre',
                                   verbose_name='genre')
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE,
        related_name='titles', null=True, blank=True, verbose_name='category')

    class Meta:
        verbose_name = 'Title'
        verbose_name_plural = 'Titles'

    def __str__(self):
        return self.name


class TitleGenre(models.Model):
    title = models.ForeignKey(Title,
                              on_delete=models.CASCADE,
                              verbose_name='title')
    genre = models.ForeignKey(Genre,
                              on_delete=models.CASCADE,
                              verbose_name='genre')

    class Meta:
        verbose_name = 'TitleGenre'
        verbose_name_plural = 'TitleGenries'

    def __str__(self):
        return f'{self.title} {self.genre}'


class Review(models.Model):
    text = models.TextField()
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews')
    score = models.PositiveSmallIntegerField(
        'оценка',
        validators=[
            MaxValueValidator(10, message='оценка не может быть больше 10'),
            MinValueValidator(1, message='оценка не может быть меньше 1')
        ])
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='reviews')

    class Meta:
        ordering = ['-pub_date']
        constraints = [models.UniqueConstraint(fields=['title', 'author'],
                                               name='unique_review')]

    def __str__(self):
        return self.text


class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True)
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments')

    class Meta:
        ordering = ['-pub_date']
