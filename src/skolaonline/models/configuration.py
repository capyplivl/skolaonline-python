from __future__ import annotations

from dataclasses import dataclass
from typing import ClassVar

from skolaonline.models._base import SkolaOnlineModel


@dataclass(kw_only=True)
class MinAppVersion(SkolaOnlineModel):
    """Minimum supported versions of the mobile app."""

    _field_aliases: ClassVar[dict[str, str]] = {
        "ios": "iOS",
    }

    ios: str | None = None
    """Minimum supported version of the iOS app."""

    android: str | None = None
    """Minimum supported version of the Android app."""
