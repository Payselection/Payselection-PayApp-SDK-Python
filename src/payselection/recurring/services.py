from typing import Any
from typing import Dict

from requests import Response

from payselection.core.service import BaseService
from payselection.core.urls import GatewayUrlsBuilder
from payselection.recurring.enum import SearchIdentifier
from payselection.recurring.schema import RecurringChangeSchema
from payselection.recurring.schema import RecurringIdRequestSchema
from payselection.recurring.schema import RecurringSchema
from payselection.recurring.schema import SEARCH_SCHEMAS


class Recurring(BaseService):
    def __init__(self):
        super().__init__(GatewayUrlsBuilder())

    @classmethod
    def recurring(cls, params: Dict[str, Any]) -> Response:
        """
        Registers regular payment RecurringId
        (subscription) within the created RebillId.
        """
        return cls().call_api(RecurringSchema(**params))

    @classmethod
    def unsubscribe(cls, params: Dict[str, Any]) -> Response:
        """
        Cancels the regular payment of RecurringId
         (subscription) within the created RebillId
        """
        return cls().call_api(RecurringIdRequestSchema(**params))

    @classmethod
    def search(
        cls,
        request_id: str,
        identifier: SearchIdentifier,
        identifier_value: str,
    ) -> Response:
        """
        Searches for regular payment
         (subscription) based on the selected parameter.
        """
        return cls().call_api(
            SEARCH_SCHEMAS[identifier](
                **{
                    'request_id': request_id,
                    identifier: identifier_value,
                }
            ),
        )

    @classmethod
    def change(cls, params: Dict[str, Any]) -> Response:
        """
        Changes parameters of the regular payment (subscription)
        """
        return cls().call_api(RecurringChangeSchema(**params))
