import enum

from src.schemas import TimedBaseScheme, BaseScheme


class Subscription_Type(enum.Enum):
    FOLLOWER = "follower"
    OWNER = "owner"


class SubscriptionBase(BaseScheme):
    pass


class SubscriptionCreate(SubscriptionBase):
    subscriber_id: int
    schedule_id: int
    subscription_type: Subscription_Type


from src.users.schemas import UserRead


class SubscriberRead(SubscriptionBase, TimedBaseScheme):
    id: int
    subscription_type: Subscription_Type

    subscriber: 'UserRead'


from src.schedules.schemas import ScheduleRead


class SubscriptionScheduleRead(SubscriptionBase, TimedBaseScheme):
    id: int
    subscription_type: Subscription_Type

    schedule: 'ScheduleRead'


class SubscriptionRead(SubscriberRead, SubscriptionScheduleRead):
    pass