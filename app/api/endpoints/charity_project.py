from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (check_close_date, check_invested_amount,
                                check_name_duplicate, check_project_exists)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charity_project import charity_project_crud
from app.models import Donation
from app.schemas.charity_project import (CharityProjectCreate,
                                         CharityProjectDB,
                                         CharityProjectUpdate)
from app.services.investments import investment

router = APIRouter()


@router.get(
    '/',
    response_model=list[CharityProjectDB],
    response_model_exclude_none=True,
)
async def get_all_projects(
    session: AsyncSession = Depends(get_async_session)
):
    all_projects = await charity_project_crud.get_multi(session)
    return all_projects


@router.post(
    '/',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def create_new_project(
    obj_in: CharityProjectCreate,
    session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров."""
    await check_name_duplicate(project_name=obj_in.name, session=session)

    new_project = await charity_project_crud.create(obj_in, session)
    new_project = await investment(
        obj_in=new_project, model_db=Donation, session=session
    )
    return new_project


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)]
)
async def partially_update_project(
        project_id: int,
        obj_in: CharityProjectUpdate,
        session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров."""
    project = await check_project_exists(
        project_id, session
    )

    if obj_in.name:
        await check_name_duplicate(
            project_id=project_id, project_name=obj_in.name, session=session
        )

    if project.close_date:
        check_close_date()

    project = await charity_project_crud.update(
        project, obj_in, session
    )
    return project


@router.delete(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)]
)
async def remove_project(
        project_id: int,
        session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров."""
    project = await check_project_exists(
        project_id, session
    )

    await check_invested_amount(project_id=project_id, session=session)

    project = await charity_project_crud.remove(
        project, session
    )
    return project
