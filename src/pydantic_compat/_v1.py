from __future__ import annotations

from typing import TYPE_CHECKING, Any, Iterator, Mapping, TypeVar

import pydantic.version

if not pydantic.version.VERSION.startswith("1"):
    raise ImportError("pydantic_compat._v1 only supports pydantic v1.x")

from pydantic import BaseModel

from ._shared import _check_mixin_order

if TYPE_CHECKING:
    from pydantic.fields import ModelField

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
    def model_rebuild(cls: type[BM], force: bool = True, **kwargs: Any) -> None:
        return cls.update_forward_refs(**kwargs)

    @classmethod  # type: ignore
    @property
    def model_fields(cls: type[BM]) -> Mapping[str, Any]:
        return FieldInfoMap(cls.__fields__)

    @property
    def model_fields_set(self: BM) -> set[str]:
        return self.__fields_set__  # type: ignore

    @classmethod  # type: ignore
    @property
    def model_config(cls: type[BM]) -> Mapping[str, Any]:
        return DictLike(cls.__config__)


class FieldInfoLike:
    """Wrapper to convera pydantic v1 ModelField to v2 FieldInfo."""

    def __init__(self, model_field: ModelField) -> None:
        self._model_field = model_field

    @property
    def annotation(self) -> Any:
        return self._model_field.outer_type_

    @property
    def frozen(self) -> bool:
        return not self._model_field.field_info.allow_mutation

    def __getattr__(self, key: str) -> Any:
        return getattr(self._model_field, key)


class FieldInfoMap(Mapping[str, FieldInfoLike]):
    """Adaptor between v1 __fields__ and v2 model_field."""

    def __init__(self, fields: dict[str, ModelField]) -> None:
        self._fields = fields

    def get(self, key: str, default: Any = None) -> Any:
        return self[key] if key in self._fields else default

    def __getitem__(self, key: str) -> FieldInfoLike:
        return FieldInfoLike(self._fields[key])

    def __setitem__(self, key: str, value: Any) -> None:
        self._fields[key] = value

    def __iter__(self) -> Iterator[str]:
        yield from self._fields

    def __len__(self) -> int:
        return len(self._fields)


class DictLike(Mapping[str, Any]):
    """Provide dict-like interface to an object."""

    def __init__(self, obj: Any) -> None:
        self._obj = obj

    def get(self, key: str, default: Any = None) -> Any:
        return getattr(self._obj, key, default)

    def __getitem__(self, key: str) -> Any:
        return getattr(self._obj, key)

    def __setitem__(self, key: str, value: Any) -> None:
        setattr(self._obj, key, value)

    def __iter__(self) -> Iterator[str]:
        yield from self._obj.__dict__

    def __len__(self) -> int:
        return len(self._obj.__dict__)
