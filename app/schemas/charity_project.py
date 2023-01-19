from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, Field, PositiveInt, validator


class CharityProjectBase(BaseModel):
    name: Optional[str]
    description: Optional[str]
    full_amount: Optional[PositiveInt]

    @validator('name')
    def using_name_as_null(cls, value: str):
        if value.isspace() or value == '' or value is None:
            raise ValueError('Project name canot be empty!')
        return value

    @validator('description')
    def using_description_as_null(cls, value: str):
        if value.isspace() or value == '' or value is None:
            raise ValueError('Project description canot be empty!')
        return value

    class Config:
        extra = Extra.forbid
        schema_extra = {
            "example": {
                "name": "Foo",
                "description": "A very nice Item",
                "full_amount": 35
            }
        }


class CharityProjectCreate(CharityProjectBase):
    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1)
    full_amount: PositiveInt


class CharityProjectUpdate(CharityProjectBase):
    pass


class CharityProjectDB(CharityProjectBase):
    id: int
    invested_amount: Optional[int]
    fully_invested: Optional[bool]
    create_date: Optional[datetime]
    close_date: Optional[datetime]

    class Config:
        orm_mode = True
