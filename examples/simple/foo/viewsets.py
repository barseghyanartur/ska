from rest_framework.viewsets import ModelViewSet

from ska.contrib.django.ska.integration.drf.permissions import (
    ProviderSignedRequestRequired,
    SignedRequestRequired,
)
from ska.contrib.django.ska.integration.drf.permissions.constance_permissions import (
    ConstanceProviderSignedRequestRequired,
    ConstanceSignedRequestRequired,
)

from .models import (
    FooItemConstanceProviderSignedRequestRequired,
    FooItemConstanceSignedRequestRequired,
    FooItemProviderSignedRequestRequired,
    FooItemSignedRequestRequired,
)
from .serializers import FooItemSerializer

__all__ = (
    "FooItemConstanceSignedRequestRequiredViewSet",
    "FooItemConstanceProviderSignedRequestRequiredViewSet",
    "FooItemProviderSignedRequestRequiredViewSet",
    "FooItemSignedRequestRequiredViewSet",
)


class BaseFooItemViewSet(ModelViewSet):
    """FooItem model base ViewSet."""

    lookup_field = "id"
    serializer_class = FooItemSerializer


class FooItemSignedRequestRequiredViewSet(BaseFooItemViewSet):
    """FooItem model ViewSet protected with `SignedRequestRequired`."""

    queryset = FooItemSignedRequestRequired.objects.all()
    permission_classes = (SignedRequestRequired,)


class FooItemProviderSignedRequestRequiredViewSet(BaseFooItemViewSet):
    """FooItem model ViewSet protected with `ProviderSignedRequestRequired`."""

    queryset = FooItemProviderSignedRequestRequired.objects.all()
    permission_classes = (ProviderSignedRequestRequired,)


class FooItemConstanceSignedRequestRequiredViewSet(BaseFooItemViewSet):
    """FooItem model ViewSet protected with
    `ConstanceSignedRequestRequired`.
    """

    queryset = FooItemConstanceSignedRequestRequired.objects.all()
    permission_classes = (ConstanceSignedRequestRequired,)


class FooItemConstanceProviderSignedRequestRequiredViewSet(BaseFooItemViewSet):
    """FooItem model ViewSet protected with
    `ConstanceProviderSignedRequestRequired`.
    """

    queryset = FooItemConstanceProviderSignedRequestRequired.objects.all()
    permission_classes = (ConstanceProviderSignedRequestRequired,)
