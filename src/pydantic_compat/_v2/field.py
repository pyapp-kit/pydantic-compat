from typing import Any

import pydantic

from pydantic_compat._shared import clean_field_kwargs, move_field_kwargs


def Field(*args: Any, **kwargs: Any) -> Any:
    kwargs = clean_field_kwargs(kwargs)
    kwargs = move_field_kwargs(kwargs)
    return pydantic.Field(*args, **kwargs)
