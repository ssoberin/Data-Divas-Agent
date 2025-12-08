from django.db import models


class Worker(models.Model):

    name = models.CharField(
        verbose_name="ФИО",
        max_length=255,
        null=False,
        blank=False,
    )
    phone = models.CharField(
        verbose_name="Телефон",
        max_length=15,
        null=False,
        blank=False,
    )
    notes = models.TextField(
        verbose_name="Комментарий",
        blank=True,
    )

    class Meta:
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'


class Depo(models.Model):

    name = models.CharField(
        verbose_name="Наименование депо",
        max_length=255,
        null=False,
        blank=False,
    )
    address = models.CharField(
        verbose_name="Адрес",
        max_length=255,
        null=False,
        blank=False,
    )
    depot_lat = models.FloatField(
        verbose_name="Широта",
        null=True,
        blank=True,
    )
    depot_lon = models.FloatField(
        verbose_name="Долгота",
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = 'Депо'
        verbose_name_plural = 'Депо'
