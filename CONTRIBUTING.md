# Contributing

Thank you for your interest in improving `skolaonline`.

## Setup

The project uses [uv](https://docs.astral.sh/uv/) for dependency management.

```bash
git clone https://github.com/capyplivl/skolaonline-python.git
cd skolaonline-python
uv sync
```

## Checks

Run all checks before opening a pull request:

```bash
make format
make lint
make typecheck
make test
```

## Guidelines

- Keep the public API typed and covered by tests.
- Mock HTTP traffic with [respx](https://lundberg.github.io/respx/). Tests must not
  call the real API.
- Never commit credentials, tokens or personal data from a real school account.
- Follow [Conventional Commits](https://www.conventionalcommits.org/) for commit
  messages, for example `feat: add timetable filters` or `fix: parse empty dates`.

## API specification

`tests/fixtures/swagger.json` is a copy of the official specification from
`https://aplikace.skolaonline.cz/solapi/swagger/v1/swagger.json`. When the API
changes, update the fixture together with the models and resources. The contract
tests in `tests/test_spec_coverage.py` fail when an operation is missing or does
not match the specification.

## Releasing

1. Update the version in `pyproject.toml` and add an entry to `CHANGELOG.md`.
2. Run `uv lock` and commit the changes.
3. Create and push a tag such as `v0.1.0`.

The `Publish` workflow builds the package and uploads it to PyPI using trusted
publishing. The PyPI project must have this repository and the `pypi` environment
configured as a trusted publisher.
