from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_user
from app.crud.donation import donation_crud
from app.models import CharityProject, User
from app.schemas.donation import DonationCreate, DonationDB
from app.services.investments import investment

router = APIRouter()


@router.get(
    '/',
    response_model=list[DonationDB],
)
async def get_all_donations(
    session: AsyncSession = Depends(get_async_session)
):
    all_donations = await donation_crud.get_multi(session)
    return all_donations


@router.get(
    '/my',
    response_model=list[DonationDB],
    response_model_exclude={
        'user_id', 'invested_amount', 'fully_invested'
    }
)
async def get_user_donations(
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    user_donations = await donation_crud.get_by_user(
        user=user, session=session,
    )
    return user_donations


@router.post(
    '/',
    response_model=DonationDB,
    response_model_exclude={
        'user_id', 'invested_amount', 'fully_invested'
    },
    response_model_exclude_none=True,
)
async def create_new_donation(
    obj_in: DonationCreate,
    session: AsyncSession = Depends(get_async_session),
):
    """Only for users."""
    new_donation = await donation_crud.create(obj_in, session)
    new_donation = await investment(
        obj_in=new_donation, model_db=CharityProject, session=session
    )
    return new_donation
