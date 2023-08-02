from __future__ import annotations

from functools import wraps
from typing import TYPE_CHECKING, Any, Callable

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
        pre=(mode in ("before")),
        always=True,  # should it be?
        check_fields=bool(check_fields),
        allow_reuse=True,
    )


# V2 signature
def model_validator(*, mode: Literal["wrap", "before", "after"]) -> Any:
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
    return root_validator(
        pre=mode == "before", allow_reuse=True, construct_object=mode == "after"
    )


def root_validator(
    _func: Callable | None = None,
    *,
    pre: bool = False,
    allow_reuse: bool = False,
    skip_on_failure: bool = False,
    construct_object: bool = False,
) -> Any:
    def _inner(_func: Callable) -> Any:
        func = _func
        if construct_object and not pre:
            if isinstance(_func, classmethod):
                _func = _func.__func__

            @wraps(_func)
            def func(cls: type[pydantic.BaseModel], *args: Any, **kwargs: Any) -> Any:
                arg0, *rest = args
                # cast dict to model to match the v2 model_validator signature
                # using construct because it should already be valid
                new_args = (cls.construct(**arg0), *rest)
                result: pydantic.BaseModel = _func(cls, *new_args, **kwargs)
                # cast back to dict of field -> value
                return {k: getattr(result, k) for k in result.__fields__}

        deco = pydantic.root_validator(  # type: ignore [call-overload]
            pre=pre, allow_reuse=allow_reuse, skip_on_failure=skip_on_failure
        )
        return deco(func)

    return _inner(_func) if _func else _inner
