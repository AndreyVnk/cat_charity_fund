from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import FinancialBase


async def investment(
    obj_in: FinancialBase,
    model_db: FinancialBase,
    session: AsyncSession
) -> FinancialBase:
    source_db_all = await session.execute(
        select(model_db).where(
            model_db.fully_invested == False  # noqa
        ).order_by(model_db.create_date)
    )
    source_db_all = source_db_all.scalars().all()
    for source_db in source_db_all:
        obj_in, source_db = await distribution(
            obj_in, source_db
        )
        session.add(obj_in)
        session.add(source_db)
    await session.commit()
    await session.refresh(obj_in)
    return obj_in


async def distribution(
    obj_in: FinancialBase,
    obj_db: FinancialBase
) -> list[FinancialBase]:
    rem_obj_in = obj_in.full_amount - obj_in.invested_amount
    rem_obj_db = obj_db.full_amount - obj_db.invested_amount
    if rem_obj_in > rem_obj_db:
        obj_in.invested_amount += rem_obj_db
        obj_db = await close_entity(obj_db)
    elif rem_obj_in == rem_obj_db:
        obj_in = await close_entity(obj_in)
        obj_db = await close_entity(obj_db)
    else:
        obj_db.invested_amount += rem_obj_in
        obj_in = await close_entity(obj_in)
    return obj_in, obj_db


async def close_entity(
    obj_db: FinancialBase
) -> FinancialBase:
    obj_db.invested_amount = obj_db.full_amount
    obj_db.fully_invested = True
    obj_db.close_date = datetime.now()
    return obj_db
