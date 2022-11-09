import logging
import os
from typing import Iterable, Optional, Tuple

import requests  # type: ignore
import tushare
from tushare.pro.client import DataApi

logger = logging.getLogger(__name__)


def get_client() -> DataApi:
    tushare_client = tushare.pro_api(os.getenv("TU_SHARE_TOKE"))
    return tushare_client


def fetch_stocks(fields: Optional[list] = None) -> Iterable[dict]:
    if fields is None:
        fields = [
            "ts_code",
            "symbol",
            "name",
            "area",
            "industry",
            "fullname",
            "enname",
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
