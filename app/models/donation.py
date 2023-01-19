from sqlalchemy import Column, ForeignKey, Integer, Text

from .financial_base import FinancialBase


class Donation(FinancialBase):
    user_id = Column(Integer, ForeignKey('user.id'))
    comment = Column(Text)
