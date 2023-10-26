from sqlalchemy import Column, ForeignKey, Integer, Text

from .base import PreBaseCharityDonation


class Donation(PreBaseCharityDonation):
    comment = Column(Text)
    user_id = Column(Integer, ForeignKey('user.id'))

    def __repr__(self):
        return (
            f'Пожертвование от {self.user_id} с целью{self.comment}. '
            f'{super().__repr__()}'
        )
