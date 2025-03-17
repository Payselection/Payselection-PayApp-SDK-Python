class UrlsBuilder:
    BASE_URL = None
    ENDPOINTS = {}
    GET_METHOD = 'GET'
    POST_METHOD = 'POST'


class WebUrlsBuilder(UrlsBuilder):
    BASE_URL: str = 'https://webform.payselection.com'

    CREATE_PAYMENT: str = 'webpayments/create'
    CREATE_PAYLINK: str = 'webpayments/paylink_create'
    PAYLINK_VOID: str = 'webpayments/paylink_void'

    ENDPOINTS = {
        'PayWidget': {
            'create': (UrlsBuilder.POST_METHOD, CREATE_PAYMENT),
        },
        'PayLink': {
            'create': (UrlsBuilder.POST_METHOD, CREATE_PAYLINK),
            'void': (UrlsBuilder.POST_METHOD, PAYLINK_VOID),
        },
    }


class GatewayUrlsBuilder(UrlsBuilder):
    BASE_URL: str = 'https://gw.payselection.com'

    CHECK_STATUS_ORDER_ID: str = 'orders/{order_id}/extended'
    CHECK_STATUS_TRANSACTION_ID: str = 'transactions/{transaction_id}'
    CHECK_STATUS_ORDER_ID_EXTENDED: str = 'orders/{order_id}/extended'
    CHECK_STATUS_TRANSACTION_ID_EXTENDED: str = (
        'transactions/{transaction_id}/extended'
    )
    CHECK_STATUS_BY_DATES: str = 'transactions/by-dates'
    #
    PAY: str = 'payments/requests/single'
    BLOCK: str = 'payments/requests/block'
    REBILL: str = 'payments/requests/rebill'
    CONFIRM: str = 'payments/confirmation'
    REFUND: str = 'payments/refund'
    CANCEL: str = 'payments/cancellation'
    CHARGE: str = 'payments/charge'
    UNSUBSCRIBE: str = 'payments/unsubscribe'
    #
    PAYOUTS: str = 'payouts'
    BALANCE: str = 'balance'
    #
    GET_PUBLIC_KEY: str = 'rsa_crypto/get_public_key'
    GET_SBP_MEMBERS: str = 'sbp/{transaction_id}/get_sbp_members'
    #
    RECURRING: str = 'payments/recurring'
    RECURRING_UNSUBSCRIBE: str = 'payments/recurring/unsubscribe'
    RECURRING_SEARCH: str = 'payments/recurring/search'
    RECURRING_CHANGE: str = 'payments/recurring/change'

    ENDPOINTS = {
        'GatewayPayment': {
            'get_public_key': (UrlsBuilder.GET_METHOD, GET_PUBLIC_KEY),
            'get_sbp_members': (UrlsBuilder.GET_METHOD, GET_SBP_MEMBERS),
        },
        'CheckTransactionStatus': {
            'check_by_order_id': (
                UrlsBuilder.GET_METHOD,
                CHECK_STATUS_ORDER_ID,
            ),
            'check_by_transaction_id': (
                UrlsBuilder.GET_METHOD,
                CHECK_STATUS_TRANSACTION_ID,
            ),
            'check_by_order_id_extended': (
                UrlsBuilder.GET_METHOD,
                CHECK_STATUS_ORDER_ID_EXTENDED,
            ),
            'check_by_transaction_id_extended': (
                UrlsBuilder.GET_METHOD,
                CHECK_STATUS_TRANSACTION_ID_EXTENDED,
            ),
            'check_by_dates': (
                UrlsBuilder.POST_METHOD,
                CHECK_STATUS_BY_DATES,
            ),
        },
        'Pay': {
            'pay': (
                UrlsBuilder.POST_METHOD,
                PAY,
            ),
            'block': (
                UrlsBuilder.POST_METHOD,
                BLOCK,
            ),
            'rebill': (
                UrlsBuilder.POST_METHOD,
                REBILL,
            ),
            'confirm': (
                UrlsBuilder.POST_METHOD,
                CONFIRM,
            ),
            'refund': (
                UrlsBuilder.POST_METHOD,
                REFUND,
            ),
            'cancel': (
                UrlsBuilder.POST_METHOD,
                CANCEL,
            ),
            'charge': (
                UrlsBuilder.POST_METHOD,
                CHARGE,
            ),
            'unsubscribe': (
                UrlsBuilder.POST_METHOD,
                UNSUBSCRIBE,
            ),
        },
        'Payout': {
            'payout': (UrlsBuilder.POST_METHOD, PAYOUTS),
            'balance': (UrlsBuilder.GET_METHOD, BALANCE),
        },
        'Recurring': {
            'recurring': (UrlsBuilder.POST_METHOD, RECURRING),
            'unsubscribe': (UrlsBuilder.POST_METHOD, RECURRING_UNSUBSCRIBE),
            'search': (UrlsBuilder.POST_METHOD, RECURRING_SEARCH),
            'change': (UrlsBuilder.POST_METHOD, RECURRING_CHANGE),
        },
    }
