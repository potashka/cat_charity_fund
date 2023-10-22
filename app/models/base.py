from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer

from app.core.db import Base

INVESTED_AMOUNT_DEFAULT = 0


class PreBaseCharityDonation(Base):
    __abstract__ = True

    full_amount = Column(Integer, nullable=False)
    invested_amount = Column(Integer, default=INVESTED_AMOUNT_DEFAULT)
    fully_invested = Column(Boolean, default=False)
    create_date = Column(DateTime, default=datetime.now)
    close_date = Column(DateTime)

    def __repr__(self):
        return (
            f'Бюджет {self.full_amount}, '
            f'Инвестировано {self.invested_amount}'
        )