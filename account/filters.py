from typing import List

from account.models import User
from common.filters import DynamicFilter


class UserFilter(DynamicFilter):
    class Meta:
        model = User
        fields: List[str] = []


class FeedbackFilter(DynamicFilter):
    class Meta:
        model = User
        fields: List[str] = []
