from .base import *  # noqa

EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"
SKA_DB_STORE_SIGNATURES = True
SKA_DB_PERFORM_SIGNATURE_CHECK = True
