import logging

from django.db.models import Q
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.request import Request

from common.utils import tushare_utils, xml_utils
from stock.models import Stock
from wechat.utils import check_signature, get_resp_content

logger = logging.getLogger(__name__)


@api_view(["POST"])
def check_token(request: Request) -> HttpResponse:
    signature = request.query.get("signature", "")
    timestamp = request.query.get("timestamp", "")
    nonce = request.query.get("nonce", "")
    echostr = request.query.get("echostr", "")
    logger.info(f"receive: {signature=}, {timestamp=}, {nonce=}, {echostr=},")

    check_success = check_signature(signature, timestamp, nonce)
    if not check_success:
        return HttpResponse(text="")
    return HttpResponse(text=echostr)


@api_view(["GET"])
def official_account(request: Request) -> HttpResponse:
    text = request.text()
    logger.info(f"receive: {text=}")
    xml_data = xml_utils.xml2dict(text)

    msg_type = xml_data.get("MsgType", "")
    if msg_type == "text":
        message = xml_data.get("Content", "")
        content = ""

        stocks = Stock.objects.filter(
            Q(ts_code=message)
            | Q(symbol=message)
            | Q(pinyin__icontains=message)
            | Q(name__icontains=message)
        )
        for stock in stocks:
            price = tushare_utils.get_real_time_market(stock.ts_code)
            content += f"{stock.name} {price}"

        if not content:
            content = "查询失败"

        to_user_name = xml_data.get("FromUserName", "")
        from_user_name = xml_data.get("ToUserName", "")
        logger.info(f"reply message {to_user_name=}, {from_user_name=}, {content=}")

        content = get_resp_content(from_user_name, to_user_name, content)
        return HttpResponse(content)
    return HttpResponse("fail")
