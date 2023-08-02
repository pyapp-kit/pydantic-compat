import contextlib
import warnings

from pydantic import version

PYDANTIC2 = version.VERSION.startswith("2")

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


def _check_mixin_order(cls: type, mixin_class: type, base_model: type) -> None:
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


def _clean_field_kwargs(kwargs: dict) -> dict:
    const = kwargs.pop("const", None)
    if const is not None:
        raise TypeError(
            f"`const` is removed in v2, use `Literal[{const!r}]` instead, "
            "it works in v1 and v2."
        )
    return kwargs
