# Django settings for example project.
import os
import sys

from .core import PROJECT_DIR

DEBUG = False
DEBUG_TOOLBAR = False
TEMPLATE_DEBUG = DEBUG
DEV = False

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

DATABASES = {
    "default": {
        # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        "ENGINE": "django.db.backends.sqlite3",
        # Or path to database file if using sqlite3.
        "NAME": PROJECT_DIR(os.path.join("..", "..", "db", "example.db")),
        # The following settings are not used with sqlite3:
        "USER": "",
        "PASSWORD": "",
        # Empty for localhost through domain sockets or '127.0.0.1' for
        # localhost through TCP.
        "HOST": "",
        # Set to empty string for default.
        "PORT": "",
    }
}

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = []

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = "America/Chicago"

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = "en"

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
MEDIA_ROOT = PROJECT_DIR(os.path.join("..", "media"))

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = "/media/"

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
STATIC_ROOT = PROJECT_DIR(os.path.join("..", "..", "static"))

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = "/static/"

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    PROJECT_DIR(os.path.join("..", "..", "media", "static")),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    # 'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = "6sf18c*w971i8a-m^1coasrmur2k6+q5_kyn*)s@(*_dk5q3&r"


AUTHENTICATION_BACKENDS = (
    "ska.contrib.django.ska.backends.SkaAuthenticationBackend",
    "django.contrib.auth.backends.ModelBackend",
)

try:
    from .local_settings import DEBUG_TEMPLATE
except Exception:
    DEBUG_TEMPLATE = False

# ***************************************************************************

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        # 'APP_DIRS': True,
        "DIRS": [PROJECT_DIR(os.path.join("..", "templates"))],
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                # "context_processors.testing",  # Testing
            ],
            "loaders": [
                "django.template.loaders.filesystem.Loader",
                "django.template.loaders.app_directories.Loader",
                # 'django.template.loaders.eggs.Loader',
            ],
            "debug": DEBUG_TEMPLATE,
        },
    },
]

# ***************************************************************************

_MIDDLEWARE = (
    "django.middleware.common.CommonMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = "urls"

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = "wsgi.application"

INSTALLED_APPS = (
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Uncomment the next line to enable the admin:
    "django.contrib.admin",
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
    # For django-constance
    "constance",
    "constance.backends.database",  # Only if ``DatabaseBackend`` is used
    "django_json_widget",
    # For djangorestframework
    "rest_framework",
    "rest_framework_jwt",
    # ska, django-ska and example/testing app
    "ska.contrib.django.ska",
    "ska.contrib.django.ska.integration.constance_integration",
    "foo",  # Our example app
)

# ***************************************************************************
# ************************** ska config *************************************
# ***************************************************************************

# Global secret key
SKA_SECRET_KEY = "secret-key"
SKA_UNAUTHORISED_REQUEST_ERROR_TEMPLATE = "ska/401.html"
# Page to redirect to after successful login
SKA_REDIRECT_AFTER_LOGIN = "/foo/logged-in/"
# Store used signatures in database
SKA_DB_STORE_SIGNATURES = True
# Perform signature check
SKA_DB_PERFORM_SIGNATURE_CHECK = True
# List of additional secret keys per provider
SKA_PROVIDERS = {
    # Client 1, group users
    "client_1.users": {
        "SECRET_KEY": "client-1-users-secret-key",
    },
    # Client 1, group power_users
    "client_1.power_users": {
        "SECRET_KEY": "client-1-power-users-secret-key",
        "USER_CREATE_CALLBACK": "foo.ska_callbacks.client1_power_users_create",
    },
    # Client 1, group admins
    "client_1.admins": {
        "SECRET_KEY": "client-1-admins-secret-key",
        "USER_VALIDATE_CALLBACK": "foo.ska_callbacks.client1_admins_validate",
        "USER_CREATE_CALLBACK": "foo.ska_callbacks.client1_admins_create",
        "USER_GET_CALLBACK": "foo.ska_callbacks.client1_admins_get",
        "USER_INFO_CALLBACK": "foo.ska_callbacks.client1_admins_info",
        "REDIRECT_AFTER_LOGIN": "/admin/",
    },
}

# ***************************************************************************
# *********************** django-constance config ***************************
# ***************************************************************************
CONSTANCE_BACKEND = "constance.backends.database.DatabaseBackend"

CONSTANCE_ADDITIONAL_FIELDS = {
    "JSONField_config": [
        "jsonfield2_addons.forms.JSONField",
        {
            # 'widget': 'django.forms.Textarea',
            "widget": "django_json_widget.widgets.JSONEditorWidget",
        },
    ],
}

CONSTANCE_CONFIG = {
    "SKA_PROVIDERS": (
        {},  # The default value
        "JSON data",  # Help text in admin
        "JSONField_config",  # Field config
    ),
    "SKA_SECRET_KEY": (
        "",  # The default value
        "Global secret key",  # Help text in admin
    ),
}

# ***************************************************************************
# ************************ djangorestframework config ***********************
# ***************************************************************************
REST_FRAMEWORK = {
    # 'DEFAULT_PERMISSION_CLASSES': (
    #     'rest_framework.permissions.IsAuthenticated',
    # ),
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_jwt.authentication.JSONWebTokenAuthentication",
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.BasicAuthentication",
    ),
}

# ***************************************************************************
# ********************************* other config ****************************
# ***************************************************************************

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {
        "require_debug_false": {"()": "django.utils.log.RequireDebugFalse"}
    },
    "formatters": {
        "verbose": {
            "format": "%(levelname)s %(asctime)s [%(pathname)s:%(lineno)s] "
            "%(message)s"
        },
        "simple": {"format": "%(levelname)s %(message)s"},
    },
    "handlers": {
        "mail_admins": {
            "level": "ERROR",
            "filters": ["require_debug_false"],
            "class": "django.utils.log.AdminEmailHandler",
        },
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
        "django_log": {
            "level": "DEBUG",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": PROJECT_DIR("../../logs/django.log"),
            "maxBytes": 1048576,
            "backupCount": 99,
            "formatter": "verbose",
        },
        "ska_log": {
            "level": "DEBUG",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": PROJECT_DIR("../../logs/ska.log"),
            "maxBytes": 1048576,
            "backupCount": 99,
            "formatter": "verbose",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["django_log"],
            "level": "ERROR",
            "propagate": True,
        },
        "ska": {
            "handlers": ["console", "ska_log"],
            "level": "DEBUG",
            "propagate": True,
        },
    },
}


# Do not put any settings below this line
try:
    from .local_settings import *
except:
    pass

if DEBUG and DEBUG_TOOLBAR:
    # debug_toolbar
    _MIDDLEWARE += ("debug_toolbar.middleware.DebugToolbarMiddleware",)

    INSTALLED_APPS += ("debug_toolbar",)

    DEBUG_TOOLBAR_CONFIG = {
        "INTERCEPT_REDIRECTS": False,
    }


# Make the `ska` package available without installation.
if DEV:
    ska_source_path = os.environ.get("SKA_SOURCE_PATH", "src")
    # sys.path.insert(0, os.path.abspath('src'))
    sys.path.insert(0, os.path.abspath(ska_source_path))

MIDDLEWARE = _MIDDLEWARE
