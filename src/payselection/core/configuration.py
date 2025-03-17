from typing import Dict
from typing import Union

from payselection.core.schemas.schema import MerchantConfiguration


class Configuration:
    """
    A class representing the configuration.
    """

    site_id = None
    secret_key = None
    public_key = None
    merchant_url_address = None
    timeout = 1800

    @staticmethod
    def configure(data: Dict[str, Union[str, int]], *args, **kwargs):
        config = MerchantConfiguration(**data)
        Configuration.site_id = config.site_id
        Configuration.secret_key = config.secret_key
        Configuration.public_key = config.public_key
        Configuration.merchant_url_address = config.merchant_url_address
        Configuration.timeout = kwargs.get('timeout', 1800)
