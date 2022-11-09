from typing import Optional

from rest_framework.renderers import JSONRenderer


class UniformJSONRenderer(JSONRenderer):
    """
    https://stackoverflow.com/a/20426493
    """

    def render(
        self,
        data: Optional[dict],
        accepted_media_type: Optional[str] = None,
        renderer_context: Optional[dict] = None,
    ) -> bytes:
        if not isinstance(data, dict) or "err" not in data:
            data = {"err": None, "data": data}

        return super().render(data, accepted_media_type, renderer_context)
