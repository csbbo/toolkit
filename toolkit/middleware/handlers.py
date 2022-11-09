import logging
import traceback

from django.http import Http404
from rest_framework import status
from rest_framework.exceptions import (
    APIException,
    AuthenticationFailed,
    MethodNotAllowed,
    NotAcceptable,
    NotAuthenticated,
    NotFound,
    ParseError,
    PermissionDenied,
    Throttled,
    ValidationError,
)
from rest_framework.response import Response

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def exception_handler(exc: Exception, context: dict) -> Response:
    """
    https://q1mi.github.io/Django-REST-framework-documentation/api-guide/exceptions_zh/
    """

    logger.info(f"request error: {exc} \ntraceback: {traceback.format_exc()}")

    # REST framework定义的异常，主动抛出异常也应该被包含在下面的类型中
    if isinstance(exc, APIException):
        msg = str(exc)

        if isinstance(exc, ValidationError):
            return Response(
                status=status.HTTP_200_OK, data={"err": "invalid", "msg": msg}
            )
        elif isinstance(exc, PermissionDenied):
            return Response(
                status=status.HTTP_200_OK,
                data={"err": "permission-denied", "msg": "访问受限"},
            )
        elif isinstance(exc, NotAuthenticated):
            return Response(
                status=status.HTTP_200_OK, data={"err": "login-required", "msg": "需要登录"}
            )
        elif isinstance(exc, ParseError):
            return Response(
                status=status.HTTP_200_OK, data={"err": "parse-error", "msg": "解析失败"}
            )
        elif isinstance(exc, NotFound):
            return Response(
                status=status.HTTP_200_OK, data={"err": "not-found", "msg": "目标不存在"}
            )
        elif isinstance(exc, MethodNotAllowed):
            return Response(
                status=status.HTTP_200_OK,
                data={"err": "method-not-allowed", "msg": "请求方式不支持"},
            )
        elif isinstance(exc, NotAcceptable):
            return Response(
                status=status.HTTP_200_OK,
                data={"err": "not0acceptable", "msg": "数据格式不支持"},
            )
        elif isinstance(exc, Throttled):
            return Response(
                status=status.HTTP_200_OK, data={"err": "throttled", "msg": "超过限流次数"}
            )
        elif isinstance(exc, AuthenticationFailed):
            return Response(
                status=status.HTTP_200_OK,
                data={"err": "authentication-failed", "msg": "认证失败"},
            )

    if isinstance(exc, Http404):
        return Response(
            status=status.HTTP_200_OK, data={"err": "http-404", "msg": "对象不存在或无访问权限"}
        )

    return Response(
        status=status.HTTP_200_OK, data={"err": "server-error", "msg": "服务器错误!"}
    )
