from django.contrib.auth.models import AbstractUser
from django.db import models

from common.models import CUBaseModel


class User(AbstractUser, CUBaseModel):
    """
    User全部字段查看AbstractUser, username, email, password等字段使用django默认支持的
    """

    id = models.BigAutoField(primary_key=True, auto_created=True)
    phone = models.CharField(max_length=11, null=True, unique=True, db_index=True)
    name = models.CharField(max_length=120, null=True)
    signature = models.CharField(max_length=120, default="")

    class Meta:
        ordering = ("-update_time",)
