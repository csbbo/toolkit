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
from rest_framework_xml.parsers import XMLParser

from common.utils import xml_utils
from common.utils.log_utils import save_stock_op_log
from common.utils.shell_utils import run_command
from stock.utils import get_stock_market_info
from wechat.utils import check_signature, get_resp_content

logger = logging.getLogger(__name__)


class WxViewSet(GenericViewSet):
    parser_classes = [XMLParser]
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
        """
        https://developers.weixin.qq.com/doc/offiaccount/Getting_Started/Getting_Started_Guide.html
        """
        body = request.body.decode(encoding="utf-8")

        xml_data = xml_utils.xml2dict(body).get("xml", {})

        msg_type = xml_data.get("MsgType", "")
        message = xml_data.get("Content", "")
        to_user_name = xml_data.get("FromUserName", "")
        from_user_name = xml_data.get("ToUserName", "")

        if msg_type == "text":
            # 包含空格则认为是命令
            if " " in message:
                result, error = run_command(message)
                if not error:
                    content = result
                else:
                    content = error
            else:
                content = get_stock_market_info(message)
                save_stock_op_log(
                    search=message,
                    response=content,
                    request_from="wechat",
                    ip=request.META.get("REMOTE_ADDR"),
                )
                logger.info(
                    f"reply message {from_user_name=}, {to_user_name=}, {content=}"
                )

            content = get_resp_content(from_user_name, to_user_name, content)
            return HttpResponse(content)
        return HttpResponse(content="")


# todo: permission_classes, authentication_classes 使用问题
@api_view(["GET"])
@permission_classes([])
@authentication_classes([])
def check_token(request: Request) -> HttpResponse:
    pass
