Одностадийная операция оплаты — платеж, состоящий из единственной операции — прямого списания средств с карты
Покупателя. Для включения рекуррентных платежей есть возможность задать rebillFlag.

[Пример запроса в документации](https://api.payselection.com/#tag/Operacii/operation/Pay)

```python
card_data = {
    'TransactionDetails': {
        'Amount': '123.45',
        'Currency': 'USD',
    },
    'PaymentMethod': 'Card',
    'PaymentDetails': {
        'CardholderName': 'Card Holder',
        'CardNumber': '5260111696757102',
        'CVC': '666',
        'ExpMonth': '06',
        'ExpYear': '30',
    },
    'MessageExpiration': datetime.now().timestamp() * 1000 + 86400000,
}

Pay.pay(
    params={
        "request_id": "8e8ae1e1-e057-4ce7-87e8-1387704c5872",
        "order_id": "string",
        "amount": "123.45",
        "currency": "USD",
        "description": "string",
        "rebill_flag": False,
        "customer_info": {
            "email": "user@example.com",
            "receipt_email": "user@example.com",
            "is_send_receipt": True,
            "phone": "+79999999999",
            "language": "en",
            "address": "string",
            "town": "string",
            "zip": "string",
            "country": "RUS",
            "ip": "192.168.0.1",
            "user_id": "string",
            "first_name": "string",
            "last_name": "string",
            "date_of_birth": "string"
        },
        "extra_data": {
            "return_url": "https://api.payselection.com/",
            "webhook_url": "https://webhook.site/94a06b69",
            "screen_height": "768",
            "screen_width": "1024",
            "challenge_window_size": 5,
            "time_zone_offset": -180,
            "color_depth": 8,
            "region": "ru",
            "user_agent": "Mozilla/5.0+(Macintosh;+Intel+Mac+OS+X+10_15_5)+AppleWebKit/527.36+(KHTML,+like+Gecko)+Chrome83.0.4103.116+Safari/537.36",
            "accept_header": "text/html",
            "java_enabled": True,
            "javascript_enabled": True
        },
        "payment_method": "Cryptogram",
    },
    card_data=card_data
)
```

Двухстадийная операция оплаты — платеж, который включает выполнение двух операций: холдирование средств на карте и
завершение авторизации — списание.

[Пример запроса в документации](https://api.payselection.com/#tag/Operacii/operation/Block)

```python
card_data = {
    'TransactionDetails': {
        'Amount': '123.45',
        'Currency': 'USD',
    },
    'PaymentMethod': 'Card',
    'PaymentDetails': {
        'CardholderName': 'Card Holder',
        'CardNumber': '5260111696757102',
        'CVC': '666',
        'ExpMonth': '06',
        'ExpYear': '30',
    },
    'MessageExpiration': datetime.now().timestamp() * 1000 + 86400000,
}

Pay.block(
    {
        "request_id": "ec458395-9786-406d-9cc3-7661ecaf700f",
        "order_id": "string",
        "amount": "123.45",
        "currency": "USD",
        "description": "string",
        "rebill_flag": False,
        "customer_info": {
            "email": "user@example.com",
            "receipt_email": "user@example.com",
            "is_send_receipt": True,
            "phone": "+79999999999",
            "language": "en",
            "address": "string",
            "town": "string",
            "zip": "string",
            "country": "RUS",
            "ip": "192.168.0.1",
            "user_id": "string",
            "first_name": "string",
            "last_name": "string",
            "date_of_birth": "string"
        },
        "payment_method": "CryptogramRSA",
    },
    card_data=card_data
)
```

Операция для списания средств по ранее сохраненной карте (через RebillId). Для создания RebillId в родительской
транзакции необходимо задать признак rebillFlag. RebillId возвращается в вебхуке. Метод позволяет надежно шифровать
карточные данные и обеспечивать безопасность платежей.

[Пример запроса в документации](https://api.payselection.com/#tag/Operacii/operation/Rebill)

```python
Pay.rebill(
    {
        "request_id": "0c9f7952-e0d0-47e0-911b-a67a30c09c26",
        "order_id": "string",
        "amount": "123.45",
        "currency": "USD",
        "description": "string",
        "rebill_id": "PS00000000000001",
        "payment_type": "Pay",
        "webhook_url": "https://webhook.site/94a06b69"
    }
)
```

Операция для завершения списания средств с карты по одностадийным (Pay) и двухстадийным (Block) операциям оплаты после
получения результата аутентификации 3D-Secure от Банка.

[Пример запроса в документации](https://api.payselection.com/#tag/Operacii/operation/Confirm)

```python
Pay.confirm(
    {
        "request_id": "2bcb50b2-1a52-4f3d-8945-791f70ad0f28",
        "transaction_id": "PS00000000000001",
        "order_id": "string",
        "payment_response": "string",
        "md": "string"
    }
)
```


Операция Refund используется для возврата денежных средств, которые были списаны с помощью одностадийной Pay или
двухстадийной Block операции проведения платежа.

[Пример запроса в документации](https://api.payselection.com/#tag/Operacii/operation/Refund)

```python
Pay.refund(
    {
        "request_id": "e30c9c42-687f-4e4a-8870-68f4a61dd43d",
        "transaction_id": "PS00000000000001",
        "amount": "123.45",
        "currency": "USD",
        "webhook_url": "https://webhook.site/94a06b69"
    }
)
```

Операция для отмены блокировки денежных средств при двухстадийной операции оплаты Block.

[Пример запроса в документации](https://api.payselection.com/#tag/Operacii/operation/Cancel)

```python
Pay.cancel(
    {
        "request_id": "ffb4761a-5ea4-4662-bd32-badfafdb59c2",
        "transaction_id": "PS00000000000001",
        "amount": "123.45",
        "currency": "USD",
        "webhook_url": "https://webhook.site/94a06b69"
    }
)
```

Операция по списанию средств с карты в рамках проведенного ранее холдирования.

[Пример запроса в документации](https://api.payselection.com/#tag/Operacii/operation/Charge)

```python
Pay.charge(
    {
        "request_id": "8150f3db-7515-48bc-8bda-e07b453c9a3f",
        "transaction_id": "PS00000000000001",
        "amount": "123.45",
        "currency": "USD",
        "webhook_url": "https://webhook.site/94a06b69"
    }
)
```

Операция по деактивации уникального RebillId (токена). Метод отменяет все активные регулярные оплаты (подписки) без
возможности их возобновления.

[Пример запроса в документации](https://api.payselection.com/#tag/Operacii/operation/Unsubscribe)

```python
Pay.unsubscribe(
    {
        "request_id": "a156f221-e2b3-4763-a519-7a10081685c4",
        "rebill_id": "PS00000000000001",
    }
)
```
