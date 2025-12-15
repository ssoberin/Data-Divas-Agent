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

    class Meta:
        verbose_name = 'Депо'
        verbose_name_plural = 'Депо'


class ObjectTypeEnum:

    WORKER = 'Сотрудник'
    DEPO = "Депо"

    values = {
        WORKER: Worker,
        DEPO: Depo,
    }



class Coordinates(models.Model):
    object_type = models.IntegerField(
        verbose_name="Тип объекта",
        null=False,
        blank=False,
        # choices=ObjectTypeEnum.values,
    )
    object_id = models.IntegerField(
        verbose_name="ID объекта",
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

    def __str__(self):
        return f"Координата объекта с типом {ObjectTypeEnum.values[self.object_type]} ID {self.object_id}"

    class Meta:
        verbose_name = 'Координата'
        verbose_name_plural = 'Координаты объектов'


