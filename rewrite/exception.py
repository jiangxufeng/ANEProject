# -*- coding:utf-8 -*-
# author: jiangxf
# updated: 2018-07-03
from rest_framework.views import exception_handler
from rest_framework.exceptions import AuthenticationFailed, APIException
from django.utils.translation import ugettext_lazy as _


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    try:
        temp_dict = eval(str(response.data))
        keys = list(temp_dict.keys())
        temp_values = []
        for i in keys:
            temp_values.append(temp_dict[i][0])
    except AttributeError:
        code = 90002
        detail = "asdadas"
    try:
        code = int(response.data['detail'][:5])
        detail = response.data['detail'][5:]
    except ValueError:
        code = 90001
        detail = response.data['detail']
    except KeyError:
        if "This field may not be blank." in set(temp_values):
            code = 70001
            detail = 'Invalid params'
            response.data.clear()
        # 商家评价评分不在0-5之间
        elif 'score' in response.data:
            code = 30008
            detail = response.data['score'][0]
            del response.data['score']
        # 手机号码格式不正确
        elif 'phone' in response.data:
            code = 20004
            detail = response.data['phone'][0]
            del response.data['phone']
        elif 'title' in response.data:
            code = 30008
            detail = response.data['title'][0]
            del response.data['title']
        elif 'location' in response.data:
            code = 30009
            detail = response.data['location'][0]
            del response.data['location']
        else:
            code = 90003
            detail = 'werwrwe'
    except:
        code = 90004
        detail = 'werwrwe'

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
    default_detail = _("20005You can't follow yourself.It's invalid.")
    status_code = 200


# 用户不存在
class FoundUserFailed(APIException):
    default_detail = _("20404Not found the user.")
    status_code = 404


# 密码未修改
class PasswordIsSame(APIException):
    default_detail = _("20006The new password is same to the old password.")
    status_code = 400


# 服务器故障500
class ServerWrong(APIException):
    default_detail = _("90500Server wrong.")
    status_code = 500


# 图书不存在
class FoundBookFailed(APIException):
    default_detail = _("30001Not found the book.")
    status_code = 404


# 商家不存在
class FoundShopFailed(APIException):
    default_detail = _("30002Not found the shop.")
    status_code = 404


# 评论不存在
class FoundCommentFailed(APIException):
    default_detail = _("30003Not found the comment.")
    status_code = 404


# 流浪猫狗信息不存在
class FoundAnimalFailed(APIException):
    default_detail = _("30004Not found the animal message.")
    status_code = 404


# 图书交换对象为自己
class ExchangeIsYourself(APIException):
    default_detail = _("30005You can't exchange the book with yourself.")
    status_code = 400


# 参数错误
class ParamsInvalid(APIException):
    default_detail = _("70001Invalid params.")
    status_code = 400


# 缺少关键参数
class MissingParameter(APIException):
    default_detail = _("70002Missing key parameter.")
    status_code = 400


# 帖子不存在
class FoundPostFailed(APIException):
    default_detail = _("40001Not found the post.")
    status_code = 404


# 该用户已点赞
class UserLikedPost(APIException):
    default_detail = _("40007The user has liked the post.")
    status_code = 400


# 点赞不存在
class FoundLikeFailed(APIException):
    default_detail = _("40008Not found the like of the post.")
    status_code = 404


# 取消的赞owner与当前用户不一致
class UserIsNotTheOwnerOfLike(APIException):
    default_detail = _("40009The user is not the owner of like.")
    status_code = 400


# 消息通知不存在
class FoundNoticeFailed(APIException):
    default_detail = _("50001Not found the notice.")
    status_code = 404


