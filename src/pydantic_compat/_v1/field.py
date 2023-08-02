import pydantic

from pydantic_compat._shared import _clean_field_kwargs


def Field(*args, **kwargs):
    kwargs = _clean_field_kwargs(kwargs)

    # renames
    min_length = kwargs.pop("min_length", None)
    if min_length is not None:
        kwargs.setdefault("min_items", min_length)
    max_length = kwargs.pop("max_length", None)
    if max_length is not None:
        kwargs.setdefault("max_items", max_length)
    frozen = kwargs.pop("frozen", None)
    if frozen is True:
        kwargs.setdefault("allow_mutation", False)

    return pydantic.Field(*args, **kwargs)
