import json
import re
from itertools import chain
from typing import Tuple

from django.db.models import Q, QuerySet
from django.http import QueryDict
from django_filters.rest_framework import FilterSet
from rest_framework.request import Request


class DynamicFilter(FilterSet):
    LOOKUP_CONDITIONS = {
        "contains",
        "icontains",
        "gt",
        "gte",
        "lt",
        "lte",
        "startswith",
        "endswith",
        "overlap",
        "len",
    }

    def __init__(
        self,
        data: QueryDict = None,
        queryset: QuerySet = None,
        *,
        request: Request = None,
        prefix: object = None,
    ):
        allow_filter_fields, allow_ordering_fields = self.get_valid_fields(self)
        valid_data = self.get_valid_data(data, allow_filter_fields)
        queryset = self.get_dynamic_filter_qs(queryset, valid_data)

        if ordering := self.get_ordering_fields(data, allow_ordering_fields):
            queryset = queryset.order_by(*ordering)
        super().__init__(data=data, queryset=queryset, request=request, prefix=prefix)

    @staticmethod
    def get_valid_fields(obj: object) -> Tuple[set, set]:
        _meta = getattr(obj, "Meta", None)
        _model_meta_field_att = getattr(
            getattr(getattr(_meta, "model"), "_meta"), "fields"
        )

        model_fields = [field.get_attname() for field in _model_meta_field_att]
        declared_fields = [x for x in getattr(obj, "declared_filters")]
        exclude_fields = getattr(_meta, "exclude", [])
        include_fields_prefix = getattr(_meta, "fields_prefix", [])

        include_fields_prefix = [f"{field}*" for field in include_fields_prefix]
        filter_fields = {
            field
            for field in chain(model_fields, include_fields_prefix)
            if field not in [*exclude_fields, *declared_fields]
        }
        ordering_fields = {
            field for field in model_fields if field not in exclude_fields
        }
        return filter_fields, ordering_fields

    @staticmethod
    def is_valid_field(field: str, allow_fields: set) -> bool:
        regex = re.compile(r"^[a-z0-9_]*$", re.IGNORECASE)

        for allow_field in allow_fields:
            if allow_field.endswith("*"):
                allow_field = allow_field.rstrip("*")
                if regex.match(field) and field.startswith(allow_field):
                    return True
            elif field == allow_field:
                return True
        return False

    @staticmethod
    def get_perfect_data(data: QueryDict) -> dict:
        result = {}
        for key in data.keys():
            values = []
            for v in data.getlist(key):
                if key.endswith("__bool"):
                    v = v.lower() == "true"
                if key.endswith("__int"):
                    v = int(v)
                elif key.endswith("__list") or key.endswith("__dict"):
                    v = json.loads(v)
                values.append(v)
            result[key] = values
        return result

    @staticmethod
    def get_valid_data(data: QueryDict, allow_fields: set) -> dict:
        result = {}
        data = DynamicFilter.get_perfect_data(data)
        for key, values in data.items():
            strip_key = key.lstrip("~")

            field_lookup = strip_key.rsplit("__", 1)
            field, lookup = field_lookup[0], field_lookup[-1]

            if lookup not in DynamicFilter.LOOKUP_CONDITIONS:
                field = key

            if not DynamicFilter.is_valid_field(field, allow_fields):
                continue

            result[key] = values
        return result

    @staticmethod
    def get_dynamic_filter_qs(queryset: QuerySet, data: dict) -> QuerySet:
        queries = Q()
        for key, values in data.items():
            sub_queries = Q()
            for value in values:
                sub_queries |= Q(**{key: value})
            if key.startswith("~"):
                queries &= ~sub_queries
            else:
                queries &= sub_queries
        return queryset.filter(queries)

    @staticmethod
    def get_ordering_fields(data: QueryDict, allow_ordering_fields: set) -> list:
        ordering = []
        for value in data.getlist("ordering"):
            if value.startswith("-"):
                strip_field = value.lstrip("-")
            else:
                strip_field = value
            if strip_field in allow_ordering_fields:
                ordering.append(value)
        return ordering
