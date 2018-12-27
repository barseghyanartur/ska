from rest_framework.viewsets import ModelViewSet

from ska.contrib.django.ska.integration.drf.permissions import (
    ProviderSignedRequestRequired
)

from .models import FooItem
from .serializers import FooItemSerializer

__all__ = (
    'FooItemViewSet',
)


class FooItemViewSet(ModelViewSet):
    """FooItem model viewset."""

    permission_classes = (ProviderSignedRequestRequired,)
    queryset = FooItem.objects.all()
    serializer_class = FooItemSerializer
