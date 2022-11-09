from rest_framework.authentication import SessionAuthentication
from rest_framework.request import Request


# 替换默认SessionAuthentication，SessionAuthentication会开启Csrf认证
class CsrfExemptSessionAuthentication(SessionAuthentication):
    """
    https://blog.csdn.net/denglinglin2653/article/details/101223037
    """

    def enforce_csrf(self, request: Request) -> None:
        return
