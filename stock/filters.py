from typing import List

from common.filters import DynamicFilter
from stock.models import Stock


class StockFilter(DynamicFilter):
    class Meta:
        model = Stock
        fields: List[str] = []
