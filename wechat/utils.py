import os
import time

from common.utils import hash_utils


def check_signature(signature: str, timestamp: str, nonce: str) -> bool:
    token = os.getenv("WECHAT_TOKEN", "")  # 请按照公众平台官网\基本配置中信息填写
    params = [token, timestamp, nonce]
    params.sort()
    content = "".join(params)

    hashcode = hash_utils.get_sha1(content)
    return hashcode == signature


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
