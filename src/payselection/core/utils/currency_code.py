from typing import Any
from typing import Dict

import pycountry
from pydantic import GetCoreSchemaHandler
from pydantic import GetJsonSchemaHandler
from pydantic_core import core_schema
from pydantic_core import PydanticCustomError


class ISO4217(str):
    """ISO4217 parses Currency in the [ISO 4217]
    (https://en.wikipedia.org/wiki/ISO_4217) format."""

    allowed_countries_list = [
        country.alpha_3 for country in pycountry.currencies
    ]
    allowed_currencies = set(allowed_countries_list)

    @classmethod
    def _validate(
        cls,
        currency_code: str,
        _: core_schema.ValidationInfo,
    ) -> str:
        """Validate a ISO 4217 language code from the provided str value.

        Args:
            currency_code: The str value to be validated.
            _: The Pydantic ValidationInfo.

        Returns:
            The validated ISO 4217 currency code.

        Raises:
            PydanticCustomError: If the ISO 4217 currency code is not valid.
        """
        currency_code = currency_code.upper()
        if currency_code not in cls.allowed_currencies:
            raise PydanticCustomError(
                'ISO4217',
                'Invalid ISO 4217 currency code. '
                'See https://en.wikipedia.org/wiki/ISO_4217',
            )
        return currency_code

    @classmethod
    def __get_pydantic_core_schema__(
        cls,
        _: Any,
        __: GetCoreSchemaHandler,
    ) -> core_schema.CoreSchema:
        return core_schema.with_info_after_validator_function(
            cls._validate,
            core_schema.str_schema(min_length=3, max_length=3),
        )

    @classmethod
    def __get_pydantic_json_schema__(
        cls,
        schema: core_schema.CoreSchema,
        handler: GetJsonSchemaHandler,
    ) -> Dict[str, Any]:
        json_schema = handler(schema)
        json_schema.update({'enum': cls.allowed_countries_list})
        return json_schema
