from sqlalchemy import Column, String, Text

from app.core.consts import CHARITY_PROJECT
from .base import PreBaseCharityDonation


class CharityProject(PreBaseCharityDonation):
    __table_name__ = CHARITY_PROJECT
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=False)
