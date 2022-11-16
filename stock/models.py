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
    fullname = models.CharField(max_length=100, verbose_name="股票全称")
    enname = models.CharField(max_length=200, verbose_name="英文全称")
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
        return f"{self.ts_code} {self.name}"


class Quote(CUBaseModel):
    """
    只保留最近30个交易日行情
    """

    stock = models.ForeignKey(
        Stock, db_constraint=False, on_delete=models.CASCADE, related_name="history"
    )
    date = models.DateField(verbose_name="时间")

    price = models.FloatField(verbose_name="当前价格")
    pre_close = models.FloatField(null=True, verbose_name="昨日收盘价")
    open = models.FloatField(null=True, verbose_name="开盘价")
    high = models.FloatField(null=True, verbose_name="最高价")
    low = models.FloatField(null=True, verbose_name="最低价")
    incr_limit = models.FloatField(null=True, verbose_name="涨停价")
    drop_limit = models.FloatField(null=True, verbose_name="跌停价")
    chg = models.FloatField(null=True, verbose_name="涨跌")
    pct_chg = models.FloatField(null=True, max_length=8, verbose_name="涨跌幅")
    vol = models.FloatField(null=True, verbose_name="成交量(手)")
    amount = models.FloatField(null=True, verbose_name="成交额(万)")
    turnover_rate = models.FloatField(null=True, max_length=8, verbose_name="换手率")
    total_mv = models.FloatField(null=True, verbose_name="总市值")
    circ_mv = models.FloatField(null=True, verbose_name="流通市值")

    class Meta:
        unique_together = ("stock", "date")
        ordering = ("-update_time",)

    def __str__(self) -> str:
        return f"{self.stock.ts_code}, {self.date} ({self.id})"
