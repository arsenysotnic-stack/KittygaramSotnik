from django.db import models
from django.contrib.auth import get_user_model
from cats.models import Cat

User = get_user_model()


class Clinic(models.Model):
    name = models.CharField('Название', max_length=200)
    address = models.CharField('Адрес', max_length=500, blank=True)
    phone = models.CharField('Телефон', max_length=50, blank=True)
    website = models.URLField('Сайт', blank=True)
    created_at = models.DateTimeField('Дата добавления', auto_now_add=True)

    class Meta:
        verbose_name = 'Клиника'
        verbose_name_plural = 'Клиники'
        ordering = ['name']

    def __str__(self):
        return self.name


class HealthRecord(models.Model):
    VISIT = 'visit'
    PROCEDURE = 'procedure'
    MEDICATION = 'medication'
    VACCINATION = 'vaccination'
    ANALYSIS = 'analysis'

    RECORD_TYPE_CHOICES = [
        (VISIT, 'Визит к врачу'),
        (PROCEDURE, 'Процедура'),
        (MEDICATION, 'Лекарство'),
        (VACCINATION, 'Вакцинация'),
        (ANALYSIS, 'Анализы'),
    ]

    cat = models.ForeignKey(
        Cat,
        on_delete=models.CASCADE,
        related_name='health_records',
        verbose_name='Кот'
    )
    record_type = models.CharField(
        'Тип записи',
        max_length=20,
        choices=RECORD_TYPE_CHOICES
    )
    title = models.CharField('Название', max_length=200)
    description = models.TextField('Описание', blank=True)
    date = models.DateField('Дата')
    next_date = models.DateField('Дата следующей процедуры', null=True, blank=True)
    clinic = models.ForeignKey(
        Clinic,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='records',
        verbose_name='Клиника'
    )
    doctor_name = models.CharField('Врач', max_length=200, blank=True)
    is_completed = models.BooleanField('Выполнено', default=False)
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='health_records',
        verbose_name='Создал'
    )
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)

    class Meta:
        verbose_name = 'Запись здоровья'
        verbose_name_plural = 'Записи здоровья'
        ordering = ['-date']

    def __str__(self):
        return f'{self.cat.name} — {self.get_record_type_display()} ({self.date})'
