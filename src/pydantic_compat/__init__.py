"""CompatibilityMixin for pydantic v1/1/v2"""
from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("pydantic-compat")
except PackageNotFoundError:
    __version__ = "uninstalled"

__author__ = "Talley Lambert"
__email__ = "talley.lambert@gmail.com"
