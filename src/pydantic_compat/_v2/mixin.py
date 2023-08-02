from __future__ import annotations

from typing import TYPE_CHECKING, Any, TypeVar, cast

from pydantic import BaseModel, ConfigDict
from pydantic._internal import _model_construction

from pydantic_compat._shared import V2_RENAMED_CONFIG_KEYS, _check_mixin_order

if TYPE_CHECKING:
    BM = TypeVar("BM", bound=BaseModel)


def _convert_config(config: type) -> ConfigDict:
    config_dict = {k: getattr(config, k) for k in dir(config) if not k.startswith("__")}

    deprecated_renamed_keys = V2_RENAMED_CONFIG_KEYS.keys() & config_dict.keys()
    for k in sorted(deprecated_renamed_keys):
        config_dict[V2_RENAMED_CONFIG_KEYS[k]] = config_dict.pop(k)

    # leave these here for now to warn about lost functionality
    # deprecated_removed_keys = V2_REMOVED_CONFIG_KEYS & config_dict.keys()
    # for k in sorted(deprecated_removed_keys):
    #     config_dict.pop(k)

    return cast(ConfigDict, config_dict)


class _MixinMeta(_model_construction.ModelMetaclass):
    def __new__(cls, name, bases, namespace, **kwargs):
        if "Config" in namespace and isinstance(namespace["Config"], type):
            namespace["model_config"] = _convert_config(namespace.pop("Config"))
        return super().__new__(cls, name, bases, namespace, **kwargs)


class PydanticCompatMixin(metaclass=_MixinMeta):
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
