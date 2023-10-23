from datetime import datetime
from typing import Union

from app.models import CharityProject, Donation


def distribute_donations(
    obj_in: Union[CharityProject, Donation],
    open_objects: list[Union[CharityProject, Donation]]
) -> list[Union[CharityProject, Donation]]:

    def update(
        obj: Union[CharityProject, Donation],
        amount: int,
    ) -> None:
        obj.invested_amount = (obj.invested_amount or 0) + amount
        if obj.full_amount == obj.invested_amount:
            obj.fully_invested = True
            obj.close_date = datetime.now()

    updated_objects = []
    for source in open_objects:
        amount = min(
            source.full_amount - (source.invested_amount or 0),
            obj_in.full_amount - (obj_in.invested_amount or 0))
        update(obj_in, amount)
        update(source, amount)
        updated_objects.append(source)
        if obj_in.fully_invested:
            break
    return updated_objects
