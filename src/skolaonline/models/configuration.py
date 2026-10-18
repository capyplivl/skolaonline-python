from __future__ import annotations

from dataclasses import dataclass
from typing import ClassVar

from skolaonline.models._base import SkolaOnlineModel


@dataclass(kw_only=True)
class MinAppVersion(SkolaOnlineModel):
    _field_aliases: ClassVar[dict[str, str]] = {
        "i_os": "iOS",
    }

    i_os: str | None = None
    android: str | None = None
