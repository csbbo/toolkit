from django.contrib import admin

from common.models import Config, Log


@admin.register(Config)
class ConfigAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "key",
        "value",
        "category",
        "remark",
        "create_time",
        "update_time",
    )
    list_display_links = ("id",)
    list_editable = ("value", "category")

    search_fields = ("key",)
    search_help_text = f"搜索{'、'.join(search_fields)}"
    list_filter = ("category", "create_time", "update_time")


@admin.register(Log)
class LogAdmin(admin.ModelAdmin):
    list_display = ("id", "type", "info", "create_time")
    list_display_links = ("id",)

    search_fields = ("type", "info")
    search_help_text = f"搜索{'、'.join(search_fields)}"
    list_filter = ("type", "create_time")
