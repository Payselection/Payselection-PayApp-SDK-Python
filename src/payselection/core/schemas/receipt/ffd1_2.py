from datetime import datetime
from typing import List
from typing import Optional

from pydantic import BaseModel
from pydantic import Field
from pydantic import field_validator
from typing_extensions import Annotated

from payselection.core.enums import AgentType
from payselection.core.enums import Measure
from payselection.core.enums import PaymentObjectInt
from payselection.core.enums import SNO
from payselection.core.schemas.receipt.item import ItemBase
from payselection.core.schemas.receipt.item import VatRequiredType
from payselection.core.schemas.receipt.receipt_data import AgentInfo
from payselection.core.schemas.receipt.receipt_data import BaseCompany
from payselection.core.schemas.receipt.receipt_data import BaseFFD
from payselection.core.schemas.schema import PhonesSchema


class SectoralProp(BaseModel):
    federal_id: str
    date: str
    number: Annotated[str, Field(max_length=32)]
    value: Annotated[str, Field(max_length=256)]

    @field_validator('date')
    @classmethod
    def validate_date_format(cls, value: str) -> str:
        datetime.strptime(value, '%d.%m.%Y')
        return value

    @field_validator('federal_id')
    @classmethod
    def validate_federal_id(cls, v):
        if len(v) == 3 and v.isdigit() and 1 <= int(v) <= 72:
            return v
        raise ValueError(
            'federal_id must be a 3-digit string between 001 and 072',
        )


class FFD1_2(BaseFFD):
    class Company(BaseCompany):
        sno: SNO

    class Item(ItemBase):
        class ItemSupplierInfo(PhonesSchema):
            phones: List[str]

        class MarkQuantity(BaseModel):
            numerator: Annotated[int, Field(gt=0)]
            denominator: Annotated[int, Field(gt=0)]

            @field_validator('denominator')
            @classmethod
            def validate_denominator_numerator(cls, denominator: int, values):
                if denominator <= values.data.get('numerator', 0):
                    raise ValueError(
                        'numerator must be less than the denominator',
                    )
                return denominator

        class MarkCode(BaseModel):
            unknown: Annotated[Optional[str], Field(None, max_length=32)]
            ean8: Annotated[Optional[str], Field(None, pattern=r'^[0-9]{8}$')]
            ean13: Annotated[
                Optional[str],
                Field(None, pattern=r'^[0-9]{13}$'),
            ]
            itf14: Annotated[
                Optional[str],
                Field(None, pattern=r'^[0-9]{14}$'),
            ]
            gs10: Annotated[Optional[str], Field(None, max_length=38)]
            gs1m: Annotated[Optional[str], Field(None, max_length=200)]
            short: Annotated[Optional[str], Field(None, max_length=38)]
            fur: Annotated[
                Optional[str],
                Field(
                    None,
                    pattern=r'^[A-Z0-9]{2}-\d{6}-[A-Z0-9]{10}$',
                ),
            ]
            egais20: Annotated[
                Optional[str],
                Field(None, min_length=23, max_length=23),
            ]
            egais30: Annotated[
                Optional[str],
                Field(None, min_length=14, max_length=14),
            ]

        class AgentInfoAlt(AgentInfo):
            type: AgentType

        measure: Measure
        payment_object: PaymentObjectInt
        supplier_info: Annotated[
            Optional[ItemSupplierInfo],
            Field(default=None),
        ]
        mark_quantity: Annotated[Optional[MarkQuantity], Field(default=None)]
        mark_processing_mode: Annotated[Optional[str], Field(pattern='^0$')]
        sectoral_item_props: Annotated[
            Optional[List[SectoralProp]],
            Field(
                default=None,
            ),
        ]
        mark_code: Annotated[Optional[MarkCode], Field(default=None)]
        agent_info: Annotated[Optional[AgentInfoAlt], Field(default=None)]

        @field_validator('mark_code')
        @classmethod
        def validate_mark_code(cls, value):
            if all(el is None for el in value.model_dump().values()):
                raise ValueError("Mark code can't be empty")
            return value

    class OperatingCheckProp(BaseModel):
        name: Annotated[str, Field(pattern=r'^0$')]
        value: Annotated[str, Field(max_length=64)]
        timestamp: str

        @field_validator('timestamp')  # noqa
        @classmethod
        def check_timestamp_format(cls, value: str) -> str:
            datetime.strptime(value, '%d.%m.%Y %H:%M:%S')
            return value

    company: Company
    items: List[Item]
    operating_check_props: Annotated[
        Optional[OperatingCheckProp],
        Field(default=None),
    ]
    sectoral_check_props: Annotated[
        Optional[List[SectoralProp]],
        Field(
            default=None,
        ),
    ]
    vats: Annotated[Optional[List[VatRequiredType]], Field(None, max_length=6)]
