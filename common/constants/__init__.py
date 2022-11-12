from typing import Any


class Constant:
    @classmethod
    def get_choices(cls) -> list:
        if hasattr(cls, "CHOICES"):
            return getattr(cls, "CHOICES")
        return []

    @classmethod
    def get_options(cls) -> list:
        options = []

        for choice in cls.get_choices():
            options.append(
                {
                    "value": choice[0],
                    "label": choice[1],
                }
            )
        return options

    @classmethod
    def get_display(cls, name: Any) -> str:
        data = dict(cls.get_choices())
        return data.get(name, "")

    @classmethod
    def get_values(cls, *, exclude_field: tuple = ("CHOICES",)) -> list:
        d = cls.__dict__
        ret = {
            str(d[item])
            for item in d.keys()
            if not item.startswith("_") and item not in exclude_field
        }
        return list(ret)
