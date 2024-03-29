from typing import Optional

from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.settings import api_settings

__author__ = "Artur Barseghyan"
__copyright__ = "2013-2023 Artur Barseghyan"
__license__ = "GPL-2.0-only OR LGPL-2.1-or-later"
__all__ = ("ObtainJSONWebTokenView",)

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
jwt_decode_handler = api_settings.JWT_DECODE_HANDLER
jwt_get_username_from_payload = api_settings.JWT_PAYLOAD_GET_USERNAME_HANDLER


class ObtainJSONWebTokenView(APIView):
    """Obtain a JSON web token."""

    def get(self, request: Request, format: Optional[str] = None) -> Response:
        user = authenticate(request=request)

        if user is not None:
            if user.is_active:
                payload = jwt_payload_handler(user)
                data = {"token": jwt_encode_handler(payload)}
                return Response(data)
            else:
                raise AuthenticationFailed("User is not active")

        raise AuthenticationFailed("Authentication failed")
