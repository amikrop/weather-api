from django.conf import settings

from weatherapi.settings import env

DEFAULTS = {
    "ELEVATION_MIN": -500,
    "ELEVATION_MAX": 9000,
    "TEMPERATURE_MIN": -90,
    "TEMPERATURE_MAX": 60,
    "WIND_SPEED_MAX": 100,
    "RAINFALL_MAX": 500,
}

SETTINGS = {key: env.float(f"WEATHER_{key}", value) for key, value in DEFAULTS.items()}


class Settings:
    def __getattr__(self, name):
        user_settings = getattr(settings, "WEATHER", {})
        try:
            return user_settings[name]
        except KeyError:
            return SETTINGS[name]


app_settings = Settings()
