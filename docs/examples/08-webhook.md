## Работа с входящими Webhook

Проверка подписи X-WEBHOOK-SIGNATURE

```python



class CheckWebhookSignature:
    async def __call__(self, request: Request):
        body = await request.body()
        site_id = request.headers.get('X-SITE-ID')
        sign = request.headers.get('X-WEBHOOK-SIGNATURE')
        data = {
            'method': request.method,
            'url': str(request.url),
            'site_id': site_id,
            'request_body': json.loads(body.decode("utf-8")),
        }
        WebhookSignature.verify_signature(
            sign,
            data,
            Configuration.secret_key,
        )

app = FastAPI(
    title='Webhook APP',
    version='0.1.0',
    docs_url='/docs',
)

webhook_router = APIRouter()

@webhook_router.post('/payment/')
async def get_payment_data(data: Dict[str, Any]) -> EventWebhookBase:
    return WebhookEvent.get_payment(data)

app.include_router(webhook_router, tags=['WEBHOOKS'], prefix=f'/test-webhook',
                   dependencies=[Depends(CheckWebhookSignature())])
```

### Прием входных данных

Webhook для операций

```python
webhook_payment = WebhookEvent.get_payment(
    {
        "payment_method": "Card",
        "payout_token": "49642b71-7b85-1bb4-a620-737b3f924249",
        "rebill_id": "PS00000000000001",
        "rrn": "string",
        "recurring_id": "1173",
        "subtype": "string",
        "card_masked": "stringstring",
        "card_holder": "Card Holder",
        "expiration_date": "string",
        "qr_code_string": "https%3A%2F%2Fqr.nspk.ru%2FAD10005VD436V4O88UDBFCKI0OD01A2Q%3Ftype%3D02%26bank%3D100000000017%26sum%3D1000%26cur%3DRUB%26crc%3D72F4",
        "sber_string": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAQAAAAEAAQMAAABmvDolAAAABlBMVEX///8AAABVwtN+AAACrUlEQVR42uyYPY68OhDECxF06CP4JnCx1cCIi5mb+AgOHSDqqZr50vxfjpHG0Wr0C7Zxubq68Tu5ErkJggg==",
        "sber_deep_link": "sberpay://invoicing/v2?bankInvoiceId=361071a8fcbd67&operationType=Web2App",
        "split_data": [
            {
                "submerchant_id": "string",
                "amount": "123.45",
                "description": "string"
            }
        ],
        "event": "Payment",
        "transaction_id": "PS00000000000001",
        "order_id": "string",
        "amount": "123.45",
        "currency": "USD",
        "service_id": "3453",
        "date_time": "17.02.2025 15:30:45",
        "is_test": 0,
        "email": "user@example.com",
        "phone": "+79999999999",
        "description": "string",
        "custom_fields": "ScreenHeight=1080;ScreenWidth=1920;JavaEnabled=false;TimeZoneOffset=-120;Region=ru-RU;ColorDepth=24;UserAgent=Mozilla%2F5.0%20%28Windows%20NT%206.1%3B%20Win64%3B%20x64%3B%20rv%3A108.0%29%20Gecko%2F20100101%20Firefox%2F108.0;acceptHeader=text%2Fhtml;javaScriptEnabled=true;Language=ru;IP=0.0.0.0;IsSendReceipt=false",
        "brand": "string",
        "country_code_alpha2": "RU",
        "bank": "string",
        "gate": "testbank"
    }
)
```

Webhook для подписок

```python
webhook_recurring = WebhookEvent.get_recurring(
    {
        "event": "RegisterRecurring",
        "rebill_id": "PS00000000000001",
        "amount": "123.45",
        "currency": "USD",
        "description": "string",
        "webhook_url": "https://webhook.site/94a06b69",
        "account_id": "order63",
        "email": "user@example.com",
        "start_date": "2025-03-11T13:38+0000",
        "interval": "5",
        "period": "day",
        "max_periods": "3",
        "recurring_id": "1173",
        "recurring_status": "new",
    }
)
```
