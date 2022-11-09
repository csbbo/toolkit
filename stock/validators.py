from rest_framework import serializers


class StockInfoSerializer(serializers.Serializer):
    search = serializers.ListField(
        child=serializers.CharField(
            error_messages={"required": "search为必填项", "blank": "search不能为空"}
        )
    )
