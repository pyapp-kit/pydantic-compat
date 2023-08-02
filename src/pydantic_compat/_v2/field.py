import pydantic

from pydantic_compat._shared import clean_field_kwargs, move_field_kwargs

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
    kwargs = clean_field_kwargs(kwargs)
    kwargs = move_field_kwargs(kwargs)
    return pydantic.Field(*args, **kwargs)
