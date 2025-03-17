import hmac
import json
from hashlib import sha256
from typing import Any
from typing import Dict
from typing import Optional
from typing import Union


def get_signature_body(
    method: str,
    url: str,
    site_id: int,
    data: Union[str, Dict[str, Any]],
    request_id: Optional[str],
) -> bytes:
    if request_id is None:
        result_string = (
            f'{method.upper()}\n{url}\n{site_id}\n{json.dumps(data)}'
        )
    else:
        url = url.format(endpoint=url.lstrip('/'))
        result_string = (
            f'{method.upper()}\n/{url}\n{site_id}\n{request_id}\n{data}'
        )
    return result_string.encode()


def get_signature(
    method: str,
    url: str,
    site_id: int,
    data: Union[str, Dict[str, Any]],
    secret_key: str,
    request_id: Optional[str] = None,
):
    signature = hmac.new(
        key=secret_key.encode(),
        msg=get_signature_body(method, url, site_id, data, request_id),
        digestmod=sha256,
    )
    return signature.hexdigest()
