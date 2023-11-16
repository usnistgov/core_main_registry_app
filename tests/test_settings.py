""" Tests Settings
"""

SECRET_KEY = "fake-key"

INSTALLED_APPS = [
    # Django apps
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.sites",
    # Extra apps
    "defender",
    "menu",
    # Local apps
    "core_main_app",
    "core_main_registry_app",
    "core_parser_app",
    "tests",
]

MIDDLEWARE = (
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
)

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": ["templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                # Needed by any curator app
                "core_main_app.utils.custom_context_processors.domain_context_processor",
                "django.template.context_processors.i18n",
            ],
        },
    },
]

# IN-MEMORY TEST DATABASE
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
        "USER": "",
        "PASSWORD": "",
        "HOST": "",
        "PORT": "",
    },
}


PASSWORD_HASHERS = ("django.contrib.auth.hashers.UnsaltedMD5PasswordHasher",)

USE_TZ = True
CELERYBEAT_SCHEDULER = "django_celery_beat.schedulers:DatabaseScheduler"

MONGODB_INDEXING = False
MONGODB_ASYNC_SAVE = False
ENABLE_SAML2_SSO_AUTH = False
ALLOW_MULTIPLE_SCHEMAS = True

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
CUSTOM_NAME = "NMRR"
ROOT_URLCONF = "tests.urls"
