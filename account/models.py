from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import UserManager
from django.db import models

from common.models import CUBaseModel


# password与last_login是AbstractBaseUser中字段
class User(AbstractBaseUser, CUBaseModel):
    id = models.BigAutoField(primary_key=True, auto_created=True)
    username = models.CharField(max_length=120, unique=True, db_index=True)
    phone = models.CharField(max_length=11, null=True, unique=True, db_index=True)
    email = models.CharField(max_length=120, null=True, unique=True, db_index=True)
    name = models.CharField(max_length=120, null=True)
    password = models.CharField(max_length=128, null=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    signature = models.CharField(max_length=120, default="")
    last_login_time = models.DateTimeField(null=True)

    USERNAME_FIELD = "username"
    objects = UserManager()

    class Meta:
        db_table = "account_user"
        ordering = ("-create_time",)
