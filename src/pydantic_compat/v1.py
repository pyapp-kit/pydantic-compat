try:
    from pydantic.v1 import *  # noqa
except ImportError:
    from pydantic import *  # type: ignore # noqa
