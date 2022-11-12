from typing import List, Union

from django.db.models import Q

from common.utils.tushare_utils import get_quotes
from stock.models import Quote, Stock


def batch_save_stocks(items: list, batch_size: int = 100) -> None:
    update_fields: List[str] = []
    unique_fields = ["ts_code"]

    bulk_create_list = []
    for item in items:
        if not update_fields:
            update_fields = [x for x in item.keys() if x not in unique_fields]
        bulk_create_list.append(Stock(**item))

    Stock.objects.bulk_create(
        bulk_create_list,
        batch_size=batch_size,
        update_conflicts=True,
        update_fields=update_fields,
        unique_fields=unique_fields,
    )


def batch_save_quotes(items: list, batch_size: int = 100) -> None:
    update_fields: List[str] = []
    unique_fields = ["stock_id", "date"]

    bulk_create_list = []
    for item in items:
        if not update_fields:
            update_fields = [x for x in item.keys() if x not in unique_fields]
        bulk_create_list.append(Quote(**item))

    Quote.objects.bulk_create(
        bulk_create_list,
        batch_size=batch_size,
        update_conflicts=True,
        update_fields=update_fields,
        unique_fields=unique_fields,
    )


def get_stock_market_info(search: Union[str, list]) -> str:
    """
    实时行情信息
    """
    results = []
    if isinstance(search, str):
        search = [search]

    for s in search:
        queryset = Stock.objects.filter(
            Q(ts_code=s) | Q(symbol=s) | Q(cnspell__icontains=s) | Q(name__icontains=s)
        )[:20]

        ts_codes = queryset.values_list("ts_code", flat=True)
        for item in get_quotes(ts_codes):
            name = item["name"]
            pct_chg = item["pct_chg"]
            price = item["price"]
            results.append(f"{name} {price} {pct_chg}%")
    return "\n".join(results) + "\n"
