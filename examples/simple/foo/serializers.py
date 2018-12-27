from rest_framework import serializers

from .models import FooItem

__all__ = (
    'FooItemSerializer',
)


class FooItemSerializer(serializers.ModelSerializer):
    """FooItem model serializer."""

    class Meta(object):

        model = FooItem
        fields = (
            'title',
            'slug',
            'body',
        )
