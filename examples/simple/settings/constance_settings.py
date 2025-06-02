
from .base import *  # noqa

INSTALLED_APPS += (  # noqa
    "constance",
    "constance.backends.database",  # Only if ``DatabaseBackend`` is used
    "django_json_widget",
    "ska.contrib.django.ska.integration.constance_integration",
)

# CONSTANCE_BACKEND = 'constance.backends.redisd.RedisBackend'
CONSTANCE_BACKEND = "constance.backends.database.DatabaseBackend"

CONSTANCE_REDIS_CONNECTION = {
    "host": "localhost",
    "port": 6379,
    "db": 0,
}

CONSTANCE_ADDITIONAL_FIELDS = {
    "JSONField_config": [
        "jsonfield2_addons.forms.JSONField",
        # 'jsonfield.forms.JSONField',
        {
            # 'widget': 'django.forms.Textarea',
            "widget": "django_json_widget.widgets.JSONEditorWidget",
        },
    ],
}

AUTHENTICATION_BACKENDS = (
    "ska.contrib.django.ska.backends.constance_backend.SkaAuthenticationConstanceBackend",  # noqa
    "django.contrib.auth.backends.ModelBackend",
)

ROOT_URLCONF = "constance_urls"
