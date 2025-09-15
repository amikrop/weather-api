import django.core.validators
import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
        migrations.CreateModel(
            name="Station",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(blank=True, max_length=100, verbose_name="Name"),
                ),
                (
                    "latitude",
                    models.FloatField(
                        blank=True,
                        null=True,
                        validators=[
                            django.core.validators.MinValueValidator(-90),
                            django.core.validators.MaxValueValidator(90),
                        ],
                        verbose_name="Latitude",
                    ),
                ),
                (
                    "longitude",
                    models.FloatField(
                        blank=True,
                        null=True,
                        validators=[
                            django.core.validators.MinValueValidator(-180),
                            django.core.validators.MaxValueValidator(180),
                        ],
                        verbose_name="Longitude",
                    ),
                ),
                (
                    "elevation",
                    models.FloatField(
                        blank=True, null=True, verbose_name="Elevation (m)"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Measurement",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "datetime",
                    models.DateTimeField(
                        default=django.utils.timezone.now, verbose_name="Date and time"
                    ),
                ),
                (
                    "temperature",
                    models.FloatField(
                        blank=True, null=True, verbose_name="Temperature (C)"
                    ),
                ),
                (
                    "humidity",
                    models.FloatField(
                        blank=True,
                        null=True,
                        validators=[
                            django.core.validators.MinValueValidator(0),
                            django.core.validators.MaxValueValidator(100),
                        ],
                        verbose_name="Humidity (%)",
                    ),
                ),
                (
                    "wind_speed",
                    models.FloatField(
                        blank=True, null=True, verbose_name="Wind speed (m/s)"
                    ),
                ),
                (
                    "wind_direction",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("N", "North"),
                            ("NE", "North-East"),
                            ("E", "East"),
                            ("SE", "South-East"),
                            ("S", "South"),
                            ("SW", "South-West"),
                            ("W", "West"),
                            ("NW", "North-West"),
                        ],
                        max_length=2,
                        verbose_name="Wind direction (compass point)",
                    ),
                ),
                (
                    "rainfall",
                    models.FloatField(
                        blank=True, null=True, verbose_name="Rainfall (mm)"
                    ),
                ),
                (
                    "station",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="weather.station",
                    ),
                ),
            ],
            options={
                "ordering": ["-datetime"],
                "unique_together": {("datetime", "station")},
            },
        ),
    ]
