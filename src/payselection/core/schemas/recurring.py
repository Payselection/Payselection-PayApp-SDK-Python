from datetime import datetime
from datetime import timedelta
from typing import List
from typing import Optional

from pydantic import EmailStr
from pydantic import Field
from pydantic import field_validator
from pydantic import HttpUrl
from typing_extensions import Annotated

from payselection.core.enums import Period
from payselection.core.schemas.receipt.receipt_data import ReceiptData
from payselection.core.schemas.schema import AMOUNT
from payselection.core.schemas.schema import BaseSchema
from payselection.core.schemas.schema import DATE_MAPPING
from payselection.core.schemas.schema import SplitData
from payselection.core.utils.currency_code import ISO4217


class RecurringData(BaseSchema):
    amount: AMOUNT
    currency: Annotated[ISO4217, Field(alias='Currency')]
    description: Annotated[
        Optional[str],
        Field(
            None,
            alias='Description',
            min_length=1,
            max_length=250,
        ),
    ]
    webhook_url: Annotated[Optional[HttpUrl], Field(None, alias='WebhookUrl')]
    account_id: Annotated[
        str,
        Field(
            alias='AccountId',
            min_length=1,
            max_length=100,
            pattern=r'^[\x20-\x7Eа-яА-Я№]+$',
        ),
    ]
    email: Annotated[Optional[EmailStr], Field(None, alias='Email')]
    start_date: Annotated[Optional[str], Field(None, alias='StartDate')]
    interval: Annotated[
        str,
        Field(
            alias='Interval',
            min_length=1,
            max_length=366,
            pattern=r'^\d+$',
        ),
    ]
    period: Annotated[Period, Field(alias='Period')]
    max_periods: Annotated[
        Optional[str],
        Field(
            None,
            alias='MaxPeriods',
            min_length=1,
            max_length=999,
            pattern=r'^\d+$',
        ),
    ]
    receipt_data: Annotated[
        Optional[ReceiptData],
        Field(None, alias='ReceiptData'),
    ]
    split_data: Annotated[
        Optional[List[SplitData]],
        Field(None, alias='SplitData'),
    ]

    @field_validator('start_date', mode='after')
    @classmethod
    def validate_start_date(cls, start_date: str, values) -> str:
        date_format = '%Y-%m-%dT%H:%M+0000'
        if start_date is None:
            interval = int(values.data['interval'])
            period = DATE_MAPPING[values.data['period']]
            computed_date = datetime.now() + interval * period
            return computed_date.strftime(date_format)

        try:
            start_date_dt = datetime.strptime(start_date, date_format)
        except ValueError:
            raise ValueError(
                'StartDate must be in the format YYYY-MM-DDTHH:MM+0000',
            )

        current_date = datetime.now()
        if start_date_dt < current_date:
            raise ValueError(
                'The field cannot be earlier than the current date.',
            )

        max_date = current_date + timedelta(days=365)
        if start_date_dt > max_date:
            raise ValueError(
                'The field cannot be more than 1 year from the current date.',
            )

        return start_date
