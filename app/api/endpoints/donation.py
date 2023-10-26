from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud.charity_project import charityproject_crud
from app.crud.donation import donation_crud
from app.models import User
from app.schemas.donation import DonationCreate, DonationDB
from app.services.donation import distribute_donations

EXCLUDE_DONATIONDB = (
    'user_id',
    'invested_amount',
    'fully_invested',
    'close_date'
)


router = APIRouter()


@router.get(
    '/',
    response_model=list[DonationDB],
    dependencies=[Depends(current_superuser)],
    response_model_exclude_none=True,
    summary='Список пожертвований'
)
async def get_all_donations(
    session: AsyncSession = Depends(get_async_session),
):
    """
    Только для суперъюзеров
    """
    return await donation_crud.get_multi(session)


@router.get(
    '/my',
    response_model=list[DonationDB],
    dependencies=[Depends(current_user)],
    response_model_exclude={*EXCLUDE_DONATIONDB},
    summary='Список пожертвований авторизованного пользователя'
)
async def get_my_donations(
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
):
    return await donation_crud.get_user_donations(
        user=user, session=session
    )


@router.post(
    '/',
    response_model=DonationDB,
    response_model_exclude_none=True,
    response_model_exclude={*EXCLUDE_DONATIONDB},
    summary='Пожертвовать'
)
async def create_new_donation(
    donation: DonationCreate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    new_donation = await donation_crud.create(donation, session, False, user)
    session.add_all(
        distribute_donations(
            new_donation,
            await charityproject_crud.get_open_objects(session=session)
        )
    )
    await session.commit()
    await session.refresh(new_donation)
    return new_donation
