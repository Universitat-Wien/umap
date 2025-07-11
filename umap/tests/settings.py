import os

from umap.settings.base import *  # pylint: disable=W0614,W0401

SECRET_KEY = "justfortests"
DEFAULT_FROM_EMAIL = "test@test.org"
EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"
STORAGES["staticfiles"]["BACKEND"] = (
    "django.contrib.staticfiles.storage.StaticFilesStorage"
)

if os.environ.get("GITHUB_ACTIONS", False) == "true":
    DATABASES = {
        "default": {
            "ENGINE": "django.contrib.gis.db.backends.postgis",
            "NAME": "postgres",
            "USER": "postgres",
            "HOST": "postgis",
            "PORT": 5432,
            "PASSWORD": "postgres",
        }
    }

PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.MD5PasswordHasher",
]


WEBSOCKET_ENABLED = True
WEBSOCKET_BACK_PORT = "8010"
WEBSOCKET_FRONT_URI = "ws://localhost:8010"
