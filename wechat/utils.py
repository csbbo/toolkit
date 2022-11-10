import logging
import os
import time

from common.utils import hash_utils

logger = logging.getLogger(__name__)


def check_signature(signature: str, timestamp: str, nonce: str, echostr: str) -> str:
    """
    @params signature: 微信加密签名，signature结合了开发者填写的 token 参数和请求中的 timestamp 参数、nonce参数
    @params timestamp: 时间戳
    @params nonce: 随机数
    @params echostr: 随机字符串, 原样返回 echostr 参数内容，则接入生效，成为开发者成功，否则接入失败
    """
    logger.info(f"check_signature: {signature=}, {timestamp=}, {nonce=}, {echostr=}")

    token = os.getenv("WECHAT_TOKEN", "")
    params = [token, timestamp, nonce]
    params.sort()
    content = "".join(params)

    hashcode = hash_utils.get_sha1(content)
    return echostr if (hashcode == signature) else ""


def get_resp_content(from_user: str, to_user: str, content: str) -> str:
    resp_xml = f"""
                <xml>
                    <ToUserName><![CDATA[{to_user}]]></ToUserName>
                    <FromUserName><![CDATA[{from_user}]]></FromUserName>
                    <CreateTime>{int(time.time())}</CreateTime>
                    <MsgType><![CDATA[text]]></MsgType>
                    <Content><![CDATA[{content}]]></Content>
                </xml>
                """
    return resp_xml
