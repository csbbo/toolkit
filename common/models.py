from django.db import models


class CBaseModel(models.Model):
    """
    add create time for Model
    """

    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    class Meta:
        abstract = True


class CUBaseModel(CBaseModel):
    """
    add update time for Model
    """

    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        abstract = True
