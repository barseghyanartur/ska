# Think about allowing auth_user_param point to a value from a nested structure

Consider the following payload:

```json
{
   "company":{
      "name":"Royal Lafleur",
      "website":"http://google.com"
   },
   "user":{
      "first_name":"Yinthe",
      "last_name":"van Dagsburg",
      "email":"mhelmerhorst@erhout.com"
   },
   "shipping_address":{
      "street":"Ivyweg",
      "house_number":"8",
      "city":"Schore",
      "postal_code":"8374IE",
      "country":"NL"
   },
   "billing_address":{
      "street":"Femkeboulevard",
      "house_number":"7",
      "city":"Hallum",
      "postal_code":"5594TA",
      "country":"NL"
   },
   "amount":1277179,
   "currency":"EUR"
}
```

Then something like this should be possible:

```python
signature_to_dict(
    auth_user=payload["user"]["email"],
    secret_key=SECRET_KEY,
    extra=payload,
    auth_user_param="user.email",
    nested_separator=".",
    # nested_separator_param=DEFAULT_NESTED_SEPARATOR_PARAM,
)
```

If ``nested_separator`` is given, but ``nested_separator_param`` not, we 
should fall back to the default (``DEFAULT_NESTED_SEPARATOR_PARAM``). 

If ``nested_separator`` is given, both ``nested_separator`` and 
``nested_separator_param`` shall be hashed too.

Think about the best separator (might be the dot).

We will need to supply a `nested_separator` and `nested_separator_param`
along too.

What it will do, it will include the 
