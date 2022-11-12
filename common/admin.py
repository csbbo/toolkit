from typing import Union

from django import forms
from django.contrib import admin

from common.models import Config, Log


def get_search_help_text(search_fields: Union[list, tuple]) -> str:
    """
    搜索框提示信息
    """
    return f"搜索: {'、'.join(search_fields)}"


"""
https://docs.djangoproject.com/zh-hans/4.1/ref/contrib/admin/#django.contrib.admin.ModelAdmin.list_display
https://blog.csdn.net/weixin_45987577/article/details/123880795
admin显示属性

list_display: 列表页显示字段
list_display_links: 可以链接到表单的字段
readonly_fields: 只读字段
list_per_page: 分页大小
ordering: 默认排序字段

search_fields: 列表页可以模糊搜索的字段
search_help_text: 模糊搜索提示文本
list_filter: 右侧筛选，可以继承自SimpleListFilter来自定义筛选字段和规则

fields: 详情页展示字段
form: 指定详情页form表单,可以自定义显示的数据, 字段
readonly_fields: 详情页只读字段
"""


@admin.register(Config)
class ConfigAdmin(admin.ModelAdmin):
    class Form(forms.ModelForm):
        key = forms.CharField(label="Key")
        value = forms.Textarea()
        category = forms.CharField(required=False, label="分类")
        remark = forms.CharField(required=False, label="备注")

    form = Form

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

    search_fields = ("key",)
    search_help_text = get_search_help_text(search_fields)
    list_filter = ("category", "create_time", "update_time")


@admin.register(Log)
class LogAdmin(admin.ModelAdmin):
    list_display = ("id", "type", "info", "create_time")
    list_display_links = ("id",)
    readonly_fields = list_display

    search_fields = ("type", "info")
    search_help_text = get_search_help_text(search_fields)
    list_filter = ("type", "create_time")
