from enum import Enum


class Event(str, Enum):
    REGISTER_RECURRING = 'RegisterRecurring'
    CHANGE_RECURRING_STATE = 'ChangeRecurringState'
    UNSUBSCRIBE_RECURRING = 'UnsubscribeRecurring'
    CHANGE_RECURRING_BY_MERCHANT = 'ChangeRecurringByMerchant'


class RecurringStatus(str, Enum):
    NEW = 'new'
    ACTIVE = 'active'
    COMPLETED = 'completed'
    TERMINATED = 'terminated'
    FAILED = 'failed'
    OVERDUE = 'overdue'
