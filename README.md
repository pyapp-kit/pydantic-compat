# pydantic-compat

[![GitHub](https://img.shields.io/github/license/pyapp-kit/pydantic-compat)
](https://github.com/pyapp-kit/pydantic-compat/raw/main/LICENSE)
[![PyPI](https://img.shields.io/pypi/v/pydantic-compat.svg?color=green)](https://pypi.org/project/pydantic-compat)
[![Python Version](https://img.shields.io/pypi/pyversions/pydantic-compat.svg?color=green)](https://python.org)
[![CI](https://github.com/pyapp-kit/pydantic-compat/actions/workflows/ci.yml/badge.svg)](https://github.com/pyapp-kit/pydantic-compat/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/pyapp-kit/pydantic-compat/branch/main/graph/badge.svg)](https://codecov.io/gh/pyapp-kit/pydantic-compat)

## Motivation

Pydantic 2 was a major release that completely changed the pydantic API.

For applications, this is not a big deal, as they can pin to whatever version of
pydantic they need. But for libraries that want to exist in a broader
environment, pinning to a specific version of pydantic is not always an option
(as it limits the ability to co-exist with other libraries).

This package provides (unofficial) compatibility mixins and function adaptors for pydantic
v1-v2 cross compatibility. It allows you to use either v1 or v2 API names,
regardless of the pydantic version installed. (Prefer using v2 names when possible).

Tests are run on Pydantic v1.8 and up

The API conversion is not exhaustive, but suffices for many of the use cases
I have come across. It is in use by the following libraries:

- [ome-types](https://github.com/tlambert03/ome-types)
- [app-model](https://github.com/pyapp-kit/app-model)
- [useq-schema](https://github.com/pymmcore-plus/useq-schema)

Feel free to open an issue or PR if you find it useful, but lacking features
you need.

## What does it do?

Not much! :joy:

Mostly it serves to translate names from one API to another. It backports
the v2 API to v1 (so you can v2 names in a pydantic1 runtime),
and forwards the v1 API to v2 (so you can use v1 names in a v2 runtime
without deprecation warnings).

> While pydantic2 does offer deprecated access to the v1 API, if you explicitly
> wish to support pydantic1 without your users seeing deprecation warnings,
> then you need to do a lot of name adaptation depending on the runtime
> pydantic version. This package does that for you.

It does _not_ do any significantly complex translation of API logic.
For custom types, you will still likely need to add class methods to
support both versions of pydantic.

It also does not prevent you from needing to know a what's changing
under the hood in pydantic 2. You should be running tests on both
versions of pydantic to ensure your library works as expected. This
library just makes it much easier to support both versions in a single
codebase without a lot of ugly conditionals and boilerplate.

## Usage

```py
from pydantic import BaseModel
from pydantic_compat import PydanticCompatMixin
from pydantic_compat import field_validator  # or 'validator'
from pydantic_compat import model_validator  # or 'root_validator'

class MyModel(PydanticCompatMixin, BaseModel):
    x: int
    y: int = 2

    # prefer v2 dict, but v1 class Config is supported
    model_config = {'frozen': True}

    @field_validator('x', mode='after')
    def _check_x(cls, v):
        if v != 42:
            raise ValueError("That's not the answer!")
        return v

    @model_validator('x', mode='after')
    def _check_x(cls, v: MyModel):
        # ...
        return v
```

You can now use the following attributes and methods regardless of the
pydantic version installed (without deprecation warnings):

| v1 name                     | v2 name                     |
| --------------------------- | --------------------------- |
| `obj.dict()`                | `obj.model_dump()`          |
| `obj.json()`                | `obj.model_dump_json()`     |
| `obj.copy()`                | `obj.model_copy()`          |
| `Model.construct`           | `Model.model_construct`     |
| `Model.schema`              | `Model.model_json_schema`   |
| `Model.validate`            | `Model.model_validate`      |
| `Model.parse_obj`           | `Model.model_validate`      |
| `Model.parse_raw`           | `Model.model_validate_json` |
| `Model.update_forward_refs` | `Model.model_rebuild`       |
| `Model.__fields__`          | `Model.model_fields`        |
| `Model.__fields_set__`      | `Model.model_fields_set`    |


## `Field` notes

- `pydantic_compat.Field` will remove outdated fields (`const`) and translate
  fields with new names:
  | v1 name          | v2 name             |
  | ---------------- | ------------------- |
  | `min_items`      | `min_length`        |
  | `max_items`      | `max_length`        |
  | `regex`          | `pattern`           |
  | `allow_mutation` | `not frozen`        |
  | `<extra_key>`       | `json_schema_extra['<extra_key>']` |
- Don't use `var = Field(..., const='val')`, use `var: Literal['val'] = 'val'`
  it works in both v1 and v2
- No attempt is made to convert between v1's `unique_items` and v2's `Set[]`
  semantics. See <https://github.com/pydantic/pydantic-core/issues/296> for
  discussion.

## API rules

- both V1 and V2 names may be used (regardless of pydantic version), but
  usage of V2 names are strongly recommended.
- But the API must match the pydantic version matching the name you are using.
  For example, if you are using `pydantic_compat.field_validator` then the
  signature must match the pydantic (v2) `field_validator` signature (regardless)
  of the pydantic version installed. Similarly, if you choose to use
  `pydantic_compat.validator` then the signature must match the pydantic
  (v1) `validator` signature.

## Notable differences

- `BaseModel.__fields__` in v1 is a dict of `{'field_name' -> ModelField}`
  whereas in v2 `BaseModel.model_fields` is a dict of `{'field_name' ->
FieldInfo}`. `FieldInfo` is a much simpler object that ModelField, so it is
  difficult to directly support complicated v1 usage of `__fields__`.
  `pydantic-compat` simply provides a name addaptor that lets you access many of
  the attributes you may have accessed on `ModelField` in v1 while operating in
  a v2 world, but `ModelField` methods will not be made available. You'll need
  to update your usage accordingly.

- in V2, `pydantic.model_validator(..., mode='after')` passes a model _instance_
  to the validator function, whereas `pydantic.v1.root_validator(...,
pre=False)` passes a dict of `{'field_name' -> validated_value}` to the
  validator function. In pydantic-compat, both decorators follow the semantics
  of their corresponding pydantic versions, _but_ `root_validator` gains
  parameter `construct_object: bool=False` that matches the `model_validator`
  behavior (only when `mode=='after'`). If you want that behavior though, prefer
  using `model_validator` directly.

## TODO:

- Serialization decorators
