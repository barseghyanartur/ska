import json
from .base import *

INSTALLED_APPS += (
    "constance",
    "constance.backends.database",  # Only if ``DatabaseBackend`` is used
    "django_json_widget",
    "ska.contrib.django.ska.integration.constance_integration",
)

# CONSTANCE_CONFIG = {
#     'SKA_PROVIDERS': (
#         "",  # The default value
#         'JSON data',  # Help text in admin
#         'JSONField_config',  # Field config
#     )
# }

print(
    json.dumps(
        {
            # Client 1, group users
            "client_1.users": {
                "SECRET_KEY": "client-1-users-secret-key",
            },
            # Client 1, group power_users
            "client_1.power_users": {
                "SECRET_KEY": "client-1-power-users-secret-key",
                "USER_CREATE_CALLBACK": "foo.ska_callbacks."
                "client1_power_users_create",
            },
            # Client 1, group admins
            "client_1.admins": {
                "SECRET_KEY": "client-1-admins-secret-key",
                "USER_CREATE_CALLBACK": "foo.ska_callbacks.client1_admins_create",
                "USER_GET_CALLBACK": "foo.ska_callbacks.client1_admins_get",
                "USER_INFO_CALLBACK": "foo.ska_callbacks."
                "client1_admins_info_constance",
                "REDIRECT_AFTER_LOGIN": "/admin/",
            },
        }
    ),
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
    "ska.contrib.django.ska.backends.constance_backend.SkaAuthenticationConstanceBackend",
    "django.contrib.auth.backends.ModelBackend",
)

ROOT_URLCONF = "constance_urls"
