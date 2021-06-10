"""
Examples of how you could implement custom callbacks for each provider.
"""
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail
from django.utils.translation import gettext_lazy as _

from ska.defaults import DEFAULT_AUTH_USER_PARAM

__all__ = (
    "client1_admins_create",
    "client1_admins_get",
    "client1_admins_info",
    "client1_admins_info_constance",
    "client1_admins_validate",
    "client1_power_users_create",
    "client1_power_users_get",
    "client1_power_users_info",
    "client1_power_users_validate",
    "Client1Create",
    "Client1Get",
    "Client1Info",
    "Client1Validate",
)


class BaseClientAction(object):
    @staticmethod
    def _send_email(group_name, user, request, signed_request_data):
        """Custom callback for power users."""
        # Sending email to users
        email = signed_request_data.get("email", "")
        first_name = signed_request_data.get("first_name", "")
        if email:
            send_mail(
                _("Welcome {}!").format(group_name),
                _(
                    """Dear {0}\nYou have been added to the group power """
                    """users.\nBest regards"""
                ).format(first_name),
                "from@example.com",
                [email],
                fail_silently=True,
            )


# **************************************************************************
# ************************* USER_VALIDATE_CALLBACK *************************
# **************************************************************************


class Client1Validate(BaseClientAction):
    """Client 1 `USER_VALIDATE_CALLBACK` callbacks."""

    @staticmethod
    def power_users(request, signed_request_data):
        """Custom callback for power users."""
        return Client1Validate._send_email(
            _("power users"), None, request, signed_request_data
        )

    @staticmethod
    def admins(request, signed_request_data):
        """Custom callback for admins."""
        request_data = request.GET.dict()
        email = signed_request_data.get("email", "")
        auth_user = request_data.get(DEFAULT_AUTH_USER_PARAM)
        if auth_user == "forbidden_username":
            raise PermissionDenied("Access denied (username forbidden).")

        if email == "forbidden@example.com":
            raise PermissionDenied("Access denied (email forbidden).")

        return Client1Validate._send_email(
            _("validate::admins"), None, request, signed_request_data
        )


client1_power_users_validate = Client1Validate.power_users
client1_admins_validate = Client1Validate.admins

# **************************************************************************
# ************************* USER_CREATE_CALLBACK ***************************
# **************************************************************************


class Client1Create(BaseClientAction):
    """Client 1 `USER_CREATE_CALLBACK` callbacks."""

    @staticmethod
    def power_users(user, request, signed_request_data):
        """Custom callback for power users."""
        user.is_staff = True
        user.save()
        return Client1Create._send_email(
            _("power users"), user, request, signed_request_data
        )

    @staticmethod
    def admins(user, request, signed_request_data):
        """Custom callback for admins."""
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return Client1Create._send_email(
            _("create::admins"), user, request, signed_request_data
        )


client1_power_users_create = Client1Create.power_users
client1_admins_create = Client1Create.admins


# **************************************************************************
# *************************** USER_GET_CALLBACK ****************************
# **************************************************************************


class Client1Get(BaseClientAction):
    """Client 1 `USER_GET_CALLBACK` callbacks."""

    @staticmethod
    def power_users(user, request, signed_request_data):
        """Custom callback for power users."""
        return Client1Get._send_email(
            _("get::power users"), user, request, signed_request_data
        )

    @staticmethod
    def admins(user, request, signed_request_data):
        """Custom callback for admins."""
        return Client1Get._send_email(
            _("get::admins"), user, request, signed_request_data
        )


client1_power_users_get = Client1Get.power_users
client1_admins_get = Client1Get.admins

# **************************************************************************
# *************************** USER_INFO_CALLBACK ***************************
# **************************************************************************


class Client1Info(BaseClientAction):
    """Client 1 `USER_INFO_CALLBACK` callbacks."""

    @staticmethod
    def power_users(user, request, signed_request_data):
        """Custom callback for power users."""
        return Client1Info._send_email(
            _("info::power users"), user, request, signed_request_data
        )

    @staticmethod
    def admins(user, request, signed_request_data):
        """Custom callback for admins."""
        return Client1Info._send_email(
            _("info::admins"), user, request, signed_request_data
        )

    @staticmethod
    def admins_constance(user, request, signed_request_data):
        """Custom callback for admins."""
        print("Constance callback!")
        return Client1Info._send_email(
            _("info::constance::admins"), user, request, signed_request_data
        )


client1_power_users_info = Client1Info.power_users
client1_admins_info = Client1Info.admins
client1_admins_info_constance = Client1Info.admins_constance
