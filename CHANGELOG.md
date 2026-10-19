# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.0] - 2026-10-19

### Added

- Sync `SkolaOnline` and async `AsyncSkolaOnline` clients covering all 119
  operations of SOL API 1.0.
- Typed dataclass models and enums for all 272 schemas of the specification.
- OAuth2 password and refresh token authentication with automatic refresh,
  token persistence callback and standalone token helpers.
- API key and HTTP Basic authentication.
- File downloads with `DownloadedFile` and multipart uploads.
- Exception hierarchy mapped from HTTP status codes.
- English docstrings for all endpoints, parameters, models, fields and enum
  members.

[Unreleased]: https://github.com/capyplivl/skolaonline-python/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/capyplivl/skolaonline-python/releases/tag/v0.1.0
