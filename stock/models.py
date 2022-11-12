from django.db import models

from common.models import CUBaseModel


class Stock(CUBaseModel):
    id = models.BigAutoField(primary_key=True, auto_created=True)
    ts_code = models.CharField(
        max_length=9, db_index=True, unique=True, verbose_name="TS代码"
    )
    symbol = models.CharField(max_length=6, db_index=True, verbose_name="股票代码")
    name = models.CharField(max_length=20, db_index=True, verbose_name="股票名称")
    area = models.CharField(max_length=20, null=True, verbose_name="地域")
    industry = models.CharField(max_length=4, null=True, verbose_name="所属行业")
    fullname = models.CharField(max_length=40, verbose_name="股票全称")
    enname = models.CharField(max_length=80, verbose_name="英文全称")
    cnspell = models.CharField(max_length=20, verbose_name="拼音缩写")
    market = models.CharField(max_length=20, verbose_name="市场类型")
    exchange = models.CharField(max_length=20, verbose_name="交易所代码")
    curr_type = models.CharField(max_length=20, verbose_name="交易货币")
    list_status = models.CharField(max_length=1, verbose_name="上市状态")
    list_date = models.CharField(max_length=8, verbose_name="上市日期")
    delist_date = models.CharField(max_length=8, null=True, verbose_name="退市日期")
    is_hs = models.CharField(max_length=1, null=True, verbose_name="是否沪深港通标的")

    class Meta:
        ordering = ("-update_time",)

    def __str__(self) -> str:
        return f"{self.ts_code} {self.name} ({self.id})"
