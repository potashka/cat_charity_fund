from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

import app.api.validators as validators
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charity_project import charityproject_crud
from app.crud.donation import donation_crud
from app.schemas.charity_project import (
    CharityProjectCreate,
    CharityProjectDB,
    CharityProjectUpdate,
)
from app.services.donation import distribute_donations

router = APIRouter()


@router.get(
    '/',
    response_model=list[CharityProjectDB],
    response_model_exclude_none=True,
    summary='Просмотр всего списка проектов'
)
async def get_all_charity_projects(
    session: AsyncSession = Depends(get_async_session),
):
    return await charityproject_crud.get_multi(session)


@router.post(
    '/',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
    summary='Создает благотворительный проект'
)
async def create_new_charityproject(
    charityproject: CharityProjectCreate,
    session: AsyncSession = Depends(get_async_session),
):
    """
    Только для суперъюзеров
    """
    await validators.check_name_duplicate(charityproject.name, session)
    new_project = await charityproject_crud.create(
        charityproject, session, False
    )
    session.add_all(
        distribute_donations(
            new_project,
            await donation_crud.get_open_objects(session=session)
        )
    )
    await session.commit()
    await session.refresh(new_project)
    return new_project


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
    summary=(
        'Редактирование проекта'
    )
)
async def partially_update_charitypoject(
    project_id: int,
    obj_in: CharityProjectUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    """
    Только для суперъюзеров
    """
    charityproject = await validators.check_charityproject_exists(project_id, session)
    validators.check_charityproject_closed(charityproject)
    if obj_in.full_amount is not None:
        validators.check_full_amount_to_update(
            charityproject, obj_in.full_amount, session
        )
    if obj_in.name is not None:
        await validators.check_name_duplicate(obj_in.name, session)
    updated_project = await charityproject_crud.update(charityproject, obj_in, session)
    await session.refresh(updated_project)
    return updated_project


@router.delete(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
    summary='Удаление проекта'
)
async def delete_charityproject(
    project_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    """
    Только для суперъюзеров
    """
    charityproject = await validators.check_charityproject_exists(project_id, session)
    await validators.check_charityproject_to_delete(project_id, session)

    charityproject_deleted = await charityproject_crud.remove(
        charityproject, session
    )
    return charityproject_deleted
