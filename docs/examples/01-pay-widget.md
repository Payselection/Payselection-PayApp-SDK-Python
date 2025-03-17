## Платежный виджет (PayWidget)

[Пример запроса в документации](https://api.payselection.com/#tag/Platezhnyj-vidzhet-or-PayWidget/operation/Create)

Метод создания платежа, который позволяет провести оплату

```python
 PayWidget.create(
    {
        "request_id": "16786c74-e777-4dcf-8b05-ce65b1d8f375",
        "payment_request": {
            "order_id": "string",
            "amount": "123.45",
            "currency": "USD",
            "description": "string",
            "rebill_flag": True,
            "extra_data": {
                "return_url": "https://site.com/",
                "success_url": "https://site.com/",
                "decline_url": "https://site.com/",
                "webhook_url": "https://webhook.site/94a06b69",
                "short_description": {
                    "ru": "string",
                    "en": "string"
                },
            }
        },
)
```
