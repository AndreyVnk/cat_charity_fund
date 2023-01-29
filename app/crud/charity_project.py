from datetime import datetime
from typing import Optional

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import NULL_VALUE
from app.crud.base import CRUDBase
from app.models import CharityProject


class CRUDMeetingRoom(CRUDBase):

    async def check_project_id_by_name(
            self,
            *,
            project_id: int = None,
            project_name: str,
            session: AsyncSession,
    ) -> Optional[int]:
        stmt = select(CharityProject.id).where(
            CharityProject.name == project_name
        )
        if project_id:
            stmt = stmt.where(
                CharityProject.id != project_id
            )
        project = await session.execute(stmt)
        return project.scalars().first()

    async def check_invested_update(
            self,
            project_id: int,
            session: AsyncSession
    ) -> CharityProject:
        projects = await session.execute(
            select(CharityProject).where(
                CharityProject.id == project_id,
                CharityProject.invested_amount != NULL_VALUE
            )
        )
        return projects.scalars().first()

    async def get_projects_by_completion_rate(
            self,
            session: AsyncSession,
    ) -> list[list[str]]:
        projects = await session.execute(
            select(
                [
                    CharityProject.name,
                    (func.round(
                        (func.julianday(
                            CharityProject.close_date
                        ) - func.julianday(
                            CharityProject.create_date
                        )) * 86400
                    )
                    ).label('date_diff'),
                    CharityProject.description
                ]
            ).where(
                CharityProject.fully_invested != NULL_VALUE
            ).order_by('date_diff')
        )
        projects = [
            [
                row[0],
                str(
                    datetime.fromtimestamp(
                        int(row[1])
                    ) - datetime.fromtimestamp(0)
                ),
                row[2]
            ] for row in projects
        ]
        return projects


charity_project_crud = CRUDMeetingRoom(CharityProject)
