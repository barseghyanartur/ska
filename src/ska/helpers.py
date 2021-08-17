from datetime import datetime, timedelta
from importlib import import_module
import json
import time
from typing import Callable, Dict, List, Tuple, Union, Optional
from urllib.parse import quote

from .defaults import SIGNATURE_LIFETIME

__author__ = "Artur Barseghyan <artur.barseghyan@gmail.com>"
__copyright__ = "2013-2021 Artur Barseghyan"
__license__ = "GPL 2.0/LGPL 2.1"
__all__ = (
    "default_value_dumper",
    "dict_keys",
    "dict_to_ordered_list",
    "extract_signed_data",
    "get_callback_func",
    "javascript_value_dumper",
    "make_valid_until",
    "sorted_urlencode",
    "default_quoter",
    "javascript_quoter",
)


def get_callback_func(
    func: Union[str, Callable], fail_silently: bool = True
) -> Optional[Callable]:
    """Take a string and try to extract a function from it.

    :param func: If `callable` is given, return as is. If `str`
        is given, try to extract the function from the string given and
        return.
    :param fail_silently:
    :return: Returns `callable` if what's extracted is callable or
        None otherwise.
    """
    if callable(func):
        return func
    elif isinstance(func, str):
        try:
            module_path, class_name = func.rsplit(".", 1)
        except ValueError as err:
            if not fail_silently:
                raise ImportError(f"{func} doesn't look like a module path")
            return None

        module = import_module(module_path)

        try:
            return getattr(module, class_name)
        except AttributeError as err:
            if not fail_silently:
                raise ImportError(
                    f'Module "{module_path}" does not define a "{class_name}" '
                    f"attribute/class"
                )


def dict_keys(
    data: Dict[str, Union[bytes, str, float, int]], return_string: bool = False
) -> Union[str, List[str]]:
    """Get sorted keys from dictionary given.

    If ``return_string`` argument is set to True, returns keys joined by
    commas.

    :param data:
    :param return_string:
    :return:
    """
    keys = list(data.keys())
    keys.sort()

    if return_string:
        return ",".join(keys)

    return keys


def dict_to_ordered_list(
    data: Dict[str, Union[bytes, str, float, int]]
) -> List[Tuple[str, Union[bytes, str, float, int]]]:
    """Get extra as ordered list.

    :param dict data:
    :return:
    """
    items = list(data.items())
    items.sort()
    return items


def dict_to_ordered_dict(obj):
    if isinstance(obj, dict):
        obj = dict(sorted(obj.items()))
        for k, v in obj.items():
            if isinstance(v, dict) or isinstance(v, list):
                obj[k] = dict_to_ordered_dict(v)

    if isinstance(obj, list):
        for i, v in enumerate(obj):
            if isinstance(v, dict) or isinstance(v, list):
                obj[i] = dict_to_ordered_dict(v)
        # obj = sorted(obj, key=lambda x: json.dumps(x))

    return obj


def default_value_dumper(value):
    return value


def javascript_value_dumper(value):
    if isinstance(value, (int, float, str)):
        return value
    # elif isinstance(value, UUID):
    #     return str(value)
    else:
        return json.dumps(value, separators=(",", ":"))


def default_quoter(value):
    return quote(value)


def javascript_quoter(value):
    return quote(value, safe="~()*!.'")


def sorted_urlencode(
    data: Dict[str, Union[bytes, str, float, int]],
    quoted: bool = True,
    value_dumper: Optional[Callable] = default_value_dumper,
    quoter: Optional[Callable] = default_quoter,
) -> str:
    """Similar to built-in ``urlencode``, but always puts data in a sorted
    constant way that stays the same between various python versions.

    :param data:
    :param quoted:
    :param value_dumper:
    :param quoter:
    :return:
    """
    if not value_dumper:
        value_dumper = default_value_dumper

    if not quoter:
        quoter = default_quoter

    # _sorted = [f"{k}={value_dumper(v)}" for k, v in dict_to_ordered_list(data)]
    _sorted = [
        f"{k}={value_dumper(v)}" for k, v in dict_to_ordered_dict(data).items()
    ]
    res = "&".join(_sorted)
    if quoted:
        res = quoter(res)
    return res


def extract_signed_data(
    data: Dict[str, Union[bytes, str, float, int]], extra: List[str]
) -> Dict[str, Union[bytes, str, float, int]]:
    """Filters out non-white-listed items from the ``extra`` dictionary given.

    :param data:
    :param extra:
    :return:
    """
    extracted_extra = dict(data)
    for key, value in data.items():
        if key not in extra:
            extracted_extra.pop(key)

    return extracted_extra


def make_valid_until(lifetime: int = SIGNATURE_LIFETIME) -> float:
    """Make valid until.

    :param lifetime:
    :return:
    """
    return time.mktime(
        (datetime.now() + timedelta(seconds=lifetime)).timetuple()
    )
