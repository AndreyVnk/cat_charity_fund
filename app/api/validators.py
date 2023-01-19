from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.models import CharityProject


async def check_name_duplicate(
    *,
    project_id: int = None,
    project_name: str,
    session: AsyncSession,
) -> None:
    project = await charity_project_crud.check_project_id_by_name(
        project_id=project_id, project_name=project_name, session=session
    )
    if project:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Проект с таким именем уже существует!'
        )


async def check_close_date(
) -> None:
    raise HTTPException(
        status_code=HTTPStatus.BAD_REQUEST,
        detail='Закрытый проект нельзя редактировать!'
    )


async def check_invested_amount(
    project_id: int,
    session: AsyncSession
) -> None:
    project = await charity_project_crud.check_invested_update(
        project_id, session
    )
    if project:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='В проект были внесены средства, не подлежит удалению!'
        )


async def check_project_exists(
    project_id: int,
    session: AsyncSession,
) -> CharityProject:
    project = await charity_project_crud.get(
        obj_id=project_id, session=session
    )
    if not project:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Проект не найден!'
        )
    return project
