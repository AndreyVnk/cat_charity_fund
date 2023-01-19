from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, PositiveInt


class DonationCreate(BaseModel):
    full_amount: PositiveInt
    comment: Optional[str]

    class Config:
        extra = Extra.forbid
        schema_extra = {
            "example": {
                "full_amount": 35,
                "comment": "A very big Donation",
            }
        }


class DonationDB(DonationCreate):
    id: int
    invested_amount: Optional[int]
    fully_invested: Optional[bool]
    create_date: Optional[datetime]
    user_id: Optional[int]

    class Config:
        orm_mode = True
