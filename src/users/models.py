from typing import List

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import String
from sqlalchemy.orm import mapped_column, Mapped, relationship

from src.models import TimedBaseModel


class User(SQLAlchemyBaseUserTable[int], TimedBaseModel):
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    surname: Mapped[str] = mapped_column(String(50), nullable=False)

    schedules: Mapped[List["Schedule"]] = relationship(
        back_populates="owner",
        lazy="selectin",
        cascade="all, delete-orphan"
    )

    subscriptions: Mapped[List["Schedule"]] = relationship(
        secondary="subscription",
        back_populates="subscribers",
        lazy="selectin"
    )

    subscription_associations: Mapped[List["Subscription"]] = relationship(
        back_populates="subscriber",
        cascade="all, delete-orphan"
    )

