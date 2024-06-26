from server.settings.components import config

CORS_ALLOWED_ORIGINS = [
    'http://localhost:8080',
    'http://127.0.0.1:9000',
    'http://localhost:3000',
]
CORS_ALLOW_ALL_ORIGINS = config(
    'CORS_ALLOW_ALL_ORIGINS',
    cast=bool,
    default=True,
)
CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
]
CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]
CORS_PREFLIGHT_MAX_AGE = config(
    'CORS_PREFLIGHT_MAX_AGE',
    cast=int,
    default=86400,
)
CORS_ALLOW_CREDENTIALS = config(
    'CORS_ALLOW_CREDENTIALS',
    cast=bool,
    default=False,
)
