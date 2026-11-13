"""HTTP helpers shared by all extractors: timeouts, retries and JSON decoding."""

from __future__ import annotations

import time
from typing import Any

import requests

DEFAULT_TIMEOUT_SECONDS = 60
DEFAULT_RETRIES = 6
DEFAULT_BACKOFF_SECONDS = 3.0
USER_AGENT = "brazil-economic-trajectory/0.1 (+https://github.com/gabrielnicolini/brazil-economic-trajectory)"

RETRYABLE_STATUS = {429, 500, 502, 503, 504}


class HttpError(RuntimeError):
    """Raised when a request fails after all retries."""


def get_json(
    url: str,
    params: dict[str, Any] | None = None,
    *,
    timeout: float = DEFAULT_TIMEOUT_SECONDS,
    retries: int = DEFAULT_RETRIES,
    backoff: float = DEFAULT_BACKOFF_SECONDS,
    session: requests.Session | None = None,
) -> Any:
    """GET a URL and decode its JSON body, retrying transient failures.

    Retries on connection errors, timeouts, the status codes in
    ``RETRYABLE_STATUS`` and undecodable bodies with exponential backoff. Any other HTTP error is
    raised immediately. The token-free URL is safe to log.
    """
    http = session or requests.Session()
    headers = {"User-Agent": USER_AGENT, "Accept": "application/json"}
    last_error: Exception | None = None
    for attempt in range(retries + 1):
        try:
            response = http.get(url, params=params, headers=headers, timeout=timeout)
        except (requests.ConnectionError, requests.Timeout) as exc:
            last_error = exc
        else:
            if response.status_code in RETRYABLE_STATUS:
                last_error = HttpError(f"HTTP {response.status_code} for {response.url}")
            else:
                response.raise_for_status()
                try:
                    return response.json()
                except ValueError as exc:  # transient HTML or empty body with status 200
                    last_error = HttpError(f"non-JSON body for {response.url}: {exc}")
        if attempt < retries:
            time.sleep(backoff * (2**attempt))
    raise HttpError(f"request failed after {retries + 1} attempts: {url}") from last_error
