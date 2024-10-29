from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

from src.models import TimedBaseModel
from src.subscriptions.schemas import Subscription_Type


class Subscription(TimedBaseModel):
    subscriber_id: Mapped[int] = mapped_column(
        ForeignKey("user.id", ondelete="CASCADE"),
        nullable=False,
        primary_key=True
    )
    schedule_id: Mapped[int] = mapped_column(
        ForeignKey("schedule.id", ondelete="CASCADE"),
        nullable=False,
        primary_key=True
    )
    subscription_type: Mapped["Subscription_Type"] = mapped_column(nullable=False, default=Subscription_Type.FOLLOWER)

    # association between Subscription -> Subscriber
    subscriber: Mapped["User"] = relationship(back_populates="subscription_associations", lazy="selectin")

    # association between Subscription -> Schedule
    schedule: Mapped["Schedule"] = relationship(back_populates="subscription_associations", lazy="selectin")