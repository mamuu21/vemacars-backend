from .base import *

DEBUG = False

ALLOWED_HOSTS = [
    "vemacars-backend.deploy.tz",
    ".deploy.tz",          # 👈 VERY important (wildcard subdomains)
    "localhost",
    "127.0.0.1",
]

CORS_ALLOWED_ORIGINS = [
    "https://vemacars.deploy.tz",
]

CSRF_TRUSTED_ORIGINS = [
    "https://vemacars.deploy.tz",
]
