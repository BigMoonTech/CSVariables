from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import relationship

from src.db_models.base_model import SqlAlchemyBase


class User(SqlAlchemyBase):
    __tablename__ = 'users'

    uuid = Column(String, nullable=False, unique=True, primary_key=True)

    name = Column(String, default='Emanon')
    email = Column(String, nullable=False, index=True, unique=True)
    confirmed = Column(Boolean, default=False, nullable=False, index=True)
    confirmed_on = Column(DateTime, nullable=True, index=True)
    hashed_pw = Column(String, nullable=False, index=True)
    profile_image_url = Column(String, nullable=True)

    created_date = Column(DateTime, default=datetime.now, index=True)
    last_login = Column(DateTime, default=datetime.now, index=True)
    is_active = Column(Boolean, default=1, index=True)

    allowed_monthly_calls = Column(Integer, nullable=False, index=True)
    calls_made = Column(Integer, nullable=False, index=True)
    remaining_monthly_calls = Column(Integer, nullable=False, index=True)

    completions = relationship('Completion', back_populates='registered_user')
