from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    # Now add the ERROR code to the response.
    if response is not None:
        response.data['error'] = '1'
        try:
            response.data['error_msg'] = response.data['detail']
            del response.data['detail']  # 删除detail字段
            return response
        except KeyError:
            return response
