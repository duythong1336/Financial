from rest_framework.views import exception_handler
from rest_framework.response import Response
from shared.utils import response_data
from rest_framework import status
def custom_exception_handler(exc, context):
    # exceptions box
    handlers = {
        'ValidationError': _handle_validation_error,
        'Http404': _handle_http404_error,
        'NotFound': _handle_not_found_error,
        'PermissionDenied': _handle_generic_error,
        'NotAuthenticated': _handle_authentication_error,
        'AuthenticationFailed': _handle_authentication_failed, # For wrong password or email when login
        'InvalidUserError': _handle_authentication_failed,
        # 'AttributeError': _handle_generic_error,
        'TokenError': _handle_generic_error,
        'InvalidTokenError': _handle_generic_error,
        # 'ValueError': _handle_generic_error,
        'DoesNotExist': _handle_http404_error,
    }
    # print(type(exc))
    response = exception_handler(exc, context)
    if response is not None:
        response.data = response_data(
            success = False,
            statusCode = response.status_code,
            message = exc.default_detail if hasattr(exc, 'default_detail') else '',
            data = exc.detail if hasattr(exc, 'detail') else []
        )
    
    exception_class = exc.__class__.__name__
    # print(exception_class)
    # For in the box exceptions
    if exception_class in handlers:
        return handlers[exception_class](exc, context, response)
    return response

def _handle_value_error(exc, context, response):
    
    response.data = response_data(
        success = False,
        statusCode = 400,
        message = 'Please login to process',
        data = dict(exc)
    )
    
    return response
 
def _handle_authentication_error(exc, context, response):
    
    response.data = response_data(
        success = False,
        statusCode = response.status_code,
        message = 'Please login to process',
        data = exc.detail
    )
    
    return response

def _handle_validation_error(exc, context, response):
    
    response.data = response_data(
        success = False,
        statusCode = response.status_code,
        message = exc.default_detail,
        data = exc.detail
    )
    
    return response

def _handle_authentication_failed(exc, context, response):
    response.data = response_data(
        success = False,
        statusCode = response.status_code,
        # message = 'Wrong email or password. Please try again',
        message = exc.detail,
    )
    
    return response

def _handle_generic_error(exc, context, response):

    # print(context)
    if response is None:
        response = Response(status = status.HTTP_500_INTERNAL_SERVER_ERROR)
    response.data = response_data(
        success = False,
        statusCode = response.status_code if response is not None else status.HTTP_500_INTERNAL_SERVER_ERROR,
        message = exc.default_detail,
        data = exc.detail
    )
    
    return response

def _handle_http404_error(exc, context, response):
    
    if response is None:
        response = Response(status = status.HTTP_404_NOT_FOUND)
    
    response.data = response_data(
        success = False,
        statusCode = status.HTTP_404_NOT_FOUND,
        message = exc.detail
    )   

    return response

def _handle_not_found_error(exc, context, response):
    response.data = response_data(
        success = False,
        statusCode = 404,
        message = exc.detail,
        data = []
    )

    return response