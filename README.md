## PaySelection SDK for Python

[![Latest Stable Version](https://img.shields.io/pypi/v/payselection.svg)](https://pypi.org/project/payselection/)
[![License](https://img.shields.io/pypi/l/payselection.svg)](https://github.com/Payselection/Payselection-PayApp-SDK-Python)

PaySelection SDK позволяет интегрировать работу с платежами для приложений, написанных с помощью Python

## Требования

1. Python >= 3.7
2. pip

## Установка
### C помощью pip

1. Установите pip.
2. В консоли выполните команду
```bash
pip install --upgrade payselection
```

## Начало работы

1. Импортируйте модуль
```python
import payselection
```
2. Установите данные для конфигурации
```python
from payselection import Configuration

Configuration.configure(
    {
        'site_id': <ID сайта>,
        'secret_key': <Секретный ключ сайта>,
        'public_key': <Публичный ключ сайта>,
        'merchant_url_address': <URL-адрес сайта ТСПа>,
    }
)
```

### Полезные ссылки

[Личный кабинет](https://merchant.payselection.com/login/)

[Разработчикам](https://api.payselection.com/#section/Request-signature)

### Поддержка

По возникающим вопросам технического характера обращайтесь на support@payselection.com
