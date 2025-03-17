from datetime import datetime
from typing import List
from typing import Optional

from dateutil.zoneinfo import get_zonefile_instance
from pydantic import Field
from pydantic import field_validator
from pydantic import PositiveInt
from typing_extensions import Annotated

from payselection.core.schemas.schema import OrderIdSchema
from payselection.core.schemas.schema import RequestIdSchema
from payselection.core.schemas.schema import TransactionIdSchema
from payselection.gateway_payment.enums import Statuses


class OrderIdRequestSchema(OrderIdSchema):
    pass


class TransactionRequestIdSchema(TransactionIdSchema):
    pass


class TransactionsByDatesSchema(RequestIdSchema):
    start_creation_date: Annotated[str, Field(alias='StartCreationDate')]
    end_creation_date: Annotated[str, Field(alias='EndCreationDate')]
    page_number: Annotated[PositiveInt, Field(alias='PageNumber')]
    time_zone: Annotated[Optional[str], Field(None, alias='TimeZone')]
    statuses: Annotated[
        Optional[List[Statuses]],
        Field(None, alias='Statuses'),
    ]

    @field_validator('time_zone')
    @classmethod
    def validate_time_zone(cls, value: str) -> str:
        if value not in set(get_zonefile_instance().zones):
            raise ValueError(f'Invalid time zone: {value}')
        return value

    @field_validator('start_creation_date', 'end_creation_date')
    @classmethod
    def validate_sum(cls, value: str) -> str:
        try:
            datetime.fromisoformat(value)
        except Exception:
            raise ValueError(
                'This field must be a string, '
                'containing valid date in ISO format',
            )
        return value
