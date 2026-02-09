from .base import *


DEBUG = True

ALLOWED_HOSTS = [
    "127.0.0.1", 
    "localhost",
    ".ngrok-free.dev"]

CORS_ALLOW_ALL_ORIGINS = True

CSRF_TRUSTED_ORIGINS = [
    "https://*.ngrok-free.dev",
]