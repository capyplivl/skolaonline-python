from __future__ import annotations

from skolaonline.models import (
    GetScenariosItemResponse,
    ParticipantsResponse,
    StartEmergencyRequest,
    StartEmergencyResponse,
)
from skolaonline.resources._base import (
    AsyncAPIResource,
    SyncAPIResource,
    parse_model,
    parse_model_list,
)


class Emergency(SyncAPIResource):
    def list_participants(
        self, *, participant_selection_id: str | None = None
    ) -> ParticipantsResponse:
        """Return one level of the emergency participant selection tree."""
        response = self._request(
            "GET",
            "/api/v1/emergency/participantSelection",
            params={"participantSelectionId": participant_selection_id},
        )
        return parse_model(response, ParticipantsResponse)

    def list_scenarios(self) -> list[GetScenariosItemResponse]:
        """Return the saved emergency scenarios of the organization."""
        response = self._request("GET", "/api/v1/emergency/scenarios")
        return parse_model_list(response, GetScenariosItemResponse)

    def start(self, body: StartEmergencyRequest) -> StartEmergencyResponse:
        """Start an emergency or a drill."""
        response = self._request("POST", "/api/v1/emergency/start", json=body.to_dict())
        return parse_model(response, StartEmergencyResponse)


class AsyncEmergency(AsyncAPIResource):
    async def list_participants(
        self, *, participant_selection_id: str | None = None
    ) -> ParticipantsResponse:
        """Return one level of the emergency participant selection tree."""
        response = await self._request(
            "GET",
            "/api/v1/emergency/participantSelection",
            params={"participantSelectionId": participant_selection_id},
        )
        return parse_model(response, ParticipantsResponse)

    async def list_scenarios(self) -> list[GetScenariosItemResponse]:
        """Return the saved emergency scenarios of the organization."""
        response = await self._request("GET", "/api/v1/emergency/scenarios")
        return parse_model_list(response, GetScenariosItemResponse)

    async def start(self, body: StartEmergencyRequest) -> StartEmergencyResponse:
        """Start an emergency or a drill."""
        response = await self._request(
            "POST", "/api/v1/emergency/start", json=body.to_dict()
        )
        return parse_model(response, StartEmergencyResponse)
