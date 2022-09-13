from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship

from src.db_models.base_model import SqlAlchemyBase

class UnregisteredUser(SqlAlchemyBase):
    __tablename__ = 'unregistered_users'

    id = Column(Integer, primary_key=True, autoincrement=True)

    ip_address = Column(String, nullable=False, index=True, unique=True)

    created_date = Column(DateTime, default=datetime.now, index=True)
    free_calls = Column(Integer, default=3)
    calls_made = Column(Integer, nullable=False, index=True)
    remaining_calls = Column(Integer, nullable=False, index=True)

    completions = relationship('Completion', back_populates='unregistered_user')
