__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__copyright__ = 'Copyright (c) 2013 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'
__all__ = ('purge_signature_data', 'get_secret_key', 'get_provider_data')

import datetime

from ska.defaults import DEFAULT_PROVIDER_PARAM
from ska.contrib.django.ska.models import Signature
from ska.contrib.django.ska.settings import PROVIDERS, SECRET_KEY

def purge_signature_data():
    """
    Purges old signature data (valid_until < now).
    """
    Signature._default_manager.filter(valid_until__lt=datetime.datetime.now()).delete()

def get_secret_key(data, default=SECRET_KEY):
    """
    Obtain the secret key from request data given. This happens by looking up the secret key
    by `provider` param from the request data in the dictionary of ``PROVIDERS`` defined in
    settings module. If not found, fall back to the ``default`` value given, which is by
    default the globally set secret key.

    :param dict data:
    :param string default: Secret key value to be used as default. By default, the globally set
        secret key is used.
    """
    provider = data.get(DEFAULT_PROVIDER_PARAM, None)
    if provider:
        provider_data = PROVIDERS.get(provider, None)
        if provider_data:
            return provider_data.get('SECRET_KEY', default)

    return default

def get_provider_data(data):
    """
    Obtain the secret key from request data given. This happens by looking up the secret key
    by `provider` param from the request data in the dictionary of ``PROVIDERS`` defined in
    settings module. If not found, fall back to the ``default`` value given, which is by
    default the globally set secret key.

    :param dict data:
    :param string default: Secret key value to be used as default. By default, the globally set
        secret key is used.
    """
    provider = data.get(DEFAULT_PROVIDER_PARAM, None)
    if provider:
        return PROVIDERS.get(provider, None)
    return {}
