"""Examples of how you could implement custom callbacks for each provider."""

from django.core.mail import send_mail
from django.utils.translation import ugettext_lazy as _


class Client1Create(object):
    """Client 1 callbacks."""

    @staticmethod
    def _send_email(group_name, user, request, signed_request_data):
        """Custom callback for power users."""
        # Sending email to users
        email = signed_request_data.get('email', '')
        first_name = signed_request_data.get('first_name', '')
        if email:
            send_mail(
                _('Welcome!'),
                _("""Dear {0}\nYou have been added to the group power """
                  """users.\nBest regards""").format(first_name),
                'from@example.com',
                [email],
                fail_silently=True
            )

    @staticmethod
    def power_users(user, request, signed_request_data):
        """Custom callback for power users."""
        user.is_staff = True
        user.save()
        return Client1Create._send_email(
            _('power users'),
            user,
            request,
            signed_request_data
        )

    @staticmethod
    def admins(user, request, signed_request_data):
        """Custom callback for admins."""
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return Client1Create._send_email(
            _('admins'),
            user,
            request,
            signed_request_data
        )


client1_power_users_create = Client1Create.power_users
client1_admins_create = Client1Create.admins
