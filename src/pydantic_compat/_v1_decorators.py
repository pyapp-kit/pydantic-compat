from __future__ import annotations

from functools import wraps
from typing import TYPE_CHECKING, Callable

import pydantic.version

if not pydantic.version.VERSION.startswith("1"):
    raise ImportError("pydantic_compat._v1 only supports pydantic v1.x")

import pydantic

if TYPE_CHECKING:
    from typing import Literal


# V2 signature
def field_validator(
    _field: str,
    *fields: str,
    mode: Literal["before", "after", "wrap", "plain"] = "after",
    check_fields: bool | None = None,
) -> Callable:
    """Adaptor from v2.field_validator -> v1.validator."""
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
    return pydantic.validator(
        _field,
        *fields,
        check_fields=bool(check_fields),
        pre=(mode in ("before")),
        allow_reuse=True,
    )


# V2 signature
def model_validator(*, mode: Literal["wrap", "before", "after"]) -> Callable:
    """Adaptor from v2.model_validator -> v1.root_validator."""

    # V1 signature
    # def root_validator(
    #     _func: Optional[AnyCallable] = None,
    #     *,
    #     pre: bool = False,
    #     allow_reuse: bool = False,
    #     skip_on_failure: bool = False,
    # ) -> Union["AnyClassMethod", Callable[[AnyCallable], "AnyClassMethod"]]:
    #     ...
    pre = mode == "before"
    return pydantic.root_validator(pre=pre, allow_reuse=True)


def root_validator(
    _func: Callable | None = None,
    *,
    pre: bool = False,
    allow_reuse: bool = False,
    skip_on_failure: bool = False,
    construct_object: bool = False,
) -> Callable:
    def _inner(_func: Callable):
        func = _func
        if construct_object and not pre:

            @wraps(_func)
            def func(cls, *args, **kwargs):
                arg0, *rest = args
                new_args = (cls.construct(**arg0), *rest)
                result = _func(cls, *new_args, **kwargs)
                return result.dict()

        return pydantic.root_validator(
            func, pre=pre, allow_reuse=allow_reuse, skip_on_failure=skip_on_failure
        )

    return _inner(_func) if _func else _inner
