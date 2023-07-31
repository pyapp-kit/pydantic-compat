import pydantic.version

if int(pydantic.version.VERSION[0]) <= 1:
    raise ImportError("pydantic_compat._v2 only supports pydantic v2.x")


class PydanticCompatMixin:
    ...
