from __future__ import annotations

import dataclasses
import types
import typing
from collections.abc import Mapping
from datetime import datetime
from enum import Enum
from typing import Any, ClassVar, Self, get_args, get_origin, get_type_hints

from skolaonline._serialization import parse_datetime


def to_camel_case(name: str) -> str:
    head, *tail = name.split("_")
    return head + "".join(part[:1].upper() + part[1:] for part in tail)


def _unwrap_optional(tp: Any) -> Any:
    if get_origin(tp) in (types.UnionType, typing.Union):
        members = [arg for arg in get_args(tp) if arg is not type(None)]
        if len(members) == 1:
            return members[0]
    return tp


def _coerce(value: Any, target: Any) -> Any:
    if value is None or target is Any:
        return value
    target = _unwrap_optional(target)
    origin = get_origin(target)
    if origin is list:
        if not isinstance(value, list):
            return value
        (item_type,) = get_args(target)
        return [_coerce(item, item_type) for item in value]
    if origin is dict:
        if not isinstance(value, dict):
            return value
        _, value_type = get_args(target)
        return {key: _coerce(item, value_type) for key, item in value.items()}
    if not isinstance(target, type):
        return value
    if issubclass(target, SkolaOnlineModel):
        return target.from_dict(value) if isinstance(value, Mapping) else value
    if issubclass(target, Enum):
        try:
            return target(value)
        except ValueError:
            return value
    if target is datetime:
        return parse_datetime(value) if isinstance(value, str) else value
    if target is float and isinstance(value, int) and not isinstance(value, bool):
        return float(value)
    return value


def _serialize(value: Any) -> Any:
    if isinstance(value, SkolaOnlineModel):
        return value.to_dict()
    if isinstance(value, Enum):
        return value.value
    if isinstance(value, datetime):
        return value.isoformat()
    if isinstance(value, list):
        return [_serialize(item) for item in value]
    if isinstance(value, dict):
        return {key: _serialize(item) for key, item in value.items()}
    return value


@dataclasses.dataclass(frozen=True)
class _FieldSpec:
    name: str
    key: str
    type: Any
    required: bool
    omit_none: bool


_FIELD_SPECS: dict[type, tuple[_FieldSpec, ...]] = {}


def _field_specs(cls: type[SkolaOnlineModel]) -> tuple[_FieldSpec, ...]:
    specs = _FIELD_SPECS.get(cls)
    if specs is None:
        hints = get_type_hints(cls)
        aliases = cls._field_aliases
        specs = tuple(
            _FieldSpec(
                name=field.name,
                key=aliases.get(field.name, to_camel_case(field.name)),
                type=hints[field.name],
                required=field.default is dataclasses.MISSING
                and field.default_factory is dataclasses.MISSING,
                omit_none=field.default is None,
            )
            for field in dataclasses.fields(cls)  # type: ignore[arg-type]
        )
        _FIELD_SPECS[cls] = specs
    return specs


class SkolaOnlineModel:
    _field_aliases: ClassVar[dict[str, str]] = {}

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> Self:
        kwargs: dict[str, Any] = {}
        for spec in _field_specs(cls):
            if spec.key in data:
                kwargs[spec.name] = _coerce(data[spec.key], spec.type)
            elif spec.required:
                kwargs[spec.name] = None
        return cls(**kwargs)

    def to_dict(self) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for spec in _field_specs(type(self)):
            value = getattr(self, spec.name)
            if value is None and spec.omit_none:
                continue
            result[spec.key] = _serialize(value)
        return result
