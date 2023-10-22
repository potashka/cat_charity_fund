from datetime import datetime
from typing import Union

from sqlalchemy import false, select
from sqlalchemy.ext.asyncio import AsyncSession
# from sqlalchemy.sql.expression import not_

from app.models import CharityProject, Donation


async def close_object(
        obj: Union[CharityProject, Donation],
) -> None:
    obj.fully_invested = True
    obj.close_date = datetime.now()


async def get_not_closed_objects(
    model: Union[CharityProject, Donation],
    session: AsyncSession,
) -> list[Union[CharityProject, Donation]]:
    """charity_projects = (
        select(model).where(not_(model.fully_invested))
        .order_by(model.create_date)
    )
    return charity_projects
    """
    open_objs = await session.execute(
        select(model).where(
            model.fully_invested == false()
        ).order_by(model.create_date)
    )
    return open_objs.scalars().all()


async def distribute_donations(
    obj_in: Union[CharityProject, Donation],
    session: AsyncSession
) -> Union[CharityProject, Donation]:
    model = (
        CharityProject if isinstance(obj_in, Donation) else Donation
    )
    open_objects = await get_not_closed_objects(
        model, session
    )
    if open_objects:
        available_amount = obj_in.full_amount
        for obj in open_objects:
            balance = obj.full_amount - obj.invested_amount
            donation = min(
                balance,
                available_amount
            )
            available_amount -= donation
            obj.invested_amount += donation
            obj_in.invested_amount += donation

            if obj.full_amount == obj.invested_amount:
                await close_object(obj)

            if not available_amount:
                await close_object(obj_in)
                break
        await session.commit()
    return obj_in
