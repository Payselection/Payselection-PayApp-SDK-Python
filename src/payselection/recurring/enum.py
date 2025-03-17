from enum import Enum


class SearchIdentifier(str, Enum):
    RebillId = 'rebill_id'
    RecurringId = 'recurring_id'
    AccountId = 'account_id'
