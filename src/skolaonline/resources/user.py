from __future__ import annotations

from typing import Any

from skolaonline.models import (
    ChangePasswordRequest,
    NotificationOffRequest,
    NotificationsResponse,
    PasswordRequirementsResponse,
    PostFeedbackRequest,
    UserInfoResponse,
)
from skolaonline.resources._base import (
    AsyncAPIResource,
    SyncAPIResource,
    parse_json,
    parse_model,
)


class User(SyncAPIResource):
    def retrieve(self) -> UserInfoResponse:
        """Return information about the signed-in user."""
        response = self._request("GET", "/api/v1/user")
        return parse_model(response, UserInfoResponse)

    def logout(self) -> None:
        """Sign the user out."""
        self._request("GET", "/api/v1/user/logout")

    def list_notifications(self) -> NotificationsResponse:
        """Return the number of unprocessed records per module."""
        response = self._request("GET", "/api/v1/user/notifications")
        return parse_model(response, NotificationsResponse)

    def enable_notifications(self, fcm_token: str) -> Any:
        """Enable mobile push notifications for a Firebase token."""
        response = self._request("POST", "/api/v1/user/notifications", json=fcm_token)
        return parse_json(response)

    def disable_notifications(self, body: NotificationOffRequest) -> Any:
        """Disable mobile push notifications for a Firebase token."""
        response = self._request(
            "DELETE", "/api/v1/user/notifications", json=body.to_dict()
        )
        return parse_json(response)

    def retrieve_dashboard(
        self,
        *,
        number_of_apologies: int,
        number_of_messages: int,
        child_id: str | None = None,
    ) -> Any:
        """Return dashboard data with unprocessed record counts per module."""
        response = self._request(
            "GET",
            "/api/v1/user/dashboardData",
            params={
                "NumberOfApologies": number_of_apologies,
                "NumberOfMessages": number_of_messages,
            },
            headers={"api-ChildId": child_id},
        )
        return parse_json(response)

    def notifications_exist(self, *, fcm_token: str) -> Any:
        """Check whether a Firebase token is registered for notifications."""
        response = self._request(
            "GET", "/api/v1/user/notificationsExist", params={"fcmToken": fcm_token}
        )
        return parse_json(response)

    def retrieve_password_requirements(self) -> PasswordRequirementsResponse:
        """Return the password requirements of the organization."""
        response = self._request("GET", "/api/v1/user/passwordRequirements")
        return parse_model(response, PasswordRequirementsResponse)

    def send_feedback(self, body: PostFeedbackRequest) -> None:
        """Send feedback by email to the application operator."""
        self._request("POST", "/api/v1/user/feedback", json=body.to_dict())

    def change_password(self, body: ChangePasswordRequest) -> None:
        """Change the password of the signed-in user."""
        self._request("POST", "/api/v1/user/changePassword", json=body.to_dict())


class AsyncUser(AsyncAPIResource):
    async def retrieve(self) -> UserInfoResponse:
        """Return information about the signed-in user."""
        response = await self._request("GET", "/api/v1/user")
        return parse_model(response, UserInfoResponse)

    async def logout(self) -> None:
        """Sign the user out."""
        await self._request("GET", "/api/v1/user/logout")

    async def list_notifications(self) -> NotificationsResponse:
        """Return the number of unprocessed records per module."""
        response = await self._request("GET", "/api/v1/user/notifications")
        return parse_model(response, NotificationsResponse)

    async def enable_notifications(self, fcm_token: str) -> Any:
        """Enable mobile push notifications for a Firebase token."""
        response = await self._request(
            "POST", "/api/v1/user/notifications", json=fcm_token
        )
        return parse_json(response)

    async def disable_notifications(self, body: NotificationOffRequest) -> Any:
        """Disable mobile push notifications for a Firebase token."""
        response = await self._request(
            "DELETE", "/api/v1/user/notifications", json=body.to_dict()
        )
        return parse_json(response)

    async def retrieve_dashboard(
        self,
        *,
        number_of_apologies: int,
        number_of_messages: int,
        child_id: str | None = None,
    ) -> Any:
        """Return dashboard data with unprocessed record counts per module."""
        response = await self._request(
            "GET",
            "/api/v1/user/dashboardData",
            params={
                "NumberOfApologies": number_of_apologies,
                "NumberOfMessages": number_of_messages,
            },
            headers={"api-ChildId": child_id},
        )
        return parse_json(response)

    async def notifications_exist(self, *, fcm_token: str) -> Any:
        """Check whether a Firebase token is registered for notifications."""
        response = await self._request(
            "GET", "/api/v1/user/notificationsExist", params={"fcmToken": fcm_token}
        )
        return parse_json(response)

    async def retrieve_password_requirements(self) -> PasswordRequirementsResponse:
        """Return the password requirements of the organization."""
        response = await self._request("GET", "/api/v1/user/passwordRequirements")
        return parse_model(response, PasswordRequirementsResponse)

    async def send_feedback(self, body: PostFeedbackRequest) -> None:
        """Send feedback by email to the application operator."""
        await self._request("POST", "/api/v1/user/feedback", json=body.to_dict())

    async def change_password(self, body: ChangePasswordRequest) -> None:
        """Change the password of the signed-in user."""
        await self._request("POST", "/api/v1/user/changePassword", json=body.to_dict())
