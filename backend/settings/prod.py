from .base import *

DEBUG = False

ALLOWED_HOSTS = [
    "vemacars-backend.deploy.tz",
]

CORS_ALLOWED_ORIGINS = [
    "https://vemacars.deploy.tz",
]

CSRF_TRUSTED_ORIGINS = [
    "https://vemacars.deploy.tz",
]
