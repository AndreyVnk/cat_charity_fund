from sqlalchemy import Column, String, Text

from .financial_base import FinancialBase


class CharityProject(FinancialBase):
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=False)
