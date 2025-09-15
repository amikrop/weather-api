from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class Station(models.Model):
    name = models.CharField(_("Name"), max_length=100, blank=True)
    latitude = models.FloatField(
        _("Latitude"),
        null=True,
        blank=True,
        validators=[MinValueValidator(-90), MaxValueValidator(90)],
    )
    longitude = models.FloatField(
        _("Longitude"),
        null=True,
        blank=True,
        validators=[MinValueValidator(-180), MaxValueValidator(180)],
    )
    elevation = models.FloatField(_("Elevation (m)"), null=True, blank=True)


class Measurement(models.Model):
    class WindDirection(models.TextChoices):
        N = "N", _("North")
        NE = "NE", _("North-East")
        E = "E", _("East")
        SE = "SE", _("South-East")
        S = "S", _("South")
        SW = "SW", _("South-West")
        W = "W", _("West")
        NW = "NW", _("North-West")

    datetime = models.DateTimeField(_("Date and time"), default=timezone.now)
    temperature = models.FloatField(_("Temperature (C)"), null=True, blank=True)
    humidity = models.FloatField(
        _("Humidity (%)"),
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )
    wind_speed = models.FloatField(_("Wind speed (m/s)"), null=True, blank=True)
    wind_direction = models.CharField(
        _("Wind direction (compass point)"),
        max_length=2,
        choices=WindDirection.choices,
        blank=True,
    )
    rainfall = models.FloatField(_("Rainfall (mm)"), null=True, blank=True)
    station = models.ForeignKey(Station, on_delete=models.CASCADE)

    class Meta:
        unique_together = ["datetime", "station"]
        ordering = ["-datetime"]
