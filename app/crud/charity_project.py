from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.charity_project import CharityProject


class CRUDCharityProject(CRUDBase):

    async def get_charityproject_by_name(
            self,
            charityproject_name: str,
            session: AsyncSession
    ) -> Optional[CharityProject]:
        charityproject = await session.execute(
            select(self.model).where(
                self.model.name == charityproject_name
            )
        )
        return charityproject.scalars().first()


charityproject_crud = CRUDCharityProject(CharityProject)