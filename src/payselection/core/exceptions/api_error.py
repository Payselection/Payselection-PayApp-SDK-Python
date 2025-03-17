from typing import Any
from typing import Dict
from typing import Optional


class APIError(Exception):
    def __init__(
        self,
        status_code: int,
        error_code: str,
        description: str,
        details: Optional[Dict[str, Any]],
    ):
        self.status_code = status_code
        self.error_code = error_code
        self.description = description
        self.details = details

        details_str = (
            ' '.join(f'{k.title()}: {v}' for k, v in details.items())
            if details is not None
            else ''
        )
        self.message = (
            f'{status_code} {error_code}. '
            f'Description: {description}. {details_str}'
        ).strip()

        super().__init__(self.message)


class APIClientError(Exception):
    pass


class InvalidCallerAPI(APIClientError):
    def __init__(self, reason: Any) -> None:
        self.reason = reason
