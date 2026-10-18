from __future__ import annotations

import json
from datetime import date, datetime

import httpx
import pytest
import respx

from skolaonline import (
    APIError,
    AsyncSkolaOnline,
    AuthenticationError,
    BadRequestError,
    ConflictError,
    NotFoundError,
    PermissionDeniedError,
    RateLimitError,
    ServerError,
    SkolaOnline,
    UnprocessableEntityError,
    __version__,
)
from skolaonline.models import (
    ApologyPostData,
    EmergencyIncidentType,
    GetMessageRecipientsCountRequest,
    GetScenariosItemResponse,
    HomeworksFilterState,
    RegularPaymentsState,
)
from tests._helpers import BASE_URL


@pytest.fixture
def client() -> SkolaOnline:
    return SkolaOnline(access_token="token")


@respx.mock
def test_default_headers(client: SkolaOnline) -> None:
    route = respx.get(f"{BASE_URL}/api/v1/test/ping").mock(
        return_value=httpx.Response(200)
    )
    client.test.ping()
    headers = route.calls.last.request.headers
    assert headers["accept"] == "application/json"
    assert headers["user-agent"] == f"skolaonline-python/{__version__}"
    assert "app-lang" not in headers


@respx.mock
def test_language_and_custom_headers() -> None:
    route = respx.get(f"{BASE_URL}/api/v1/test/ping").mock(
        return_value=httpx.Response(200)
    )
    client = SkolaOnline(access_token="t", language="en", headers={"X-App": "demo"})
    client.test.ping()
    headers = route.calls.last.request.headers
    assert headers["app-lang"] == "en"
    assert headers["x-app"] == "demo"


@respx.mock
def test_query_parameter_serialization(client: SkolaOnline) -> None:
    route = respx.get(f"{BASE_URL}/api/v1/students/s1/homeworks").mock(
        return_value=httpx.Response(200, json={"homeworks": []})
    )
    response = client.homeworks.list_for_student(
        "s1",
        date_from=date(2024, 9, 1),
        date_to=datetime(2024, 9, 30, 23, 59),
        filter=HomeworksFilterState.ACTIVE,
        page_number=2,
    )
    assert response.homeworks == []
    params = route.calls.last.request.url.params
    assert dict(params) == {
        "DateFrom": "2024-09-01",
        "DateTo": "2024-09-30T23:59:00",
        "Filter": "active",
        "Pagination.PageNumber": "2",
    }


@respx.mock
def test_boolean_and_list_parameters(client: SkolaOnline) -> None:
    notes = respx.get(f"{BASE_URL}/api/v1/behaviors/kindsOfNotesClassBook").mock(
        return_value=httpx.Response(200, json={"kindsOfNotes": []})
    )
    payments = respx.get(f"{BASE_URL}/api/v1/student/s1/payments/regularpayments").mock(
        return_value=httpx.Response(200, json={"payments": []})
    )
    client.behaviors.list_note_kinds(only_valid=True, only_negative=False)
    client.payments.list_regular(
        "s1", state=[RegularPaymentsState.PAID, RegularPaymentsState.NOT_PAID]
    )
    assert str(notes.calls.last.request.url).endswith(
        "?OnlyValid=true&OnlyNegative=false"
    )
    assert payments.calls.last.request.url.params.get_list("State") == [
        "paid",
        "notPaid",
    ]


@respx.mock
def test_path_parameters_are_encoded(client: SkolaOnline) -> None:
    route = respx.get(f"{BASE_URL}/api/v1/student/marks/a%2Fb%20c").mock(
        return_value=httpx.Response(200, json={})
    )
    client.marks.retrieve("a/b c")
    assert route.called


@respx.mock
def test_json_model_body(client: SkolaOnline) -> None:
    route = respx.post(f"{BASE_URL}/api/v1/apologies").mock(
        return_value=httpx.Response(200, json={"id": "new"})
    )
    result = client.apologies.create(
        ApologyPostData(
            excused_person_id="s1",
            reason_absence_id="r1",
            date_from=datetime(2024, 9, 2),
            date_to=datetime(2024, 9, 3),
        )
    )
    assert result == {"id": "new"}
    assert json.loads(route.calls.last.request.content) == {
        "excusedPersonId": "s1",
        "reasonAbsenceId": "r1",
        "dateFrom": "2024-09-02T00:00:00",
        "dateTo": "2024-09-03T00:00:00",
    }


@respx.mock
def test_string_and_list_bodies(client: SkolaOnline) -> None:
    reject = respx.put(f"{BASE_URL}/api/v1/apologies/a1/reject").mock(
        return_value=httpx.Response(200, json={"message": None})
    )
    accept = respx.put(f"{BASE_URL}/api/v1/apologies/a1/accept").mock(
        return_value=httpx.Response(200)
    )
    sync = respx.post(f"{BASE_URL}/api/v1/b2c/synchronize").mock(
        return_value=httpx.Response(200, json={"users": []})
    )
    assert client.apologies.reject("a1", "Too late").message is None
    assert json.loads(reject.calls.last.request.content) == "Too late"
    assert client.apologies.accept("a1") is None
    assert accept.calls.last.request.content == b""
    client.apologies.accept("a1", absence_reason="Illness")
    assert json.loads(accept.calls.last.request.content) == "Illness"
    client.b2c.synchronize(("u1", "u2"))
    assert json.loads(sync.calls.last.request.content) == ["u1", "u2"]


@respx.mock
def test_header_parameters(client: SkolaOnline) -> None:
    route = respx.get(f"{BASE_URL}/api/v1/messages/recipients").mock(
        return_value=httpx.Response(200, json=[{"id": "teachers"}])
    )
    assert client.messages.list_recipients(group_id="g1", child_id="c1") == [
        {"id": "teachers"}
    ]
    request = route.calls.last.request
    assert request.headers["api-childid"] == "c1"
    assert request.url.params["id"] == "g1"


@respx.mock
def test_list_and_integer_responses(client: SkolaOnline) -> None:
    respx.get(f"{BASE_URL}/api/v1/emergency/scenarios").mock(
        return_value=httpx.Response(
            200,
            json=[
                {
                    "EmergencyIncidentType": "fire",
                    "EmergencyEventType": "emergency",
                    "NotificationText": "Evacuate",
                }
            ],
        )
    )
    respx.post(f"{BASE_URL}/api/v1/messages/recipientsCount").mock(
        return_value=httpx.Response(200, json=12)
    )
    scenarios = client.emergency.list_scenarios()
    assert isinstance(scenarios[0], GetScenariosItemResponse)
    assert scenarios[0].emergency_incident_type is EmergencyIncidentType.FIRE
    count = client.messages.count_recipients(
        GetMessageRecipientsCountRequest(recipients_groups=["r1"])
    )
    assert count == 12


@respx.mock
def test_untyped_responses(client: SkolaOnline) -> None:
    respx.get(f"{BASE_URL}/api/v1/user/notificationsExist").mock(
        return_value=httpx.Response(200, json=True)
    )
    respx.delete(f"{BASE_URL}/api/v1/messages/m1").mock(
        return_value=httpx.Response(204)
    )
    respx.get(f"{BASE_URL}/api/v1/apologies/a1/rejectionReason").mock(
        return_value=httpx.Response(200, text="plain reason")
    )
    assert client.user.notifications_exist(fcm_token="fcm") is True
    assert client.messages.delete("m1") is None
    assert client.apologies.retrieve_rejection_reason("a1") == "plain reason"


@pytest.mark.parametrize(
    ("status", "error"),
    [
        (400, BadRequestError),
        (401, AuthenticationError),
        (403, PermissionDeniedError),
        (404, NotFoundError),
        (409, ConflictError),
        (422, UnprocessableEntityError),
        (429, RateLimitError),
        (500, ServerError),
        (503, ServerError),
        (418, APIError),
    ],
)
@respx.mock
def test_error_mapping(client: SkolaOnline, status: int, error: type[APIError]) -> None:
    respx.get(f"{BASE_URL}/api/v1/test/ping").mock(
        return_value=httpx.Response(status, json="Something failed")
    )
    with pytest.raises(error) as info:
        client.test.ping()
    assert type(info.value) is error
    assert info.value.status_code == status
    assert info.value.message == "Something failed"
    assert info.value.response.status_code == status


@pytest.mark.parametrize(
    ("payload", "message"),
    [
        ({"message": "internal", "userMessage": "For user"}, "For user"),
        ({"title": "Bad Request", "detail": "Missing field"}, "Missing field"),
        ({"title": "Forbidden"}, "Forbidden"),
        ({}, "Internal Server Error"),
    ],
)
@respx.mock
def test_error_message_extraction(
    client: SkolaOnline, payload: dict[str, str], message: str
) -> None:
    respx.get(f"{BASE_URL}/api/v1/test/ping").mock(
        return_value=httpx.Response(500, json=payload)
    )
    with pytest.raises(ServerError) as info:
        client.test.ping()
    assert info.value.message == message
    assert info.value.body == payload


@respx.mock
def test_plain_text_error(client: SkolaOnline) -> None:
    respx.get(f"{BASE_URL}/api/v1/test/ping").mock(
        return_value=httpx.Response(400, text="Invalid date")
    )
    with pytest.raises(BadRequestError, match="Invalid date"):
        client.test.ping()


@respx.mock
def test_raw_request(client: SkolaOnline) -> None:
    respx.get(f"{BASE_URL}/api/v1/minAppVersion").mock(
        return_value=httpx.Response(200, json={"ios": "1.0"})
    )
    response = client.request("GET", "/api/v1/minAppVersion")
    assert response.json() == {"ios": "1.0"}


def test_supplied_http_client_is_not_closed() -> None:
    http = httpx.Client()
    with SkolaOnline(access_token="t", http_client=http):
        pass
    assert not http.is_closed
    http.close()


def test_owned_http_client_is_closed() -> None:
    client = SkolaOnline(access_token="t")
    client.close()
    assert client._http_client.is_closed


@respx.mock
def test_supplied_http_client_is_used() -> None:
    route = respx.get(f"{BASE_URL}/api/v1/test/ping").mock(
        return_value=httpx.Response(200)
    )
    with httpx.Client(headers={"X-Trace": "1"}) as http:
        SkolaOnline(access_token="t", http_client=http).test.ping()
    assert route.calls.last.request.headers["x-trace"] == "1"


async def test_async_client_closes_owned_http_client() -> None:
    client = AsyncSkolaOnline(access_token="t")
    await client.close()
    assert client._http_client.is_closed


@respx.mock
async def test_async_requests_and_errors() -> None:
    respx.get(f"{BASE_URL}/api/v1/minAppVersion").mock(
        return_value=httpx.Response(200, json={"iOS": "2.0", "android": "3.1"})
    )
    respx.get(f"{BASE_URL}/api/v1/user").mock(return_value=httpx.Response(403))
    async with AsyncSkolaOnline(access_token="t") as client:
        version = await client.configuration.min_app_version()
        assert version.ios == "2.0"
        assert version.android == "3.1"
        with pytest.raises(PermissionDeniedError):
            await client.user.retrieve()
