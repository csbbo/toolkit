from django.db import models

from common.models import CUBaseModel


class Stock(CUBaseModel):
    ts_code = models.CharField(max_length=200)
    symbol = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    area = models.CharField(max_length=200)
    industry = models.CharField(max_length=200)
    fullname = models.CharField(max_length=200)
    enname = models.CharField(max_length=200)
    market = models.CharField(max_length=200)
    exchange = models.CharField(max_length=200)
    curr_type = models.CharField(max_length=200)
    list_status = models.CharField(max_length=200)
    list_date = models.CharField(max_length=200)
    delist_date = models.CharField(max_length=200)
    is_hs = models.CharField(max_length=200)

    class Meta:
        ordering = ("-update_time",)
