from __future__ import annotations

from skolaonline.models import (
    EmergencyMultiNotificationRequest,
    NotificationGroups,
    NotificationResponse,
    SavePreferencesRequest,
    SimpleMultiNotificationRequest,
    TwoFactorMultiNotificationRequest,
)
from skolaonline.resources._base import (
    AsyncAPIResource,
    SyncAPIResource,
    parse_model,
    parse_model_list,
)


class Notifications(SyncAPIResource):
    def retrieve_preferences(
        self, *, student_id: str | None = None
    ) -> NotificationGroups:
        """Return the notification preferences of the user."""
        response = self._request(
            "GET", "/api/v1/notifications/preferences", params={"studentId": student_id}
        )
        return parse_model(response, NotificationGroups)

    def save_preferences(self, body: SavePreferencesRequest) -> None:
        """Save the notification preferences of the user."""
        self._request("POST", "/api/v1/notifications/preferences", json=body.to_dict())

    def send(self, body: SimpleMultiNotificationRequest) -> list[NotificationResponse]:
        """Send general Firebase notifications."""
        response = self._request("POST", "/api/v1/notifications", json=body.to_dict())
        return parse_model_list(response, NotificationResponse)

    def send_emergency(
        self, body: EmergencyMultiNotificationRequest
    ) -> list[NotificationResponse]:
        """Send emergency Firebase notifications."""
        response = self._request(
            "POST", "/api/v1/notifications/emergency", json=body.to_dict()
        )
        return parse_model_list(response, NotificationResponse)

    def send_two_factor(
        self, body: TwoFactorMultiNotificationRequest
    ) -> list[NotificationResponse]:
        """Send two-factor authentication Firebase notifications."""
        response = self._request(
            "POST", "/api/v1/notifications/2fa", json=body.to_dict()
        )
        return parse_model_list(response, NotificationResponse)


class AsyncNotifications(AsyncAPIResource):
    async def retrieve_preferences(
        self, *, student_id: str | None = None
    ) -> NotificationGroups:
        """Return the notification preferences of the user."""
        response = await self._request(
            "GET", "/api/v1/notifications/preferences", params={"studentId": student_id}
        )
        return parse_model(response, NotificationGroups)

    async def save_preferences(self, body: SavePreferencesRequest) -> None:
        """Save the notification preferences of the user."""
        await self._request(
            "POST", "/api/v1/notifications/preferences", json=body.to_dict()
        )

    async def send(
        self, body: SimpleMultiNotificationRequest
    ) -> list[NotificationResponse]:
        """Send general Firebase notifications."""
        response = await self._request(
            "POST", "/api/v1/notifications", json=body.to_dict()
        )
        return parse_model_list(response, NotificationResponse)

    async def send_emergency(
        self, body: EmergencyMultiNotificationRequest
    ) -> list[NotificationResponse]:
        """Send emergency Firebase notifications."""
        response = await self._request(
            "POST", "/api/v1/notifications/emergency", json=body.to_dict()
        )
        return parse_model_list(response, NotificationResponse)

    async def send_two_factor(
        self, body: TwoFactorMultiNotificationRequest
    ) -> list[NotificationResponse]:
        """Send two-factor authentication Firebase notifications."""
        response = await self._request(
            "POST", "/api/v1/notifications/2fa", json=body.to_dict()
        )
        return parse_model_list(response, NotificationResponse)
