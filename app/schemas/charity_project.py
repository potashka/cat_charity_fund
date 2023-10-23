from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, Field, PositiveInt


class CharityProjectBase(BaseModel):
    name: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = Field(None)
    full_amount: Optional[PositiveInt]

    class Config:
        extra = Extra.forbid
        min_anystr_length = 1


class CharityProjectCreate(CharityProjectBase):
    name: str = Field(..., max_length=100)
    description: str = Field(..., )
    full_amount: PositiveInt

    class Config:
        schema_extra = {
            'example': {
                'name': 'Размножающиеся кошки',
                'description': 'Деньги собираются на семинары о контрацептивах',
                'full_amount': 1000000
            }
        }


class CharityProjectDB(CharityProjectCreate):
    id: int
    invested_amount: int
    fully_invested: bool
    create_date: datetime
    close_date: Optional[datetime]

    class Config:
        orm_mode = True


class CharityProjectUpdate(CharityProjectBase):

    class Config:
        schema_extra = {
            'example': {
                'name': 'Жирные коты',
                'description': 'Лекции о правильном питании',
                'full_amount': 1000000
            }
        }
