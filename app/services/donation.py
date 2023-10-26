from datetime import datetime
from typing import Optional

from app.models.base import PreBaseCharityDonation


def distribute_donations(
    obj_in: PreBaseCharityDonation,
    open_objects: list[Optional[PreBaseCharityDonation]]
) -> list[Optional[PreBaseCharityDonation]]:
    updated = []
    if obj_in.invested_amount is None:
        obj_in.invested_amount = 0
    for source in open_objects:
        amount = min(
            source.full_amount - source.invested_amount,
            obj_in.full_amount - obj_in.invested_amount)
        for obj in (obj_in, source):
            obj.invested_amount = obj.invested_amount + amount
            if obj.invested_amount < obj.full_amount:
                continue
            if obj.full_amount == obj.invested_amount:
                obj.fully_invested = True
                obj.close_date = datetime.now()
        updated.append(source)
        if obj_in.fully_invested:
            break
    return updated
