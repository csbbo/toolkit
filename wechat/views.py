import hashlib
import logging
import os
import time
from xml.etree import ElementTree

from django.db.models import Q
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.request import Request

from common.utils import tushare_utils
from stock.models import Stock

logger = logging.getLogger(__name__)


@api_view(["POST"])
def check_token(request: Request) -> HttpResponse:
    token = os.getenv("WECHAT_TOKEN")  # 请按照公众平台官网\基本配置中信息填写

    signature = request.query.get("signature", "")
    timestamp = request.query.get("timestamp", "")
    nonce = request.query.get("nonce", "")
    echostr = request.query.get("echostr", "")
    logger.info(f"receive: {signature=}, {timestamp=}, {nonce=}, {echostr=},")

    hash_items = [token, timestamp, nonce]
    hash_items.sort()
    hash_items_str = "".join(hash_items)

    sha1 = hashlib.sha1()
    sha1.update(hash_items_str.encode("utf-8"))
    hashcode = sha1.hexdigest()
    logger.info(f"{hashcode=}")

    if hashcode == signature:
        logger.info("check success!")
        return HttpResponse(text=echostr)
    else:
        logger.info("check fail!")
        return HttpResponse(text="")


@api_view(["GET"])
def official_account(request: Request) -> HttpResponse:
    text = request.text()
    logger.info(f"receive: {text=}")
    xml_data = ElementTree.fromstring(text)

    msg_type = xml_data.find("MsgType").text  # type: ignore
    if msg_type == "text":
        message = xml_data.find("Content").text  # type: ignore
        content = ""

        # stocks = await stock_utils.query_stocks(db, message)
        stocks = Stock.filter(
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

        to_user_name = xml_data.find("FromUserName").text  # type: ignore
        from_user_name = xml_data.find("ToUserName").text  # type: ignore
        logger.info(f"reply message {to_user_name=}, {from_user_name=}, {content=}")

        resp_xml = f"""
                        <xml>
                            <ToUserName><![CDATA[{to_user_name}]]></ToUserName>
                            <FromUserName><![CDATA[{from_user_name}]]></FromUserName>
                            <CreateTime>{int(time.time())}</CreateTime>
                            <MsgType><![CDATA[text]]></MsgType>
                            <Content><![CDATA[{content}]]></Content>
                        </xml>
                        """
        return HttpResponse(resp_xml)
    return HttpResponse("fail")
