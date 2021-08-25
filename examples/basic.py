from pprint import pprint
import requests
from ska.shortcuts import signature_to_dict, validate_signed_request_data
from ska.helpers import javascript_quoter, javascript_value_dumper

SECRET_KEY = "haha1234"
URL = "https://webhook.site/44181b26-a8a6-419e-b34e-f28009a871eb"
PAYLOAD = {"first": "ffsddDDddddddddddddd", "second": "ffffff", "number": 123}

# Signing
signature = signature_to_dict(
    auth_user="user",
    secret_key=SECRET_KEY,
    extra=PAYLOAD,
    value_dumper=javascript_value_dumper,
    quoter=javascript_quoter,
)
# signature["signature"] = signature["signature"].decode()
pprint(signature)
print()

response = requests.post(URL, json=signature)
pprint(response.__dict__)
print()

# Validation
DATA = {
  "signature": "3imDv6x3mWDnrvgNbllpZ0bj3kA=",
  "auth_user": "user",
  "valid_until": "1629934247.0",
  "extra": "first,number,second",
  "first": "ffsddDDddddddddddddd",
  "second": "ffffff",
  "number": 123
}

result = validate_signed_request_data(
    DATA,
    secret_key=SECRET_KEY,
    value_dumper=javascript_value_dumper,
    quoter=javascript_quoter,
)
pprint(result)
print()
