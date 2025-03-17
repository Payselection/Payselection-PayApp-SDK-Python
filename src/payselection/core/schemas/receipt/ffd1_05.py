from typing import List
from typing import Optional

from pydantic import Field
from pydantic import field_validator
from typing_extensions import Annotated

from payselection.core.schemas.receipt.item import VatAllRequired
from payselection.core.schemas.receipt.receipt_data import AgentInfo
from payselection.core.schemas.receipt.receipt_data import BaseFFD
from payselection.core.schemas.schema import PhonesSchema


class FFD1_05(BaseFFD):
    class SupplierInfo(PhonesSchema):
        pass

    agent_info: Annotated[Optional[AgentInfo], Field(default=None)]
    supplier_info: Annotated[Optional[SupplierInfo], Field(default=None)]
    vats: Annotated[Optional[List[VatAllRequired]], Field(None, max_length=6)]

    @field_validator('supplier_info')
    @classmethod
    def validate_supplier_info(
        cls,
        value: [Optional[SupplierInfo]],
        values,
    ) -> [Optional[SupplierInfo]]:
        if values.data.get('agent_info') is not None and value is None:
            raise ValueError(
                "parameter 'supplier_info' is required, "
                "if 'agent_info' is specified",
            )
        return value
