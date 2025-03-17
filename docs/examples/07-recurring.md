Регистрация регулярной оплаты RecurringId (подписки) в рамках созданного RebillId

[Пример запроса в документации](https://api.payselection.com/#tag/Rekurrentnye-platezhi-or-Podpiski/operation/Recurring)

```python
Recurring.recurring(
    {
        "request_id": "2b5eaebc-2cf4-4301-8afa-793d23fea178",
        "rebill_id": "PS00000000000001",
        "amount": "123.45",
        "currency": "USD",
        "description": "string",
        "webhook_url": "https://webhook.site/94a06b69",
        "account_id": "order63",
        "email": "user@example.com",
        "start_date": "2023-01-11T13:38+0000",
        "interval": "5",
        "period": "day",
        "max_periods": "3"
    }
)
```

Операция для отмены регулярной оплаты RecurringId (подписки) в рамках созданного RebillId.

[Пример запроса в документации](https://api.payselection.com/#tag/Rekurrentnye-platezhi-or-Podpiski/operation/Recurring%20Unsubscribe)

```python
Recurring.unsubscribe(
    {
        "request_id": "9a7db6c2-9a8a-4b01-89ee-71dd34ce4dfe",
        "recurring_id": "1173",
    }
)
```

Поиск регулярной оплаты (подписки) по выбранному параметру.

[Пример запроса в документации](https://api.payselection.com/#tag/Rekurrentnye-platezhi-or-Podpiski/operation/Recurring%20Search)

```python
from payselection.recurring.enum import SearchIdentifier

Recurring.search('ae33699d-c7fc-415b-b134-083ef680957d', SearchIdentifier.RecurringId, "1173")
```

Изменение параметров регулярной оплаты (подписки).

[Пример запроса в документации](https://api.payselection.com/#tag/Rekurrentnye-platezhi-or-Podpiski/operation/Recurring%20Change)

```python
Recurring.change(
    {
        "request_id": "6d3c8834-00c8-4638-8bc5-c96a2ce5f27d",
        "recurring_id": "1173",
        "max_periods": "3",
        "start_date": "2023-01-11T13:38+0000",
        "interval": "5",
        "period": "day",
        "amount": "123.45"
    }
)
```
