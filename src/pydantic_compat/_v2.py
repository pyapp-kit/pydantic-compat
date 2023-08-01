from __future__ import annotations

import pydantic.version

if int(pydantic.version.VERSION[0]) <= 1:  # pragma: no cover
    raise ImportError("pydantic_compat._v2 only supports pydantic v2.x")

from typing import TYPE_CHECKING, Any, TypeVar

from pydantic import BaseModel

from ._shared import _check_mixin_order

if TYPE_CHECKING:
    BM = TypeVar("BM", bound=BaseModel)


class PydanticCompatMixin:
    def __init_subclass__(cls, *args: Any, **kwargs: Any) -> None:
        _check_mixin_order(cls, PydanticCompatMixin, BaseModel)
        # the deprecation warning is on the metaclass
        type(cls).__fields__ = property(lambda cls: cls.model_fields)

    def dict(self: BM, *args: Any, **kwargs: Any) -> Any:
        return self.model_dump(*args, **kwargs)

    def json(self: BM, *args: Any, **kwargs: Any) -> Any:
        return self.model_dump_json(*args, **kwargs)

    def copy(self: BM, *args: Any, **kwargs: Any) -> Any:
        return self.model_copy(*args, **kwargs)

    @classmethod
    def schema(cls: type[BM], *args: Any, **kwargs: Any) -> Any:
        return cls.model_json_schema(*args, **kwargs)

    @classmethod
    def validate(cls: type[BM], *args: Any, **kwargs: Any) -> Any:
        return cls.model_validate(*args, **kwargs)

    @classmethod
    def construct(cls: type[BM], *args: Any, **kwargs: Any) -> Any:
        return cls.model_construct(*args, **kwargs)

    @classmethod
    def parse_obj(cls: type[BM], *args: Any, **kwargs: Any) -> Any:
        return cls.model_validate(*args, **kwargs)

    @classmethod
    def parse_raw(cls: type[BM], *args: Any, **kwargs: Any) -> Any:
        return cls.model_validate_json(*args, **kwargs)

    # this is needed in addition to the metaclass patch in __init_subclass__
    @property
    def __fields__(self: BM) -> dict[str, Any]:
        return self.model_fields

    @property
    def __fields_set__(self: BM) -> set[str]:
        return self.model_fields_set

    if not TYPE_CHECKING:

        @classmethod
        def update_forward_refs(
            cls: type[BM],
            force: bool = False,
            raise_errors: bool = True,
            **localns: Any,
        ) -> None:
            cls.model_rebuild(
                forc=force, raise_errors=raise_errors, _types_namespace=localns
            )

        @classmethod
        def model_rebuild(
            cls: type[BM], force: bool = False, raise_errors: bool = True, **kwargs: Any
        ) -> None:
            return super().model_rebuild(
                force=force, raise_errors=raise_errors, _types_namespace=kwargs
            )
