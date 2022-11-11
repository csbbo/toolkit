from django.contrib import admin

from stock.models import Stock


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    """
    https://docs.djangoproject.com/zh-hans/4.1/ref/contrib/admin/#django.contrib.admin.ModelAdmin.list_display
    """

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

    # 搜索对所有字段起作用
    search_fields = list_display

    # 分类筛选字段
    list_filter = [
        x
        for x in list_display
        if x not in {"id", "name", "ts_code", "symbol", "cnspell", "fullname", "enname"}
    ]
