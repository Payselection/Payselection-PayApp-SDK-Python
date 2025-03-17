from typing import Any
from typing import Dict
from typing import Optional

from pydantic import Field
from pydantic import model_validator
from typing_extensions import Annotated

from payselection.core.enums import Period
from payselection.core.schemas.schema import BaseSchema
from payselection.core.schemas.schema import RequestIdSchema
from payselection.recurring.enum import SearchIdentifier
from payselection.web_payment.schema import RecurringData


class RebillIdSchema(BaseSchema):
    rebill_id: Annotated[
        str,
        Field(alias='RebillId', min_length=16, max_length=16),
    ]


class RecurringIdSchema(BaseSchema):
    recurring_id: Annotated[
        str,
        Field(
            alias='RecurringId',
            min_length=1,
            max_length=20,
            pattern=r'^\d+$',
        ),
    ]


class AccountIdSchema(BaseSchema):
    account_id: Annotated[
        str,
        Field(
            alias='AccountId',
            min_length=1,
            max_length=100,
            pattern=r'^[\x20-\x7Eа-яА-Я№]+$',
        ),
    ]


class RecurringIdRequestSchema(RecurringIdSchema, RequestIdSchema):
    pass


class RecurringSchema(RebillIdSchema, RecurringData, RequestIdSchema):
    pass


class NewRecurringSearchRebillRequest(RebillIdSchema, RequestIdSchema):
    pass


class NewRecurringSearchRecurringRequest(RecurringIdSchema, RequestIdSchema):
    pass


class NewRecurringSearchAccountRequest(AccountIdSchema, RequestIdSchema):
    pass


SEARCH_SCHEMAS = {
    SearchIdentifier.RebillId: NewRecurringSearchRebillRequest,
    SearchIdentifier.RecurringId: NewRecurringSearchRecurringRequest,
    SearchIdentifier.AccountId: NewRecurringSearchAccountRequest,
}


class RecurringChangeSchema(RecurringData, RecurringIdSchema, RequestIdSchema):
    currency: Annotated[None, Field(None, exclude=None)]
    description: Annotated[None, Field(None, exclude=None)]
    webhook_url: Annotated[None, Field(None, exclude=None)]
    account_id: Annotated[None, Field(None, exclude=None)]
    email: Annotated[None, Field(None, exclude=None)]
    interval: Annotated[
        Optional[str],
        Field(
            None,
            alias='Interval',
            min_length=1,
            max_length=366,
            pattern=r'^\d+$',
        ),
    ]
    period: Annotated[Optional[Period], Field(None, alias='Period')]
    amount: Annotated[
        Optional[str],
        Field(
            None,
            alias='Amount',
            min_length=1,
            max_length=16,
            pattern=r'^\d+(?:\.\d{2})?$',
        ),
    ]

    @model_validator(mode='before')
    @classmethod
    def check_at_least_one_field(
        cls,
        values: Dict[str, Any],
    ) -> Dict[str, Any]:
        copy_values = values.copy()
        copy_values.pop('recurring_id', None)
        copy_values.pop('request_id', None)
        if not copy_values:
            raise ValueError(
                'The request must contain '
                'at least one of the optional parameters.',
            )
        return values
