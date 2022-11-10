from typing import Union

from django.http import HttpResponse
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from stock.filters import StockFilter
from stock.serializers import StockSerializer
from stock.utils import get_stock_market_info
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

        search = data.getlist("search")
        resp = get_stock_market_info(search)
        return HttpResponse(resp)
