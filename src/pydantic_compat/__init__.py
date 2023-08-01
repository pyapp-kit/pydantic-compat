"""CompatibilityMixin for pydantic v1/1/v2."""
from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("pydantic-compat")
except PackageNotFoundError:
    __version__ = "uninstalled"

__author__ = "Talley Lambert"
__email__ = "talley.lambert@gmail.com"
__all__ = [
    "PydanticCompatMixin",
    "__version__",
    "PYDANTIC2",
    "field_validator",
    "validator",
    "model_validator",
    "root_validator",
]

from ._shared import PYDANTIC2

# if not TYPE_CHECKING:
if PYDANTIC2:
    from pydantic import field_validator, model_validator

    from ._v2 import PydanticCompatMixin
    from ._v2_decorators import root_validator, validator

else:
    from pydantic import validator  # type: ignore

    from ._v1 import PydanticCompatMixin  # type: ignore
    from ._v1_decorators import (  # type: ignore
        field_validator,
        model_validator,
        root_validator,
    )
