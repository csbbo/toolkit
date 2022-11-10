from django.urls import path

from wechat.views import WxViewSet

urlpatterns = [
    path("wx/", WxViewSet.as_view({"get": "check_token", "post": "reply_message"})),
]
