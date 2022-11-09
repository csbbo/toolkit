from django.db import models

from common.models import CUBaseModel


class Stock(CUBaseModel):
    ts_code = models.CharField(max_length=200, default="", null=True)
    symbol = models.CharField(max_length=200, default="", null=True)
    name = models.CharField(max_length=200, default="", null=True)
    area = models.CharField(max_length=200, default="", null=True)
    industry = models.CharField(max_length=200, default="", null=True)
    fullname = models.CharField(max_length=200, default="", null=True)
    enname = models.CharField(max_length=200, default="", null=True)
    market = models.CharField(max_length=200, default="", null=True)
    exchange = models.CharField(max_length=200, default="", null=True)
    curr_type = models.CharField(max_length=200, default="", null=True)
    list_status = models.CharField(max_length=200, default="", null=True)
    list_date = models.CharField(max_length=200, default="", null=True)
    delist_date = models.CharField(max_length=200, default="", null=True)
    is_hs = models.CharField(max_length=200, default="", null=True)

    class Meta:
        ordering = ("-update_time",)
