from __future__ import annotations

import warnings
from typing import Any, Callable

from pydantic.deprecated import class_validators


# V1 signature
# def validator(
#     *fields: str,
#     pre: bool = False,
#     each_item: bool = False,
#     always: bool = False,
#     check_fields: bool = True,
#     whole: Optional[bool] = None,
#     allow_reuse: bool = False,
# ) -> Callable[[AnyCallable], 'AnyClassMethod']:
#     ...
def validator(
    _field: str, *fields: str, **kwargs: Any
) -> Callable[[Callable], Callable]:
    """Adaptor from v1.validator -> v2.field_validator."""
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", DeprecationWarning)
        return class_validators.validator(_field, *fields, **kwargs)


# V1 signature
# def root_validator(
#     _func: Optional[AnyCallable] = None,
#     *,
#     pre: bool = False,
#     allow_reuse: bool = False,
#     skip_on_failure: bool = False,
# ) -> Union["AnyClassMethod", Callable[[AnyCallable], "AnyClassMethod"]]:
#     ...
def root_validator(
    *_args: str,
    pre: bool = False,
    skip_on_failure: bool | None = None,
    allow_reuse: bool = False,
    construct_object: bool = False,  # here to match our v1 patch behavior
) -> Any:
    """Adaptor from v1.root_validator -> v2.model_validator."""
    # If you use `@root_validator` with pre=False (the default)
    # you MUST specify `skip_on_failure=True`
    # we let explicit `skip_on_failure=False` pass through to fail,
    # but we default to `skip_on_failure=True` to match v1 behavior
    if not pre and skip_on_failure is None:
        skip_on_failure = True

    if construct_object:
        raise ValueError(
            "construct_object=True is not supported by pydantic-compat when running on "
            "pydantic v2. Please use pydantic_compat.model_validator(mode='after') "
            "instead. (It works for both versions)."
        )

    with warnings.catch_warnings():
        warnings.simplefilter("ignore", DeprecationWarning)

        # def model_validator( *, mode: Literal['wrap', 'before', 'after']) -> Any:
        return class_validators.root_validator(  # type: ignore [call-overload]
            *_args,
            pre=pre,
            skip_on_failure=bool(skip_on_failure),
            allow_reuse=allow_reuse,
        )
