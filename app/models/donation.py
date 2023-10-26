from sqlalchemy import Column, ForeignKey, Integer, Text

# from app.core.consts import DONATION
from .base import PreBaseCharityDonation


class Donation(PreBaseCharityDonation):
    # __table_name__ = DONATION
    comment = Column(Text)
    user_id = Column(Integer, ForeignKey('user.id'))

    def __repr__(self):
        return f'Пожертвование. {super().__repr__()}'
