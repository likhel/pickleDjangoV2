# user/exceptions.py

from rest_framework.exceptions import APIException
from django.utils.translation import gettext_lazy as _

class AccountDisabledException(APIException):
    status_code = 400
    default_detail = _('Account is disabled.')
    default_code = 'account_disabled'

class AccountNotRegisteredException(APIException):
    status_code = 400
    default_detail = _('Account is not registered.')
    default_code = 'account_not_registered'

class InvalidCredentialsException(APIException):
    status_code = 400
    default_detail = _('Invalid credentials.')
    default_code = 'invalid_credentials'

# Add other custom exceptions if needed
