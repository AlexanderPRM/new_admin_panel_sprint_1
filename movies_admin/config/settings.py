import os
from pathlib import Path

from dotenv import load_dotenv
from split_settings.tools import include

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get("SECRET_KEY", default="NOT_SO_SECRET")

DEBUG = os.environ.get("DEBUG", default="False") == "True"

ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS").split(", ")

INTERNAL_IPS = ["127.0.0.1"]

include("components/installed_apps.py")

include("components/middlewares.py")

ROOT_URLCONF = "config.urls"

include("components/templates.py")

MEDIA_ROOT = BASE_DIR / "media"
MEDIA_URL = "/media/"

WSGI_APPLICATION = "config.wsgi.application"

LOCALE_PATHS = ["movies/locale"]

include("components/database.py")

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation."
        "UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation."
        "MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation."
        "CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation."
        "NumericPasswordValidator",
    },
]

LANGUAGE_CODE = "ru-RU"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = "/static/"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
