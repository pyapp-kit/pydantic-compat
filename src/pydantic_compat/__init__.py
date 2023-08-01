"""CompatibilityMixin for pydantic v1/1/v2."""
from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("pydantic-compat")
except PackageNotFoundError:
    __version__ = "uninstalled"

__author__ = "Talley Lambert"
__email__ = "talley.lambert@gmail.com"
__all__ = ["PydanticCompatMixin", "__version__", "PYDANTIC2"]

from ._shared import PYDANTIC2

if PYDANTIC2:
    from ._v2 import PydanticCompatMixin
else:
    from ._v1 import PydanticCompatMixin  # type: ignore
