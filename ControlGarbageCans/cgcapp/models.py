from django.db import models


class GeoBase(models.Model):
    """База для хранения координат и адресов."""

    lat = models.FloatField(
        verbose_name="Широта")
    lon = models.FloatField(
        verbose_name="Долгота")
    address = models.CharField(
        max_length=512,
        verbose_name="Адрес")

    def __str__(self):
        return f'{self.lat}, {self.lon}'

    class Meta:
        verbose_name = "ГеоБаза"
        verbose_name_plural = "ГеоБаза"
