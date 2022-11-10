from django.urls import path

from wechat.views import check_token

urlpatterns = [
    path("token/", check_token),
]
