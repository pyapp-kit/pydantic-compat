import contextlib
import warnings
from typing import Any

import pydantic
import pydantic.version

PYDANTIC2 = pydantic.version.VERSION.startswith("2")

V2_REMOVED_CONFIG_KEYS = {
    "allow_mutation",
    "error_msg_templates",
    "fields",
    "getter_dict",
    "smart_union",
    "underscore_attrs_are_private",
    "json_loads",
    "json_dumps",
    "copy_on_model_validation",
    "post_init_call",
}
V2_RENAMED_CONFIG_KEYS = {
    "allow_population_by_field_name": "populate_by_name",
    "anystr_lower": "str_to_lower",
    "anystr_strip_whitespace": "str_strip_whitespace",
    "anystr_upper": "str_to_upper",
    "keep_untouched": "ignored_types",
    "max_anystr_length": "str_max_length",
    "min_anystr_length": "str_min_length",
    "orm_mode": "from_attributes",
    "schema_extra": "json_schema_extra",
    "validate_all": "validate_default",
}

V1_FIELDS_TO_V2_FIELDS = {
    "min_items": "min_length",
    "max_items": "max_length",
    "regex": "pattern",
    "allow_mutation": "-frozen",
    "metadata": "json_schema_extra",
}

V2_FIELDS_TO_V1_FIELDS = {}
for k, v in V1_FIELDS_TO_V2_FIELDS.items():
    if v.startswith("-"):
        v = v[1:]
        k = f"-{k}"
    V2_FIELDS_TO_V1_FIELDS[v] = k

FIELD_NAME_MAP = V1_FIELDS_TO_V2_FIELDS if PYDANTIC2 else V2_FIELDS_TO_V1_FIELDS


def check_mixin_order(cls: type, mixin_class: type, base_model: type) -> None:
    """Warn if mixin_class appears after base_model in cls.__bases__."""
    bases = cls.__bases__
    with contextlib.suppress(ValueError):
        mixin_index = bases.index(mixin_class)
        base_model_index = bases.index(base_model)
        if mixin_index > base_model_index:
            warnings.warn(
                f"{mixin_class.__name__} should appear before pydantic.BaseModel",
                stacklevel=3,
            )


def move_field_kwargs(kwargs: dict) -> dict:
    """Move Field(...) kwargs from v1 to v2 and vice versa."""
    for old_name, new_name in FIELD_NAME_MAP.items():
        negate = False
        if new_name.startswith("-"):
            new_name = new_name[1:]
            negate = True
        if old_name in kwargs:
            if new_name in kwargs:
                raise ValueError(f"Cannot specify both {old_name} and {new_name}")
            val = not kwargs.pop(old_name) if negate else kwargs.pop(old_name)
            kwargs[new_name] = val
    return kwargs


def clean_field_kwargs(kwargs: dict) -> dict:
    """Remove outdated Field(...) kwargs."""
    const = kwargs.pop("const", None)
    if const is not None:
        raise TypeError(
            f"`const` is removed in v2, use `Literal[{const!r}]` instead, "
            "it works in v1 and v2."
        )
    return kwargs


def Field(*args: Any, **kwargs: Any) -> Any:
    """Create a field for objects that can be configured."""
    kwargs = clean_field_kwargs(kwargs)
    kwargs = move_field_kwargs(kwargs)
    return pydantic.Field(*args, **kwargs)
