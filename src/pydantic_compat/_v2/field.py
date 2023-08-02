import pydantic

from pydantic_compat._shared import _clean_field_kwargs

# unique_items = extra.pop("unique_items", None)  # type: ignore
# if unique_items is not None:
#     raise PydanticUserError(
#         (
#             "`unique_items` is removed, use `Set` instead"
#             "(this feature is discussed in https://github.com/pydantic/pydantic-core/issues/296)"
#         ),
#         code="removed-kwargs",
#     )
# regex = extra.pop("regex", None)  # type: ignore
# if regex is not None:
#     raise PydanticUserError(
#         "`regex` is removed. use `pattern` instead", code="removed-kwargs"
#     )


def Field(*args, **kwargs):
    kwargs = _clean_field_kwargs(kwargs)

    # renames
    min_items = kwargs.pop("min_items", None)
    if min_items is not None:
        kwargs.setdefault("min_length", min_items)
    max_items = kwargs.pop("max_items", None)
    if max_items is not None:
        kwargs.setdefault("max_length", max_items)
    allow_mutation = kwargs.pop("allow_mutation", None)
    if allow_mutation is False:
        kwargs.setdefault("frozen", True)

    return pydantic.Field(*args, **kwargs)
