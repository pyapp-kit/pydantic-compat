from typing import Any

import pydantic.version
from pydantic import BaseModel

from ._shared import _check_mixin_order

if int(pydantic.version.VERSION[0]) <= 1:
    raise ImportError("pydantic_compat._v2 only supports pydantic v2.x")


class PydanticCompatMixin:
    def __init_subclass__(cls, *args: Any, **kwargs: Any) -> None:
        _check_mixin_order(cls, PydanticCompatMixin, BaseModel)

    def dict(self: BaseModel, *args: Any, **kwargs: Any) -> Any:
        return self.model_dump(*args, **kwargs)

    def json(self: BaseModel, *args: Any, **kwargs: Any) -> Any:
        return self.model_dump_json(*args, **kwargs)

    def copy(self: BaseModel, *args: Any, **kwargs: Any) -> Any:
        return self.model_copy(*args, **kwargs)

    @classmethod
    def schema(cls: BaseModel, *args: Any, **kwargs: Any) -> Any:
        return cls.model_json_schema(*args, **kwargs)

    @classmethod
    def validate(cls: BaseModel, *args: Any, **kwargs: Any) -> Any:
        return cls.model_validate(*args, **kwargs)

    @classmethod
    def construct(cls: BaseModel, *args: Any, **kwargs: Any) -> Any:
        return cls.model_construct(*args, **kwargs)

    @classmethod
    def parse_obj(cls: BaseModel, *args: Any, **kwargs: Any) -> Any:
        return cls.model_validate(*args, **kwargs)

    @classmethod
    def parse_raw(cls: BaseModel, *args: Any, **kwargs: Any) -> Any:
        return cls.model_validate_json(*args, **kwargs)
