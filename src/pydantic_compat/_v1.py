from typing import Any, TypeVar

import pydantic.version
from pydantic import BaseModel

from ._shared import _check_mixin_order

if not pydantic.version.VERSION.startswith("1"):
    raise ImportError("pydantic_compat._v1 only supports pydantic v1.x")

BM = TypeVar("BM", bound=BaseModel)


class PydanticCompatMixin:
    def __init_subclass__(cls, *args: Any, **kwargs: Any) -> None:
        _check_mixin_order(cls, PydanticCompatMixin, BaseModel)

    def model_dump(self: BM, *args: Any, **kwargs: Any) -> Any:
        return self.dict(*args, **kwargs)

    def model_dump_json(self: BM, *args: Any, **kwargs: Any) -> Any:
        return self.json(*args, **kwargs)

    def model_copy(self: BM, *args: Any, **kwargs: Any) -> Any:
        return self.copy(*args, **kwargs)

    @classmethod
    def model_json_schema(cls: type[BM], *args: Any, **kwargs: Any) -> Any:
        return cls.schema(*args, **kwargs)

    @classmethod
    def model_validate(cls: type[BM], *args: Any, **kwargs: Any) -> Any:
        return cls.validate(*args, **kwargs)

    @classmethod
    def model_construct(cls: type[BM], *args: Any, **kwargs: Any) -> Any:
        return cls.construct(*args, **kwargs)

    @classmethod
    def model_validate_json(cls: type[BM], *args: Any, **kwargs: Any) -> Any:
        return cls.parse_raw(*args, **kwargs)

    @classmethod
    def model_rebuild(cls: type[BM], **kwargs: Any) -> None:
        return cls.update_forward_refs(**kwargs)

    @classmethod
    @property
    def model_fields(cls: type[BM]) -> dict[str, Any]:
        return cls.__fields__
