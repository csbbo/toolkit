import logging
import os
from typing import Iterable, List, Optional, Tuple, Union

import requests  # type: ignore
import tushare
from tushare.pro.client import DataApi

logger = logging.getLogger(__name__)


def get_client() -> DataApi:
    tushare_client = tushare.pro_api(os.getenv("TU_SHARE_TOKEN"))
    return tushare_client


def fetch_stocks(fields: Optional[list] = None) -> Iterable[dict]:
    """
    https://tushare.pro/document/2?doc_id=25
    """
    if fields is None:
        fields = [
            "ts_code",
            "symbol",
            "name",
            "area",
            "industry",
            "fullname",
            "enname",
            "cnspell",
            "market",
            "exchange",
            "curr_type",
            "list_status",
            "list_date",
            "delist_date",
            "is_hs",
        ]

    client = get_client()
    df = client.query(
        "stock_basic", exchange="", list_status="L", fields=",".join(fields)
    )
    for _, row in df.iterrows():
        yield {key: row[key] for key in fields}


def get_real_time_market(ts_code: str) -> Tuple[Optional[float], Optional[str]]:
    """
    return: price, rose
    """
    code, market = ts_code.split(".")
    q = f"{market.lower()}{code}"

    url = f"http://qt.gtimg.cn/q={q}"
    try:
        r = requests.get(url)
    except Exception as e:
        logger.error(f"get real time market fail: \n{str(e)}")
        return None, None

    price_list = r.text.split("~")
    return float(price_list[3]), price_list[32]


def get_quotes(ts_codes: Union[str, List[str]]) -> List[dict]:
    """
    获取实时腾讯实时行情接口
    示例: https://qt.gtimg.cn/q=sz000001
    """
    results: List[dict] = []

    if isinstance(ts_codes, str):
        ts_codes = [ts_codes]

    query_codes = []
    for ts_code in ts_codes:
        code, market = ts_code.split(".")
        query_codes.append(f"{market.lower()}{code}")
    q = ",".join(query_codes)

    url = f"http://qt.gtimg.cn/q={q}"
    try:
        r = requests.get(url)
        info_list = r.text.split(";")
        for single_info in info_list:
            single_info = single_info.split("=")
            if len(single_info) != 2:
                continue
            key = single_info[0].strip("\n").replace("v_", "")
            value = single_info[1].strip('"')

            ts_code = f"{key[2:]}.{key[:2].upper()}"
            info = value.split("~")
            result = {
                "ts_code": ts_code,
                "name": info[1],
                "datetime": info[30],
                "price": info[3],
                "pre_close": info[4],
                "open": info[5],
                "high": info[33],
                "low": info[34],
                "incr_limit": info[47],
                "drop_limit": info[48],
                "chg": info[31],
                "pct_chg": f"{info[32]}%",
                "vol": info[36],
                "amount": info[37],
                "turnover_rate": f"{info[38]}%",
                "total_mv": info[45],
                "circ_mv": info[44],
            }
            results.append(result)
    except Exception as e:
        logger.error(f"get real time quote fail: {str(e)}")

    return results
