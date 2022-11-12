from django import forms
from django.contrib import admin
from django.core.handlers.wsgi import WSGIRequest
from django.db.models import QuerySet

from common.admin import get_search_help_text
from common.utils.tushare_utils import get_quotes
from stock.models import Quote, Stock


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    class Form(forms.ModelForm):
        area = forms.CharField(required=False)
        industry = forms.CharField(required=False)
        delist_date = forms.CharField(required=False)

    form = Form
    fields = (
        "id",
        ("ts_code", "symbol", "name", "cnspell"),
        ("fullname", "enname"),
        ("area", "industry", "market", "exchange", "curr_type"),
        ("list_date", "delist_date", "list_status", "is_hs"),
        ("create_time", "update_time"),
    )
    readonly_fields = ("id", "create_time", "update_time")

    list_display = (
        "id",
        "ts_code",
        "symbol",
        "name",
        "cnspell",
        "market",
        "industry",
        "area",
        "list_date",
        "list_status",
        "is_hs",
        "fullname",
        "enname",
        "exchange",
        "curr_type",
        "delist_date",
        "create_time",
        "update_time",
    )
    list_display_links = ("ts_code",)

    search_fields = [
        x for x in list_display if x not in ["id", "create_time", "update_time"]
    ]
    search_help_text = get_search_help_text(search_fields)
    # 分类筛选字段
    list_filter = [
        x
        for x in list_display
        if x
        not in {
            "id",
            "name",
            "ts_code",
            "symbol",
            "cnspell",
            "fullname",
            "enname",
            "list_date",
        }
    ]
    list_per_page = 10
    ordering = ("symbol",)


@admin.register(Quote)
class QuoteAdmin(admin.ModelAdmin):
    actions = ("update_price",)
    list_display = (
        "stock",
        "price",
        "pct_chg",
        "turnover_rate",
        "date",
        "pre_close",
        "open",
        "high",
        "low",
        "incr_limit",
        "drop_limit",
        "chg",
        "vol",
        "amount",
        "total_mv",
        "circ_mv",
    )

    readonly_fields = list_display

    search_fields = ("stock__name", "stock__ts_code")
    search_help_text = get_search_help_text(search_fields)
    list_filter = ("date",)
    list_per_page = 10
    ordering = ("-turnover_rate",)

    @admin.display(description="update price")
    def update_price(self, request: WSGIRequest, queryset: QuerySet) -> None:
        ts_codes = list(queryset.values_list("stock__ts_code", flat=True))
        result_map: dict = {}

        for result in get_quotes(ts_codes=ts_codes):
            result_map[result["ts_code"]] = result

        bulk_update_list: list = []
        for quote in queryset.select_related("stock"):
            quote.price = result_map[quote.stock.ts_code]["price"]
            bulk_update_list.append(quote)

        Quote.objects.bulk_update(bulk_update_list, fields=["price"], batch_size=500)
