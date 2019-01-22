import datetime
from importlib import import_module
import time

from six.moves.urllib.parse import quote

from .defaults import SIGNATURE_LIFETIME

__title__ = 'ska.helpers'
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__copyright__ = '2013-2019 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'
__all__ = (
    'get_callback_func',
    'dict_keys',
    'dict_to_ordered_list',
    'sorted_urlencode',
    'extract_signed_data',
    'make_valid_until',
)


def get_callback_func(func, fail_silently=True):
    """Take a string and try to extract a function from it.

    :param mixed func: If `callable` is given, return as is. If `string`
        is given, try to extract the function from the string given and
        return.
    :param fail_silently: bool
    :return callable: Returns `callable` if what's extracted is callable or
        None otherwise.
    """
    if callable(func):
        return func
    elif isinstance(func, str):
        try:
            module_path, class_name = func.rsplit('.', 1)
        except ValueError as err:
            if not fail_silently:
                raise ImportError(
                    "%s doesn't look like a module path" % func)

        module = import_module(module_path)

        try:
            return getattr(module, class_name)
        except AttributeError as err:
            if not fail_silently:
                raise ImportError(
                    'Module "%s" does not define a "%s" attribute/class' % (
                        module_path, class_name)
                    )


def dict_keys(data, return_string=False):
    """Get sorted keys from dictionary given.

    If ``return_string`` argument is set to True, returns keys joined by
    commas.

    :param dict data:
    :param bool return_string:
    """
    keys = list(data.keys())
    keys.sort()

    if return_string:
        return ','.join(keys)

    return keys


def dict_to_ordered_list(data):
    """Get extra as ordered list.

    Actually, I'm not sure whether I should or should not be using
    ``OrderedDict`` here.

    :param dict data:
    :return list:
    """
    items = list(data.items())
    items.sort()
    return items


def sorted_urlencode(data, quoted=True):
    """Similar to built-in ``urlencode``, but always puts data in a sorted
    constant way that stays the same between various python versions.
    """
    _sorted = ["{0}={1}".format(k, v) for k, v in dict_to_ordered_list(data)]
    res = '&'.join(_sorted)
    if quoted:
        res = quote(res)
    return res


def extract_signed_data(data, extra):
    """Filters out non-white-listed items from the ``extra`` dictionary given.

    :param dict data:
    :param list extra:
    :return dict:
    """
    extracted_extra = dict(data)
    for key, value in data.items():
        if key not in extra:
            extracted_extra.pop(key)

    return extracted_extra


def make_valid_until(lifetime=SIGNATURE_LIFETIME):
    """Make valid until.

    :param int lifetime:
    :return datetime.datetime"""
    return time.mktime(
        (
            datetime.datetime.now() +
            datetime.timedelta(seconds=lifetime)
        ).timetuple()
    )
