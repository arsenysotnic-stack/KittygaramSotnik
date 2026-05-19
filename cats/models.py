from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Achievement(models.Model):
    name = models.CharField('Название', max_length=64, unique=True)

    class Meta:
        verbose_name = 'Достижение'
        verbose_name_plural = 'Достижения'

    def __str__(self):
        return self.name


class Cat(models.Model):
    name = models.CharField('Имя', max_length=32)
    color = models.CharField('Цвет', max_length=32)
    birth_year = models.PositiveIntegerField('Год рождения')
    image = models.ImageField(
        'Фото',
        upload_to='cats/images/',
        blank=True,
        null=True
    )
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='cats',
        verbose_name='Владелец'
    )
    achievements = models.ManyToManyField(
        Achievement,
        through='AchievementCat',
        verbose_name='Достижения',
        blank=True
    )
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)

    class Meta:
        verbose_name = 'Котик'
        verbose_name_plural = 'Котики'
        ordering = ['-created_at']

    def __str__(self):
        return self.name


class AchievementCat(models.Model):
    cat = models.ForeignKey(Cat, on_delete=models.CASCADE)
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE)
    awarded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('cat', 'achievement')