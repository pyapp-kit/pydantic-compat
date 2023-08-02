from __future__ import annotations

from typing import TYPE_CHECKING, Any, ClassVar, Dict, cast

from pydantic import BaseModel
from pydantic._internal import _model_construction

from pydantic_compat._shared import V2_RENAMED_CONFIG_KEYS, check_mixin_order

if TYPE_CHECKING:
    from pydantic import ConfigDict
    from typing_extensions import Protocol

    # fmt:off
    class Model(Protocol):
        def model_dump(self, *args: Any, **kwargs: Any) ->  dict[str, Any]: ...
        def model_dump_json(self, *args: Any, **kwargs: Any) -> str: ...
        def model_copy(self, *args: Any, **kwargs: Any) -> Model: ...
        @classmethod
        def model_json_schema(cls, *args: Any, **kwargs: Any) -> dict[str, Any]: ...
        @classmethod
        def model_validate(cls, *args: Any, **kwargs: Any) -> Model: ...
        @classmethod
        def model_construct(cls, *args: Any, **kwargs: Any) -> Model: ...
        @classmethod
        def model_validate_json(cls, *args: Any, **kwargs: Any) -> type[Model]: ...
        @classmethod
        def model_rebuild(cls, *args: Any, **kwargs: Any) -> bool | None: ...

        model_fields: ClassVar[dict]
        model_fields_set: ClassVar[set[str]]
        model_config: ClassVar[ConfigDict]
    # fmt:on


def _convert_config(config: type) -> ConfigDict:
    config_dict = {k: getattr(config, k) for k in dir(config) if not k.startswith("__")}

    deprecated_renamed_keys = V2_RENAMED_CONFIG_KEYS.keys() & config_dict.keys()
    for k in sorted(deprecated_renamed_keys):
        config_dict[V2_RENAMED_CONFIG_KEYS[k]] = config_dict.pop(k)

    # leave these here for now to warn about lost functionality
    # deprecated_removed_keys = V2_REMOVED_CONFIG_KEYS & config_dict.keys()
    # for k in sorted(deprecated_removed_keys):
    #     config_dict.pop(k)

    return cast("ConfigDict", config_dict)


class _MixinMeta(_model_construction.ModelMetaclass):
    def __new__(cls, name, bases, namespace, **kwargs):  # type: ignore
        if "Config" in namespace and isinstance(namespace["Config"], type):
            namespace["model_config"] = _convert_config(namespace.pop("Config"))
        return super().__new__(cls, name, bases, namespace, **kwargs)


class PydanticCompatMixin(metaclass=_MixinMeta):
    def __init_subclass__(cls, *args: Any, **kwargs: Any) -> None:
        check_mixin_order(cls, PydanticCompatMixin, BaseModel)
        # the deprecation warning is on the metaclass
        type(cls).__fields__ = property(lambda cls: cls.model_fields)  # type: ignore

    def dict(self: Model, *args: Any, **kwargs: Any) -> Any:
        return self.model_dump(*args, **kwargs)

    def json(self: Model, *args: Any, **kwargs: Any) -> Any:
        return self.model_dump_json(*args, **kwargs)

    def copy(self: Model, *args: Any, **kwargs: Any) -> Any:
        return self.model_copy(*args, **kwargs)

    @classmethod
    def schema(cls: type[Model], *args: Any, **kwargs: Any) -> Any:
        return cls.model_json_schema(*args, **kwargs)

    @classmethod
    def validate(cls: type[Model], *args: Any, **kwargs: Any) -> Any:
        return cls.model_validate(*args, **kwargs)

    @classmethod
    def construct(cls: type[Model], *args: Any, **kwargs: Any) -> Any:
        return cls.model_construct(*args, **kwargs)

    @classmethod
    def parse_obj(cls: type[Model], *args: Any, **kwargs: Any) -> Any:
        return cls.model_validate(*args, **kwargs)

    @classmethod
    def parse_raw(cls: type[Model], *args: Any, **kwargs: Any) -> Any:
        return cls.model_validate_json(*args, **kwargs)

    # this is needed in addition to the metaclass patch in __init_subclass__
    @property
    def __fields__(self: Model) -> Dict[str, Any]:  # noqa: UP006
        return self.model_fields

    @property
    def __fields_set__(self: Model) -> set[str]:
        return self.model_fields_set

    @classmethod
    def update_forward_refs(
        cls: type[Model],
        force: bool = False,
        raise_errors: bool = True,
        **localns: Any,
    ) -> None:
        cls.model_rebuild(
            forc=force, raise_errors=raise_errors, _types_namespace=localns
        )

    @classmethod
    def model_rebuild(
        cls: type[Model], force: bool = False, raise_errors: bool = True, **kwargs: Any
    ) -> bool | None:
        return super().model_rebuild(
            force=force, raise_errors=raise_errors, _types_namespace=kwargs
        )
