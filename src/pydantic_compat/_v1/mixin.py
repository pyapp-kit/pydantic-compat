from __future__ import annotations

import sys
from typing import TYPE_CHECKING, Any, ClassVar, Iterator, Mapping

from pydantic import main

from pydantic_compat._shared import V2_RENAMED_CONFIG_KEYS, check_mixin_order

if TYPE_CHECKING:
    from typing import Dict

    from pydantic.fields import ModelField  # type: ignore
    from typing_extensions import Protocol

    # fmt:off
    class Model(Protocol):
        def dict(self, *args: Any, **kwargs: Any) ->  Dict[str, Any]: ...  # noqa: UP006
        def json(self, *args: Any, **kwargs: Any) -> str: ...
        def copy(self, *args: Any, **kwargs: Any) -> Model: ...
        @classmethod
        def schema(cls, *args: Any, **kwargs: Any) -> Dict[str, Any]: ...  # noqa: UP006
        @classmethod
        def validate(cls, *args: Any, **kwargs: Any) -> Model: ...
        @classmethod
        def construct(cls, *args: Any, **kwargs: Any) -> Model: ...
        @classmethod
        def parse_raw(cls, *args: Any, **kwargs: Any) -> type[Model]: ...
        @classmethod
        def update_forward_refs(cls, *args: Any, **kwargs: Any) -> None: ...

        __fields__: ClassVar[Dict]  # noqa: UP006
        __fields_set__: set[str]
        __config__: ClassVar[type]
    # fmt:on

if sys.version_info < (3, 9):

    def _get_fields(obj) -> dict[str, Any]:
        return obj.__fields__

    main.ModelMetaclass.model_fields = property(_get_fields)

REVERSE_CONFIG_NAME_MAP = {v: k for k, v in V2_RENAMED_CONFIG_KEYS.items()}


def _convert_config(config_dict: dict) -> type:
    deprecated_renamed_keys = REVERSE_CONFIG_NAME_MAP.keys() & config_dict.keys()
    for k in sorted(deprecated_renamed_keys):
        config_dict[REVERSE_CONFIG_NAME_MAP[k]] = config_dict.pop(k)

    return type("Config", (), config_dict)


class _MixinMeta(main.ModelMetaclass):
    def __new__(cls, name, bases, namespace: dict, **kwargs):  # type: ignore
        if "model_config" in namespace and isinstance(namespace["model_config"], dict):
            namespace["Config"] = _convert_config(namespace.pop("model_config"))

        return super().__new__(cls, name, bases, namespace, **kwargs)


class PydanticCompatMixin(metaclass=_MixinMeta):
    @classmethod
    def __try_update_forward_refs__(cls, **localns: Any) -> None:
        sup = super()
        if hasattr(sup, "__try_update_forward_refs__"):
            sup.__try_update_forward_refs__(**localns)

    def __init_subclass__(cls, *args: Any, **kwargs: Any) -> None:
        check_mixin_order(cls, PydanticCompatMixin, main.BaseModel)

    def model_dump(self: Model, *args: Any, **kwargs: Any) -> Any:
        return self.dict(*args, **kwargs)

    def model_dump_json(self: Model, *args: Any, **kwargs: Any) -> Any:
        return self.json(*args, **kwargs)

    def model_copy(self: Model, *args: Any, **kwargs: Any) -> Any:
        return self.copy(*args, **kwargs)

    @classmethod
    def model_json_schema(cls: type[Model], *args: Any, **kwargs: Any) -> Any:
        return cls.schema(*args, **kwargs)

    @classmethod
    def model_validate(cls: type[Model], *args: Any, **kwargs: Any) -> Any:
        return cls.validate(*args, **kwargs)

    @classmethod
    def model_construct(cls: type[Model], *args: Any, **kwargs: Any) -> Any:
        return cls.construct(*args, **kwargs)

    @classmethod
    def model_validate_json(cls: type[Model], *args: Any, **kwargs: Any) -> Any:
        return cls.parse_raw(*args, **kwargs)

    @classmethod
    def model_rebuild(cls: type[Model], force: bool = True, **kwargs: Any) -> None:
        return cls.update_forward_refs(**kwargs)

    if sys.version_info < (3, 9):
        # differences in the behavior of patching class properties in python<3.9
        @property
        def model_fields(cls: type[Model]) -> Mapping[str, Any]:
            return FieldInfoMap(cls.__fields__)

    else:

        @classmethod  # type: ignore [misc]
        @property
        def model_fields(cls: type[Model]) -> Mapping[str, Any]:
            return FieldInfoMap(cls.__fields__)

    @property
    def model_fields_set(self: Model) -> set[str]:
        return self.__fields_set__

    @classmethod  # type: ignore [misc]
    @property
    def model_config(cls: type[Model]) -> Mapping[str, Any]:
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
