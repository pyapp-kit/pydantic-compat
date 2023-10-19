from typing import ClassVar

import pydantic
import pytest

from pydantic_compat import PydanticCompatMixin


class Model(PydanticCompatMixin, pydantic.BaseModel):
    x: int = 1


def test_v1_api():
    m = Model()
    assert m.x == 1
    assert m.dict() == {"x": 1}
    assert m.json().replace(" ", "") == '{"x":1}'
    assert m.copy() == m

    assert Model.parse_raw('{"x": 2}') == Model(x=2)
    assert Model.parse_obj({"x": 2}) == Model(x=2)
    assert Model.construct(x=2) == Model(x=2)
    assert Model.validate({"x": 2}) == Model(x=2)
    assert Model.schema() == {
        "title": "Model",
        "type": "object",
        "properties": {
            "x": {"title": "X", "type": "integer", "default": 1},
        },
    }

    Model.update_forward_refs(name="name")


def test_v2_api():
    m = Model()
    assert m.x == 1
    assert m.model_dump() == {"x": 1}
    assert m.model_dump_json().replace(" ", "") == '{"x":1}'
    assert m.model_copy() == m

    assert Model.model_validate_json('{"x": 2}') == Model(x=2)
    assert Model.model_validate({"x": 2}) == Model(x=2)
    assert Model.model_construct(x=2) == Model(x=2)
    assert Model.model_validate({"x": 2}) == Model(x=2)
    assert Model.model_json_schema() == {
        "title": "Model",
        "type": "object",
        "properties": {
            "x": {"title": "X", "type": "integer", "default": 1},
        },
    }
    Model.model_rebuild(force=True)


def test_v1_attributes():
    m = Model()
    assert "x" in m.__fields__
    assert "x" in Model.__fields__
    assert "x" not in m.__fields_set__
    m.x = 2
    assert "x" in m.__fields_set__


def test_v2_attributes():
    m = Model()
    assert "x" in m.model_fields
    assert "x" in Model.model_fields
    assert "x" not in m.model_fields_set
    m.x = 2
    assert "x" in m.model_fields_set


def test_mixin_order():
    with pytest.warns(
        match="PydanticCompatMixin should appear before pydantic.BaseModel"
    ):

        class Model1(pydantic.BaseModel, PydanticCompatMixin):
            x: int = 1

    class Model2(PydanticCompatMixin, pydantic.BaseModel):
        x: int = 1


V2Config = {"populate_by_name": True, "extra": "forbid", "frozen": True}


class V1Config:
    allow_population_by_field_name = True
    extra = "forbid"
    frozen = True
    json_encoders: ClassVar[dict] = {}


@pytest.mark.parametrize("config", [V1Config, V2Config])
def test_config(config):
    class Model1(PydanticCompatMixin, pydantic.BaseModel):
        name: str = pydantic.Field(alias="full_name")

    # to make sure that populate_by_name is working
    with pytest.raises((ValueError, TypeError)):  # (v1, v2)
        m = Model1(name="John")

    class Model(PydanticCompatMixin, pydantic.BaseModel):
        name: str = pydantic.Field(alias="full_name")
        if isinstance(config, dict):
            model_config = config
        else:
            Config = config

    m = Model(name="John")

    # test frozen
    with pytest.raises((ValueError, TypeError)):  # (v1, v2)
        m.name = "Sue"

    # test extra
    with pytest.raises((ValueError, TypeError)):  # (v1, v2)
        Model(extra=1)
