Original credit transaction (OCT) - это тип транзакции, при которой денежные средства переводятся на банковские карты физическим лицам

[Пример запроса в документации](https://api.payselection.com/#tag/Operacii/operation/Payout%20%7C%20%D0%92%D1%8B%D0%BF%D0%BB%D0%B0%D1%82%D1%8B%20%D0%BD%D0%B0%20%D0%BA%D0%B0%D1%80%D1%82%D1%83l)

```python
Payout.payout(
    {
        "request_id": "6235e0d4-c5cb-43a0-9930-23c0bc793199",
        "order_id": "string",
        "amount": "123.45",
        "currency": "USD",
        "description": "string",
        "customer_info": {
            "email": "user@example.com",
            "phone": "+79999999999",
            "language": "en",
            "address": "string",
            "town": "string",
            "zip": "string",
            "country": "RUS",
            "ip": "192.168.0.1",
            "first_name": "string",
            "last_name": "string",
            "date_of_birth": "string"
        },
        "payout_method": "Card",
        "payout_details": {
            "card_number": "4129436949329530",
            "cardholder_name": "Card Holder"
        }
    }
)
```

Операция проверки доступного баланса для Payout.

[Пример запроса в документации](https://api.payselection.com/#tag/Operacii/operation/Balance)

```python
Payout.balance(
    {
        "request_id": "5301caef-8e4e-420e-918f-0133c526fb20"
    }
)
```
