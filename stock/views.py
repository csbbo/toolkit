from typing import Union

from django.db.models import Q
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

    @action(
        detail=False,
        methods=["GET"],
        url_path="info",
        serializer_class=StockInfoSerializer,
        permission_classes=[],
    )
    def info(self, request: Request) -> Union[Response, HttpResponse]:
        data = request.GET
        self.get_serializer(data=data).is_valid(raise_exception=True)

        searches = data.getlist("search")

        infos = []
        for search in searches:
            queryset = self.get_queryset().filter(
                Q(ts_code=search)
                | Q(symbol=search)
                | Q(pinyin__icontains=search)
                | Q(name__icontains=search)
            )

            for stock in queryset:
                name = stock.name
                ts_code = stock.ts_code
                price, rose = tushare_utils.get_real_time_market(ts_code)
                if not (price and rose):
                    infos.append(price)
                    continue

                infos.append(f"{name} {price} {rose}%")

        resp = "\n".join(infos) + "\n"
        return HttpResponse(resp)
