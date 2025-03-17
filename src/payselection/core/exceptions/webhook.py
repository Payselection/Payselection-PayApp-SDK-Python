from typing import Any


class WebhookException(Exception):
    pass


class InvalidRequestSignature(WebhookException):
    def __init__(self, reason: Any) -> None:
        self.reason = reason


class EventNotFound(WebhookException):
    def __init__(self, reason: Any) -> None:
        self.reason = reason
