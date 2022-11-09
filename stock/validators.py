from rest_framework import serializers
from rest_framework.exceptions import ValidationError


class StockInfoSerializer(serializers.Serializer):
    pinyin = serializers.CharField(required=False)
    name = serializers.CharField(required=False)
    ts_code = serializers.CharField(required=False)
    symbol = serializers.CharField(required=False)

    def validate(self, attrs):
        if not attrs:
            raise ValidationError("参数不能为空")
        return attrs
