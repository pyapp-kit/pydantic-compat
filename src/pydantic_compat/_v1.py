import pydantic.version

if not pydantic.version.VERSION.startswith("1"):
    raise ImportError("pydantic_compat._v1 only supports pydantic v1.x")


class PydanticCompatMixin:
    ...
