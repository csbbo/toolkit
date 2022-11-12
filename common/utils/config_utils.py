import json
from typing import Any

from django.core.exceptions import ObjectDoesNotExist

from common.models import Config


def get_dict_config(key: str, default: Any = None) -> Any:
    value = get_config(key, default)

    if value and isinstance(value, str):
        value = json.loads(value)
    return value


def get_int_config(key: str, default: Any = None) -> Any:
    value = get_config(key, default)

    if value and isinstance(value, str):
        value = int(value)
    return value


def get_float_config(key: str, default: Any = None) -> Any:
    value = get_config(key, default)

    if value and isinstance(value, str):
        value = float(value)
    return value


def get_config(key: str, default: Any = None) -> Any:
    try:
        return Config.objects.get(key=key).value
    except ObjectDoesNotExist:
        return default
