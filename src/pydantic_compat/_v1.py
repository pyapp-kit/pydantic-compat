from typing import Any

import pydantic.version
from pydantic import BaseModel

from ._shared import _check_mixin_order

if not pydantic.version.VERSION.startswith("1"):
    raise ImportError("pydantic_compat._v1 only supports pydantic v1.x")


class PydanticCompatMixin:
    def __init_subclass__(cls, *args: Any, **kwargs: Any) -> None:
        _check_mixin_order(cls, PydanticCompatMixin, BaseModel)

    def model_dump(self: BaseModel, *args: Any, **kwargs: Any) -> Any:
        return self.dict(*args, **kwargs)

    def model_dump_json(self: BaseModel, *args: Any, **kwargs: Any) -> Any:
        return self.json(*args, **kwargs)

    def model_copy(self: BaseModel, *args: Any, **kwargs: Any) -> Any:
        return self.copy(*args, **kwargs)

    @classmethod
    def model_json_schema(cls: BaseModel, *args: Any, **kwargs: Any) -> Any:
        return cls.schema(*args, **kwargs)

    @classmethod
    def model_validate(cls: BaseModel, *args: Any, **kwargs: Any) -> Any:
        return cls.validate(*args, **kwargs)

    @classmethod
    def model_construct(cls: BaseModel, *args: Any, **kwargs: Any) -> Any:
        return cls.construct(*args, **kwargs)

    @classmethod
    def model_validate_json(cls: BaseModel, *args: Any, **kwargs: Any) -> Any:
        return cls.parse_raw(*args, **kwargs)
