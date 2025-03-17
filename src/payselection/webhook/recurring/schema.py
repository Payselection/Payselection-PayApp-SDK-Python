from typing import Optional

from pydantic import Field
from typing_extensions import Annotated

from payselection.core.schemas.schema import BaseSchema
from payselection.recurring.schema import RebillIdSchema
from payselection.recurring.schema import RecurringIdSchema
from payselection.web_payment.schema import RecurringData
from payselection.webhook.recurring.enum import Event
from payselection.webhook.recurring.enum import RecurringStatus


class EventWebhookBase(RebillIdSchema, RecurringData, RecurringIdSchema):
    event: Annotated[Event, Field(alias='Event')]
    recurring_status: Annotated[
        RecurringStatus,
        Field(alias='RecurringStatus'),
    ]


class RegisterRecurringEventWebhook(EventWebhookBase):
    pass


class ChangeRecurringStateEventWebhook(EventWebhookBase):
    class Recurrent(BaseSchema):
        class TransactionStateDetails(BaseSchema):
            code: Annotated[str, Field(alias='Code')]
            description: Annotated[str, Field(alias='Description')]

        transaction_id: Annotated[
            Optional[str],
            Field(
                None,
                alias='TransactionId',
                min_length=16,
                max_length=16,
            ),
        ]
        transaction_state: Annotated[
            Optional[str],
            Field(
                None,
                alias='TransactionState',
            ),
        ]
        transaction_state_details: Annotated[
            Optional[TransactionStateDetails],
            Field(
                None,
                alias='TransactionStateDetails',
            ),
        ]

    split_data: Annotated[None, Field(None, exclude=True)]
    recurrent: Annotated[Recurrent, Field(alias='Recurrent')]


class UnsubscribeRecurringEventWebhook(EventWebhookBase):
    split_data: Annotated[None, Field(None, exclude=True)]


class ChangeRecurringByMerchantEventWebhook(EventWebhookBase):
    pass


EVENT_SCHEMAS = {
    Event.REGISTER_RECURRING: RegisterRecurringEventWebhook,
    Event.CHANGE_RECURRING_STATE: ChangeRecurringStateEventWebhook,
    Event.UNSUBSCRIBE_RECURRING: UnsubscribeRecurringEventWebhook,
    Event.CHANGE_RECURRING_BY_MERCHANT: ChangeRecurringByMerchantEventWebhook,
}
