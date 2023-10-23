from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charityproject_crud
from app.models import CharityProject

FORBIDDEN_TO_DELETE = (
    'В проект были внесены средства, не подлежит удалению!'
)
FORBIDDEN_TO_UPDATE = 'Закрытый проект нельзя редактировать!'
INVALID_AMOUNT = (
    'Значение требуемой суммы не может быть меньше внесённой'
)
NAME_EXISTS = 'Проект с таким именем уже существует!'
PROJECT_NOT_FOUND = 'Проект не найден!'


async def check_name_duplicate(
    charityproject_name: str,
    session: AsyncSession,
) -> None:
    charityproject = await charityproject_crud.get_charityproject_by_name(
        charityproject_name,
        session
    )
    if charityproject:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=NAME_EXISTS,
        )


async def check_charityproject_exists(
    charityproject_id: int,
    session: AsyncSession,
) -> CharityProject:
    charityproject = await charityproject_crud.get(
        obj_id=charityproject_id, session=session
    )
    if charityproject is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=PROJECT_NOT_FOUND
        )
    return charityproject


async def check_charityproject_to_delete(
        charityproject_id: int,
        session: AsyncSession
) -> CharityProject:
    charityproject = await check_charityproject_exists(
        charityproject_id,
        session
    )
    if charityproject.invested_amount > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=FORBIDDEN_TO_DELETE
        )
    return charityproject


async def check_charityproject_closed(
        charityproject: CharityProject,
        # session: AsyncSession
) -> None:
    if charityproject.fully_invested:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=FORBIDDEN_TO_UPDATE,
        )


async def check_full_amount_to_update(
        charityproject: CharityProject,
        full_amount: int,
        session: AsyncSession,
):
    if charityproject.invested_amount > full_amount:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=INVALID_AMOUNT
        )
