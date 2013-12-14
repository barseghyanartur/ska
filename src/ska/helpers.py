__title__ = 'ska.helpers'
__author__ = 'Artur Barseghyan'
__copyright__ = 'Copyright (c) 2013 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'
__all__ = ('get_callback_func',)

def get_callback_func(function):
    """
    Takes a string and tries to extract a function from it.

    :param mixed function: If `callable` is given, return as is. If `string` is given, try to
        extract the function from the string given and return.
    :return callable: Returns `callable` if what's extracted is callable or None otherwise.
    """
    if callable(function):
        return function
    elif isinstance(function, str):
        path = function.split('.')
        try:
            exec('from %s import %s as %s' % ('.'.join(path[0:-1]), path[-1], 'func'))
            if callable(func):
                return func
        except:
            return None
