from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import APIException, ErrorDetail
from rest_framework import status
from rest_framework.utils.serializer_helpers import ReturnDict, ReturnList
from django.utils.encoding import force_str

def _get_error_details(data, default_code=None):
    """
    Descend into a nested data structure, forcing any
    lazy translation strings or strings into `ErrorDetail`.
    """
    if isinstance(data, (list, tuple)):
        ret = [
            _get_error_details(item, default_code) for item in data
        ]
        if isinstance(data, ReturnList):
            return ReturnList(ret, serializer=data.serializer)
        return ret
    elif isinstance(data, dict):
        ret = {
            key: _get_error_details(value, default_code)
            for key, value in data.items()
        }
        if isinstance(data, ReturnDict):
            return ReturnDict(ret, serializer=data.serializer)
        return ret

    text = force_str(data)
    code = getattr(data, 'code', default_code)
    return ErrorDetail(text, code)

class InvalidUserError(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = _('Wrong email or password')
    default_code = 'invalid_user_error'
    
    
class InvalidTokenError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _('Token is invalid or expired')
    default_code = 'invalid_token_error'
    

class CustomValidationError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _('Invalid input.')
    default_code = 'invalid'

    def __init__(self, detail=None, code=None):
        if detail is None:
            detail = self.default_detail
        if code is None:
            code = self.default_code

        # For validation failures, we may collect many errors together,
        # so the details should always be coerced to a list if not already.
        if isinstance(detail, tuple):
            detail = list(detail)
        elif not isinstance(detail, dict) and not isinstance(detail, list):
            detail = [detail]

        self.detail = _get_error_details(detail, code)