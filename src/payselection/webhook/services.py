from typing import Any
from typing import Dict

from payselection.core.exceptions.webhook import EventNotFound
from payselection.core.exceptions.webhook import InvalidRequestSignature
from payselection.core.utils.signature_formation import get_signature
from payselection.webhook.payment.schema import (
    EVENT_SCHEMAS as PAYMENT_EVENT_SCHEMAS,
)
from payselection.webhook.payment.schema import (
    EventWebhookBase as PaymentEventWebhookBase,
)
from payselection.webhook.recurring.schema import (
    EVENT_SCHEMAS as RECURRING_EVENT_SCHEMAS,
)
from payselection.webhook.recurring.schema import (
    EventWebhookBase as RecurringEventWebhookBase,
)


class WebhookSignature:
    @classmethod
    def verify_signature(
        cls,
        request_signature: str,
        signature_params: Dict[str, Any],
        service_secret_key: str,
    ) -> None:
        signature = get_signature(
            method=signature_params['method'],
            url=signature_params['url'],
            site_id=signature_params['site_id'],
            data=signature_params['request_body'],
            secret_key=service_secret_key,
        )

        if request_signature != signature:
            raise InvalidRequestSignature(
                reason='The provided signature does '
                'not match the expected value.',
            )


class WebhookEvent:
    @classmethod
    def get_event_key(cls, data: Dict[str, Any]) -> str:
        for key in ('Event', 'event'):
            if key in data:
                return key
        raise EventNotFound(reason='Event key is missing in data')

    @classmethod
    def get_payment(cls, data: Dict[str, Any]) -> PaymentEventWebhookBase:
        return PAYMENT_EVENT_SCHEMAS[data[cls.get_event_key(data)]](**data)

    @classmethod
    def get_recurring(
        cls,
        data: Dict[str, Any],
    ) -> RecurringEventWebhookBase:
        return RECURRING_EVENT_SCHEMAS[data[cls.get_event_key(data)]](**data)
