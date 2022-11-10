import logging
from typing import List

from django.http import HttpResponse
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.permissions import BasePermission
from rest_framework.request import Request
from rest_framework.viewsets import GenericViewSet

from common.utils import xml_utils
from stock.utils import get_stock_market_info
from wechat.utils import check_signature, get_resp_content

logger = logging.getLogger(__name__)


class WxViewSet(GenericViewSet):
    permission_classes: List[BasePermission] = []

    def check_token(self, request: Request) -> HttpResponse:
        """
        https://developers.weixin.qq.com/doc/offiaccount/Basic_Information/Access_Overview.html
        需要正确响应来自微信服务器的请求微信服务器，才能修改公众号服务器配置
        """
        data = request.GET
        signature = data.get("signature", "")
        timestamp = data.get("timestamp", "")
        nonce = data.get("nonce", "")
        echostr = data.get("echostr", "")

        result = check_signature(signature, timestamp, nonce, echostr)
        return HttpResponse(content=result)

    def reply_message(self, request: Request) -> HttpResponse:
        text = request.data
        logger.info(f"receive: {text=}")
        logger.info(xml_utils.xml2dict(text))
        xml_data = xml_utils.xml2dict(text).get("xml", {})

        msg_type = xml_data.get("MsgType", "")
        if msg_type == "text":
            message = xml_data.get("Content", "")
            content = get_stock_market_info(message)

            if not content:
                content = "查询失败"

            to_user_name = xml_data.get("FromUserName", "")
            from_user_name = xml_data.get("ToUserName", "")
            logger.info(f"reply message {to_user_name=}, {from_user_name=}, {content=}")

            content = get_resp_content(from_user_name, to_user_name, content)
            return HttpResponse(content)
        return HttpResponse("fail")


# todo: permission_classes, authentication_classes 使用问题
@api_view(["GET"])
@permission_classes([])
@authentication_classes([])
def check_token(request: Request) -> HttpResponse:
    pass
