from django.urls import include, path
from rest_framework import routers

from stock.views import StockViewSet

router = routers.SimpleRouter()
router.register("stock", StockViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
