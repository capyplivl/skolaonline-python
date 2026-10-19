# skolaonline

[![CI](https://github.com/capyplivl/skolaonline-python/actions/workflows/ci.yml/badge.svg)](https://github.com/capyplivl/skolaonline-python/actions/workflows/ci.yml)
[![PyPI](https://img.shields.io/pypi/v/skolaonline)](https://pypi.org/project/skolaonline/)
[![Python](https://img.shields.io/pypi/pyversions/skolaonline)](https://pypi.org/project/skolaonline/)
[![License](https://img.shields.io/github/license/capyplivl/skolaonline-python)](https://github.com/capyplivl/skolaonline-python/blob/main/LICENSE)

A modern, fully typed Python SDK for the [Škola OnLine](https://www.skolaonline.cz/) API
(SOL API 1.0), generated from and verified against the official
[OpenAPI specification](https://aplikace.skolaonline.cz/solapi/swagger/v1/swagger.json).

This is an unofficial library and is not affiliated with BAKALÁŘI software s.r.o.

## Features

- Sync and async clients built on [httpx](https://www.python-httpx.org/)
- All 119 API operations across 18 resource groups
- 270+ dataclass models and enums with automatic serialization
- OAuth2 password and refresh token flows with automatic token refresh
- API key and HTTP Basic authentication for system integrations
- File downloads and multipart uploads
- Typed exception hierarchy for API errors
- Full type annotations and `py.typed` support
- English docstrings for every endpoint, parameter, model field and enum member,
  shown by IDE autocompletion

## Installation

```bash
pip install skolaonline
```

## Quick Start

```python
from datetime import date

from skolaonline import SkolaOnline

with SkolaOnline(username="your_username", password="your_password") as client:
    user = client.user.retrieve()
    print(user.full_name, user.user_type)

    timetable = client.timetable.retrieve(
        student_id=user.person_id,
        date_from=date(2026, 10, 19),
        date_to=date(2026, 10, 23),
    )
    for day in timetable.days:
        for hour in day.schedules:
            subject = hour.subject.name if hour.subject else hour.title
            print(day.date.date(), hour.begin_time.time(), subject)

    marks = client.marks.list_marks(user.person_id)
    for mark in marks.marks:
        print(mark.mark_date.date(), mark.mark_text, mark.theme)
```

For parent accounts, use the IDs from `user.children` as `student_id`.

### Async

```python
from skolaonline import AsyncSkolaOnline

async with AsyncSkolaOnline(
    username="your_username", password="your_password"
) as client:
    user = await client.user.retrieve()
    messages = await client.messages.list_received(page_size=20)
    for message in messages.messages:
        print(message.sent_date, message.title)
```

Every method of `SkolaOnline` has an async counterpart with the same name and
signature on `AsyncSkolaOnline`.

## Authentication

### Username and password

The client requests an access token from the OAuth2 token endpoint
(`/api/connect/token`) on the first API call. Tokens are refreshed automatically
with the refresh token when they expire or when the API answers with
`401 Unauthorized`. If the refresh token is rejected, the client signs in again
with the stored credentials.

```python
client = SkolaOnline(username="your_username", password="your_password")
token = client.login()
print(token.access_token, token.refresh_token, token.expires_at)
```

`login()` is optional and forces an immediate sign in, which is useful to
validate credentials early.

### Reusing tokens

Persist tokens to avoid storing passwords. The `on_token_refresh` callback is
called with a `Token` every time a new token is obtained.

```python
from skolaonline import SkolaOnline, Token


def save_token(token: Token) -> None:
    store(token.access_token, token.refresh_token, token.expires_at)


client = SkolaOnline(
    access_token="stored_access_token",
    refresh_token="stored_refresh_token",
    expires_at=1792400000.0,
    on_token_refresh=save_token,
)
```

Passing only `refresh_token` is also supported. A client created with only
`access_token` uses it as is and never refreshes it.

### Standalone token helpers

```python
from skolaonline import get_token, refresh_access_token

token = get_token("your_username", "your_password")
token = refresh_access_token(token.refresh_token)
```

`async_get_token()` and `async_refresh_access_token()` are the async variants.

### API key and Basic authentication

Data interface endpoints used by system integrations accept an API key sent in
the `X-Api-Key` header, or HTTP Basic credentials.

```python
client = SkolaOnline(api_key="your_api_key")
students = client.data_interface.list_students()

client = SkolaOnline(basic_auth=("integration_user", "secret"))
```

Only one authentication method can be configured per client. Clients without any
credentials can call anonymous endpoints such as
`client.configuration.min_app_version()`.

## Configuration

| Argument | Default | Description |
|----------|---------|-------------|
| `base_url` | `https://aplikace.skolaonline.cz/solapi` | API root, also used for the token endpoint |
| `language` | `None` | Response language sent in the `app-lang` header, `cs` or `en` |
| `timeout` | `30.0` | Timeout in seconds for API and token requests |
| `headers` | `None` | Extra headers sent with every request |
| `client_id` | `test_client` | OAuth2 client ID |
| `scope` | `openid offline_access profile sol_api` | OAuth2 scope for the password grant |
| `http_client` | `None` | Custom `httpx.Client` or `httpx.AsyncClient` |

### Supplying an HTTPX client

Pass your own `httpx.Client` to reuse a connection pool, proxies, transports or
event hooks. The SDK applies its base URL, authentication, timeout and headers
per request. A supplied client is not closed by the SDK.

```python
import httpx

from skolaonline import SkolaOnline

with httpx.Client(proxy="http://localhost:8080") as http:
    client = SkolaOnline(username="user", password="secret", http_client=http)
    client.user.retrieve()
```

## API Coverage

| Resource | Methods |
|----------|---------|
| `absences` | `code_lists`, `list_by_subject`, `list_in_day`, `list_in_period` |
| `apologies` | `accept`, `cancel_rejection`, `code_lists`, `create`, `delete`, `list_absence_reasons`, `list_for_student`, `list_for_teacher`, `list_teacher_classes`, `list_times_from`, `list_times_to`, `reject`, `retrieve_for_student`, `retrieve_for_teacher`, `retrieve_rejection_reason`, `update`, `update_rejection_reason` |
| `b2c` | `authenticate`, `synchronize` |
| `behaviors` | `code_lists`, `create`, `delete`, `list_educational_measure_kinds`, `list_educational_measure_reasons`, `list_evaluation_kinds`, `list_for_student`, `list_for_teacher`, `list_note_kinds`, `list_students_of_class`, `list_teacher_classes`, `list_types`, `retrieve`, `sign`, `sign_many`, `update` |
| `class_books` | `calculate_lesson_number`, `delete`, `list_entries`, `save`, `save_attendance` |
| `configuration` | `min_app_version` |
| `data_interface` | `list_additional_data_definitions`, `list_classes`, `list_student_records`, `list_students`, `list_students_with_consent` |
| `emergency` | `list_participants`, `list_scenarios`, `start` |
| `files` | `download`, `upload` |
| `homeworks` | `code_lists`, `delete_elaboration_attachment`, `download_assignment_attachment`, `download_elaboration_attachment`, `list_for_student`, `list_for_teacher`, `mark_done`, `retrieve`, `save_elaboration`, `upload_elaboration_attachment` |
| `marks` | `code_lists`, `create_for_teacher`, `delete_for_teacher`, `list_by_subject`, `list_final`, `list_marking_students`, `list_marks`, `retrieve`, `retrieve_for_teacher`, `sign`, `sign_many`, `update_for_teacher` |
| `messages` | `count_recipients`, `create_draft`, `delete`, `download_attachment`, `list_drafts`, `list_received`, `list_recipients`, `list_recipients_without_contacts`, `list_sent`, `mark_as_read`, `retrieve_received`, `retrieve_sent`, `retrieve_settings`, `send`, `send_draft`, `update_draft`, `upload_attachment`, `vote` |
| `notifications` | `retrieve_preferences`, `save_preferences`, `send`, `send_emergency`, `send_two_factor` |
| `payments` | `list_regular`, `retrieve`, `retrieve_summary`, `update_parents_note` |
| `student_status` | `list_students` |
| `test` | `ping` |
| `timetable` | `code_lists`, `retrieve`, `retrieve_detail` |
| `user` | `change_password`, `disable_notifications`, `enable_notifications`, `list_notifications`, `logout`, `notifications_exist`, `retrieve`, `retrieve_dashboard`, `retrieve_password_requirements`, `send_feedback` |

Path parameters are positional, query and header parameters are keyword-only and
use snake_case names. Pagination parameters `Pagination.PageNumber` and
`Pagination.PageSize` are exposed as `page_number` and `page_size`. Dates accept
`datetime.date` or `datetime.datetime`.

Operations that the specification documents without a response schema return the
decoded JSON value, the response text, or `None` for empty responses.

The test suite checks every method against the bundled OpenAPI specification:
each operation is implemented exactly once, with the documented HTTP method,
path, query parameters, headers and request body type.

## Models

Models live in `skolaonline.models`. Field names are snake_case versions of the
API names, and `to_dict()` converts a model back to the API representation.

```python
from datetime import datetime

from skolaonline.models import ApologyPostData

apology = ApologyPostData(
    excused_person_id="student_id",
    reason_absence_id="reason_id",
    date_from=datetime(2026, 10, 20),
    date_to=datetime(2026, 10, 21),
    specification="Doctor appointment",
)
client.apologies.create(apology)
```

- Model fields are keyword-only. Required fields of request models have no default.
- Enum fields use `StrEnum` members. Unknown values returned by the API are kept
  as plain strings.
- Date and time fields are parsed into `datetime` objects.
- Names that collide across API modules are prefixed with their module, for
  example `MarkCodeListsResponse` and `TimetableCodeListsResponse`.

## Files

Downloads return a `DownloadedFile` with the content, the file name from the
`Content-Disposition` header and the content type.

```python
file = client.messages.download_attachment(message_id, attachment_id)
file.save(file.filename or "attachment")
```

Uploads accept bytes, a binary file object, or a `(filename, content)` or
`(filename, content, content_type)` tuple.

```python
with open("homework.pdf", "rb") as handle:
    client.homeworks.upload_elaboration_attachment(homework_id, handle, submit=True)

result = client.files.upload([("notes.txt", b"Notes", "text/plain")])
```

## Error Handling

```python
from skolaonline import (
    APIError,
    AuthenticationError,
    NotFoundError,
    PermissionDeniedError,
    SkolaOnlineError,
)

try:
    client.marks.retrieve("mark_id")
except AuthenticationError as error:
    print("Sign in failed", error.error_code)
except PermissionDeniedError:
    print("The module is not enabled for this user")
except NotFoundError:
    print("Mark not found")
except APIError as error:
    print(error.status_code, error.message, error.body)
except SkolaOnlineError as error:
    print("Client error", error)
```

| HTTP status | Exception |
|-------------|-----------|
| 400 | `BadRequestError` |
| 401 | `AuthenticationError` |
| 403 | `PermissionDeniedError` |
| 404 | `NotFoundError` |
| 409 | `ConflictError` |
| 422 | `UnprocessableEntityError` |
| 429 | `RateLimitError` |
| 5xx | `ServerError` |
| Other 4xx | `APIError` |

Every `APIError` exposes `status_code`, `message`, the decoded `body` and the
original `httpx.Response`. The message is taken from `userMessage`, `message`,
`detail`, `title` or `error_description` when the API returns JSON, otherwise
from the response text. Token endpoint failures always raise
`AuthenticationError`. `SkolaOnlineError` is the base class of all exceptions
raised by the library.

## Development

```bash
uv sync
make test
make coverage
make typecheck
make lint
make format
```

## Python Version

Supports Python 3.11 through 3.14.

## Contributing

Contributions are welcome. Please read the [Contributing Guide](CONTRIBUTING.md)
before opening a pull request.

## License

[MIT](LICENSE)
