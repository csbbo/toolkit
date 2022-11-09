from typing import Union

from django.http import HttpResponse
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from common.utils import tushare_utils
from stock.filters import StockFilter
from stock.serializers import StockSerializer
from stock.validators import StockInfoSerializer


class StockViewSet(RetrieveModelMixin, ListModelMixin, GenericViewSet):
    serializer_class = StockSerializer
    queryset = serializer_class.Meta.model.objects.all()
    filterset_class = StockFilter

    @action(detail=False, methods=["GET"], url_path="info", serializer_class=StockInfoSerializer, permission_classes=[])
    def info(self, request: Request) -> Union[Response, HttpResponse]:
        data = request.GET
        self.get_serializer(data=data).is_valid(raise_exception=True)

        queryset = self.get_queryset()

        if pinyin := data.get("pinyin"):
            queryset = queryset.filter(pinyin__icontains=pinyin)

        if name := data.get("name"):
            queryset = queryset.filter(name__icontains=name)

        if ts_code := data.get("ts_code"):
            queryset = queryset.filter(ts_code=ts_code)

        if symbol := data.get("symbol"):
            queryset = queryset.filter(symbol=symbol)

        infos = []
        for stock in queryset:
            name = stock.name
            ts_code = stock.ts_code
            price, rose = tushare_utils.get_real_time_market(ts_code)
            if not (price and rose):
                infos.append(price)
                continue

            infos.append(f"{name} {price} {rose}%")
        return HttpResponse("\n".join(infos))
