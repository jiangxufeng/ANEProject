# -*- coding:utf-8 -*-
# author: jiangxf
# updated: 2018-07-03
from rest_framework.views import exception_handler
from rest_framework.exceptions import AuthenticationFailed, APIException
from django.utils.translation import ugettext_lazy as _


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    print(response.data)
    try:
        code = int(response.data['detail'][:5])
        detail = response.data['detail'][5:]
    except ValueError:
        code = 90001
        detail = response.data['detail']
    except KeyError:
        # 商家评价评分不在0-5之间
        if 'score' in response.data:
            code = 30008
            detail = response.data['score'][0]
            del response.data['score']
        # 手机号码格式不正确
        elif 'phone' in response.date:
            code = 20004
            detail = response.data['phone'][0]
            del response.data['phone']

    if response is not None:
        response.data['error'] = code
        try:
            response.data['error_msg'] = detail
            del response.data['detail']  # 删除detail字段
            return response
        except KeyError:
            return response


# 错误异常： detail前5位为错误码
# 用户名或密码错误
class WrongUsernameOrPwd(APIException):
    default_detail = _("20001Incorrect username or password.")
    status_code = 200


# token验证失败
class MyAuthenticationFailed(AuthenticationFailed):
    default_detail = _('20002Invalid token, Please login again.')


# 关注的用户为自己
class FollowAuthenticationFailed(APIException):
    default_detail = _("20005You can't follow yourself.It's invalid")
    status_code = 200


# 用户不存在
class FoundUserFailed(APIException):
    default_detail = _("20404Not found the user.")
    status_code = 404


# 服务器故障500
class ServerWrong(APIException):
    default_detail = _("90500Server wrong.")
    status_code = 500





