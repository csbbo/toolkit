from django.contrib import admin

from common.admin import get_search_help_text
from stock.models import Stock


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    fields = [
        "id",
        ("ts_code", "symbol", "name", "cnspell"),
        ("fullname", "enname"),
        ("area", "industry", "market", "exchange", "curr_type"),
        ("list_date", "delist_date", "list_status", "is_hs"),
        ("create_time", "update_time"),
    ]
    readonly_fields = ["id", "create_time", "update_time"]

    list_display = [
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
    ]
    list_display_links = ["ts_code"]

    search_fields = [
        x for x in list_display if x not in ["id", "create_time", "update_time"]
    ]
    search_help_text = get_search_help_text(search_fields)
    # 分类筛选字段
    list_filter = [
        x
        for x in list_display
        if x not in {"id", "name", "ts_code", "symbol", "cnspell", "fullname", "enname"}
    ]
