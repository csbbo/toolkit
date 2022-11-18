from django.core.cache import cache
from django.utils import timezone
from rest_framework.authtoken.models import Token
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.exceptions import ValidationError
from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from account.filters import FeedbackFilter, UserFilter
from account.models import User
from account.serializers import FeedbackSerializer, UserSerializer
from common.utils import date_utils, str_utils


@api_view(["POST"])
@permission_classes([])
@authentication_classes([])
def get_captcha(request: Request) -> Response:
    phone_number = request.data.get("phone_number")
    captcha = str_utils.get_random_lower_str()
    # 发送验证码到
    ...
    cache.set(phone_number, captcha, timeout=60)
    return Response()


@api_view(["POST"])
@permission_classes([])
@authentication_classes([])
def login(request: Request) -> Response:
    phone_number = request.data.get("phone_number")
    captcha = request.data.get("captcha")
    # if cache.get(phone_number) != captcha:
    if "0000" != captcha:
        raise ValidationError("验证码错误!")

    username = str_utils.get_random_lower_str()
    user, created = User.objects.get_or_create(
        phone_number=phone_number, defaults={"username": username}
    )
    user.last_login = timezone.now()
    user.save(update_fields=["last_login"])

    Token.objects.filter(user=user).delete()
    token = Token.objects.create(user=user)

    resp_data = {
        "token": token.key,
        "name": user.name,
        "username": user.username,
        "phone_number": user.phone_number,
        "signature": user.signature,
        "create_time": date_utils.datetime_format(user.create_time),
        "update_time": date_utils.datetime_format(user.update_time),
        "last_login_time": date_utils.datetime_format(user.last_login),
    }
    return Response(data=resp_data)


@api_view(["POST"])
def logout(request: Request) -> Response:
    user = request.user
    Token.objects.filter(user=user).delete()
    return Response()


class UserViewSet(RetrieveModelMixin, ListModelMixin, GenericViewSet):
    serializer_class = UserSerializer
    queryset = serializer_class.Meta.model.objects.all()
    filterset_class = UserFilter


@api_view(["GET"])
def profile(request: Request) -> Response:
    user = request.user
    data = {
        "id": user.id,
        "name": user.name,
        "username": user.username,
        "phone_number": user.phone_number,
        "signature": user.signature,
        "create_time": date_utils.datetime_format(user.create_time),
        "update_time": date_utils.datetime_format(user.update_time),
        "last_login": date_utils.datetime_format(user.last_login)
        if user.last_login
        else None,
    }
    return Response(data)


class FeedbackViewSet(CreateModelMixin, ListModelMixin, GenericViewSet):
    serializer_class = FeedbackSerializer
    queryset = serializer_class.Meta.model.objects.all()
    filterset_class = FeedbackFilter
