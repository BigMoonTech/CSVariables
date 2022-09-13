from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from src.db_models.base_model import SqlAlchemyBase

class Completion(SqlAlchemyBase):
    __tablename__ = 'completions'

    id = Column(Integer, primary_key=True, autoincrement=True)

    completion_id = Column(String, nullable=False, index=True, unique=True)
    created = Column(DateTime, default=datetime.now, index=True)
    model = Column(String, nullable=False, index=True)
    prompt_text = Column(String, nullable=False, index=True)
    response_text = Column(String, nullable=False, index=True)
    finish_reason = Column(String, nullable=False, index=True)
    prompt_tokens = Column(Integer, nullable=False, index=True)
    completion_tokens = Column(Integer, nullable=False, index=True)
    total_tokens = Column(Integer, nullable=False, index=True)

    # define the relationship to the user and unregistered user
    # a completion can have one user OR one unregistered user
    user_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    ip_id = Column(Integer, ForeignKey('unregistered_users.id'), default=0, nullable=True)

    registered_user = relationship('User', back_populates='completions')
    unregistered_user = relationship('UnregisteredUser', back_populates='completions')
