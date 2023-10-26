from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, Field, PositiveInt


class DonationBase(BaseModel):
    full_amount: Optional[PositiveInt]
    comment: Optional[str]

    class Config:
        extra = Extra.forbid


class DonationCreate(DonationBase):
    invested_amount: int = Field(default=0)
    full_amount: PositiveInt

    class Config:
        schema_extra = {
            'example': {
                'comment': 'To you for chimichangas',
                'full_amount': 55
            }
        }


class DonationDB(DonationCreate):
    id: int
    user_id: Optional[int]
    invested_amount: int
    fully_invested: bool
    create_date: datetime
    close_date: Optional[datetime]

    class Config:
        orm_mode = True
