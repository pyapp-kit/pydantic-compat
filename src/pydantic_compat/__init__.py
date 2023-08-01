"""CompatibilityMixin for pydantic v1/1/v2."""

try:
    from importlib.metadata import PackageNotFoundError, version
except ImportError:
    from importlib_metadata import PackageNotFoundError, version

from typing import TYPE_CHECKING

try:
    __version__ = version("pydantic-compat")
except PackageNotFoundError:  # pragma: no cover
    __version__ = "uninstalled"

__author__ = "Talley Lambert"
__email__ = "talley.lambert@gmail.com"
__all__ = [
    "__version__",
    "field_validator",
    "model_validator",
    "PYDANTIC2",
    "PydanticCompatMixin",
    "root_validator",
    "validator",
]

from ._shared import PYDANTIC2

if TYPE_CHECKING:
    from pydantic import field_validator, model_validator, root_validator, validator

    from ._v2_mixin import PydanticCompatMixin

elif PYDANTIC2:
    from pydantic import field_validator, model_validator

    from ._v2_decorators import root_validator, validator
    from ._v2_mixin import PydanticCompatMixin

else:
    from pydantic import validator  # type: ignore

    from ._v1_decorators import (  # type: ignore
        field_validator,
        model_validator,
        root_validator,
    )
    from ._v1_mixin import PydanticCompatMixin  # type: ignore
