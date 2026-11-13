"""Tests for the shared HTTP helper. No network access: the session is faked."""

from __future__ import annotations

import pytest
import requests

from ingestion.common import http


class FakeResponse:
    def __init__(self, status_code: int, body: str, url: str = "https://example.test/x"):
        self.status_code = status_code
        self.text = body
        self.url = url

    def raise_for_status(self) -> None:
        if self.status_code >= 400:
            raise requests.HTTPError(f"HTTP {self.status_code}")

    def json(self):
        import json

        return json.loads(self.text)


class FakeSession:
    def __init__(self, responses):
        self.responses = list(responses)
        self.calls = 0

    def get(self, url, params=None, headers=None, timeout=None):
        self.calls += 1
        item = self.responses.pop(0)
        if isinstance(item, Exception):
            raise item
        return item


def test_returns_decoded_json_on_success():
    session = FakeSession([FakeResponse(200, '[{"a": 1}]')])
    assert http.get_json("https://example.test/x", session=session, backoff=0) == [{"a": 1}]
    assert session.calls == 1


def test_retries_non_json_body_then_succeeds():
    session = FakeSession([FakeResponse(200, "<html>busy</html>"), FakeResponse(200, "[]")])
    assert http.get_json("https://example.test/x", session=session, backoff=0) == []
    assert session.calls == 2


def test_retries_retryable_status_and_connection_errors():
    session = FakeSession(
        [FakeResponse(503, ""), requests.ConnectionError("down"), FakeResponse(200, "{}")]
    )
    assert http.get_json("https://example.test/x", session=session, backoff=0) == {}
    assert session.calls == 3


def test_gives_up_after_retries():
    session = FakeSession([FakeResponse(503, "")] * 3)
    with pytest.raises(http.HttpError):
        http.get_json("https://example.test/x", session=session, retries=2, backoff=0)
    assert session.calls == 3


def test_non_retryable_status_raises_immediately():
    session = FakeSession([FakeResponse(404, "")])
    with pytest.raises(requests.HTTPError):
        http.get_json("https://example.test/x", session=session, backoff=0)
    assert session.calls == 1
