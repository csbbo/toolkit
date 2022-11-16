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


class Config(CUBaseModel):
    id = models.BigAutoField(primary_key=True, auto_created=True)
    key = models.CharField(max_length=20, db_index=True, unique=True)
    value = models.TextField()
    category = models.CharField(max_length=20, null=True)
    remark = models.TextField(default="")

    class Meta:
        ordering = ("-update_time",)

    def __str__(self) -> str:
        """
        https://www.cnblogs.com/miaoning/p/11399575.html
        """
        return f"{self.key} ({self.id})"


class Log(CBaseModel):
    id = models.BigAutoField(primary_key=True, auto_created=True)
    type = models.IntegerField()
    info = models.JSONField(default=dict)

    class Meta:
        ordering = ("-create_time",)

    def __str__(self) -> str:
        return f"{self.type} ({self.id})"


class ScheduleTask(CUBaseModel):
    id = models.BigAutoField(primary_key=True, auto_created=True)
    trigger = models.CharField(max_length=8)
    config = models.JSONField(default=dict)
    name = models.CharField(max_length=200)
    actor_name = models.CharField(max_length=1024, null=True)
    args = models.JSONField(default=list)
    kwargs = models.JSONField(default=dict)
    priority = models.PositiveIntegerField(default=None)
    enabled = models.BooleanField(default=True)

    class Meta:
        ordering = ("-create_time",)

    def __str__(self) -> str:
        return f"{self.id}"
