Запрос используется для получения информации о текущем статусе по идентификатору заказа orderId, если ТСП предварительно
передает необходимое значение идентификатора в запросе по операции.

[Пример запроса в документации](https://api.payselection.com/#tag/Operacii/operation/OrderId)

```python
CheckTransactionStatus.check_by_order_id(
    {
        'request_id': 'f8d7d24c-871b-4d89-acb8-0e4e16d1f91b',
        'order_id': 'string',
    }
)
```

Запрос используется для получения информации о текущем статусе по идентификатору транзакции TransactionId. Идентификатор
присваивается операции после начала процесса авторизации в банке

[Пример запроса в документации](https://api.payselection.com/#tag/Operacii/operation/TransactionId)

```python
CheckTransactionStatus.check_by_transaction_id(
    {
        'request_id': '455b05dc-91b8-47fd-b84b-0eeec30ae077',
        'transaction_id': 'PS00000000000001',
    }
)
```

Расширенный запрос используется для получения информации о текущем статусе по идентификатору заказа orderId

[Пример запроса в документации](https://api.payselection.com/#tag/Operacii/operation/OrderId%20(extended))

```python
CheckTransactionStatus.check_by_order_id_extended(
    {
        "request_id": "14e93033-b1d6-4e9a-bcab-01d8e5cbbc2d",
        "order_id": "string",
    }
)
```

Расширенный запрос используется для получения информации о текущем статусе по идентификатору транзакции TransactionId

[Пример запроса в документации](https://api.payselection.com/#tag/Operacii/operation/TransactionId%20(extended))

```python
CheckTransactionStatus.check_by_transaction_id_extended(
    {
        "request_id": "455be948-8e28-4b24-ad47-b3b517cd119a",
        "transaction_id": "PS00000000000001",
    }
)
```

Расширенный запрос используется для получения статуса транзакций по выбранному диапазону дат. Для включения данного
метода, пожалуйста, обратитесь в техническую поддержку (support@payselection.com).

[Пример запроса в документации](https://api.payselection.com/#tag/Operacii/operation/Transactions%20(by-dates))

```python
CheckTransactionStatus.check_by_dates(
    {
        "request_id": "dfb16678-8edf-426d-87bd-d457735ae6ef",
        "start_creation_date": "2022-12-31T00:00:00",
        "end_creation_date": "2023-12-31T00:00:00",
        "page_number": 1,
        "time_zone": "Africa/Abidjan",
        "statuses": [
            "success",
            "voided",
            "preauthorized",
            "pending",
            "declined",
            "wait_for_3ds",
            "redirect"
        ]

    }
)
```
