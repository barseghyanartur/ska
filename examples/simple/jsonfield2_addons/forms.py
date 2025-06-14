"""
Taken from https://github.com/rpkilby/jsonfield2/blob/master/jsonfield/forms.py
"""

import json

from django.forms import ValidationError, fields
from django.utils.translation import gettext_lazy as _


class JSONFieldMixin(object):
    def __init__(self, *args, **kwargs):
        self.load_kwargs = kwargs.pop("load_kwargs", {})
        super(JSONFieldMixin, self).__init__(*args, **kwargs)

    def to_python(self, value):
        if isinstance(value, str) and value:
            try:
                return json.loads(value, **self.load_kwargs)
            except ValueError:
                try:
                    value = value.replace("'", '"')
                    return json.loads(value, **self.load_kwargs)
                except ValueError as err:
                    raise ValidationError(_("Enter valid JSON.")) from err
        return value

    def clean(self, value):
        if not value and not self.required:
            return None

        # Trap cleaning errors & bubble them up as JSON errors
        try:
            return super(JSONFieldMixin, self).clean(value)
        except TypeError as err:
            raise ValidationError(_("Enter valid JSON.")) from err


class JSONField(JSONFieldMixin, fields.CharField):
    pass
