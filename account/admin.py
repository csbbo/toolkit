from django.contrib import admin

from account.models import Group, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "username",
        "name",
        "phone",
        "email",
        "is_staff",
        "is_active",
        "is_superuser",
        "first_name",
        "last_name",
        "date_joined",
        "last_login",
        "create_time",
        "update_time",
    )


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ("name",)
