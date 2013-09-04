__title__ = 'ska.generate_signed_url'
__version__ = '0.4'
__build__ = 0x000004
__author__ = 'Artur Barseghyan'
__all__ = ('main',)

import argparse

from ska import sign_url

def main():
    """
    Prints signed URL to console.

    :example:

    $ python src/ska/generate_signature.py -au user -sk test
    """
    parser = argparse.ArgumentParser(description="""
    Generates signed URL.
    """)

    parser.add_argument("-au", "--auth-user", dest="auth_user", type=str, help="`auth_user` value", \
                        metavar="AUTH_USER")
    parser.add_argument("-sk", "--secret-key", dest="secret_key", type=str, help="`secret_key` value", \
                        metavar="SECRET_KEY")
    parser.add_argument("-vu", "--valid-until", dest="valid_until", type=float, help="`valid_until` value", \
                        metavar="VALID_UNTIL")
    parser.add_argument("-l", "--lifetime", dest="lifetime", type=int, help="`lifetime` value", metavar="LIFETIME")
    parser.add_argument("-u", "--url", dest="url", type=str, help="URL to sign", metavar="URL")
    parser.add_argument("-sp", "--signature-param", dest="signature_param", type=str, \
                        help="GET param holding the `signature` value", metavar="SIGNATURE_PARAM")
    parser.add_argument("-aup", "--auth-user-param", dest="auth_user_param", type=str, \
                        help="GET param holding the `auth_user` value", metavar="AUTH_USER_PARAM")
    parser.add_argument("-vup", "--valid-until-param", dest="valid_until_param", type=str, \
                        help="GET param holding the `auth_user` value", metavar="VALID_UNTIL_PARAM")

    args = parser.parse_args()

    kwargs = {}

    if args.auth_user:
        kwargs.update({'auth_user': args.auth_user})

    if args.secret_key:
        kwargs.update({'secret_key': args.secret_key})

    if args.valid_until:
        kwargs.update({'valid_until': args.valid_until})

    if args.lifetime:
        kwargs.update({'lifetime': args.lifetime})

    if args.url:
        kwargs.update({'url': args.url})

    if args.signature_param:
        kwargs.update({'signature_param': args.signature_param})

    if args.auth_user_param:
        kwargs.update({'auth_user_param': args.auth_user_param})

    if args.valid_until_param:
        kwargs.update({'valid_until_param': args.valid_until_param})

    try:
        signed_url = sign_url(**kwargs)
        print signed_url
    except Exception, e:
        print e

if __name__ == "__main__":
    main()
