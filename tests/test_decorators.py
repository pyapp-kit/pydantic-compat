from unittest.mock import Mock

import pydantic
import pytest

from pydantic_compat import (
    PYDANTIC2,
    PydanticCompatMixin,
    field_validator,
    model_validator,
    root_validator,
    validator,
)


def test_v1_validator():
    mock_before = Mock()
    mock_after = Mock()

    class Model(PydanticCompatMixin, pydantic.BaseModel):
        x: int = 1

        @validator("x", pre=True)
        def _validate_x_before(cls, v):
            mock_before(v)
            return v

        @validator("x")
        def _validate_x_after(cls, v):
            mock_after(v)
            return v

    m = Model(x="2")
    mock_before.assert_called_once_with("2")
    mock_after.assert_called_once_with(2)
    assert m.x == 2


def test_v2_field_validator():
    mock_before = Mock()
    mock_after = Mock()

    class Model(PydanticCompatMixin, pydantic.BaseModel):
        x: int = 1

        @field_validator("x", mode="before")
        def _validate_x_before(cls, v):
            mock_before(v)
            return v

        @field_validator("x", mode="after")
        def _validate_x_after(cls, v):
            mock_after(v)
            return v

    m = Model(x="2")
    mock_before.assert_called_once_with("2")
    mock_after.assert_called_once_with(2)
    assert m.x == 2


def test_v1_root_validator():
    mock_before = Mock()
    mock_after = Mock()

    class Model(PydanticCompatMixin, pydantic.BaseModel):
        x: int = 1

        @root_validator(pre=True)
        def _validate_x_before(cls, v):
            mock_before(v)
            return v

        @root_validator(pre=False)
        def _validate_x_after(cls, v):
            mock_after(v)
            return v

    m = Model(x="2")
    mock_before.assert_called_once_with({"x": "2"})
    mock_after.assert_called_once_with({"x": 2})
    assert m.x == 2


@pytest.mark.xfail(PYDANTIC2, reason="not supported in pydantic v2", strict=True)
def test_v1_root_validator_with_construct():
    """Test the construct_object parameter of root_validator.

    This converts the input dict to the model object before calling the validator.
    To match the v2 behavior.  It's not supported when running on v2.  For that, just
    use model_validator(mode='after').
    """
    mock_after2 = Mock()

    class Model(PydanticCompatMixin, pydantic.BaseModel):
        x: int = 1

        @root_validator(pre=False, construct_object=True)
        def _validate_x_after2(cls, values):
            assert isinstance(values, Model)
            mock_after2(values.x)
            return values

    m = Model(x="2")
    mock_after2.assert_called_once_with(2)
    assert m.x == 2


def test_v2_model_validator():
    mock_before = Mock()
    mock_after = Mock()

    class Model(PydanticCompatMixin, pydantic.BaseModel):
        x: int = 1

        @model_validator(mode="before")
        def _validate_x_before(cls, v):
            mock_before(v)
            return v

        @model_validator(mode="after")
        def _validate_x_after(cls, v):
            mock_after(v)
            return v

    m = Model(x="2")
    mock_before.assert_called_once_with({"x": "2"})
    mock_after.assert_called_once_with(m)
    assert m.x == 2
