import pydantic
import pytest

from pydantic_compat import PydanticCompatMixin


def test_v1_methods():
    class Model(PydanticCompatMixin, pydantic.BaseModel):
        x: int = 1

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


def test_v2_methods():
    class Model(PydanticCompatMixin, pydantic.BaseModel):
        x: int = 1

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


def test_mixin_order():
    with pytest.warns(
        match="PydanticCompatMixin should appear before pydantic.BaseModel"
    ):

        class Model1(pydantic.BaseModel, PydanticCompatMixin):
            x: int = 1

    class Model2(PydanticCompatMixin, pydantic.BaseModel):
        x: int = 1
