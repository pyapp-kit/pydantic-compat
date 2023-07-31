import contextlib
import warnings


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
