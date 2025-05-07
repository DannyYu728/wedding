from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from app.db.base import Base

class User(Base):
    __tablename__ = "users"

    id                   = Column(Integer, primary_key=True, index=True)
    email                = Column(String, unique=True, index=True, nullable=False)
    full_name            = Column(String, nullable=False)
    hashed_password      = Column(String, nullable=False)
    is_active            = Column(Boolean, default=True, nullable=False)
    is_admin             = Column(Boolean, default=False, nullable=False)
    rsvp_confirmed       = Column(Boolean, default=False, nullable=False)
    dietary_restrictions = Column(String, nullable=True)
    created_at           = Column(DateTime(timezone=True), server_default=func.now())

    appetizer_option_id = Column(Integer, ForeignKey("dinner_options.id"), nullable=True)
    main_option_id = Column(Integer, ForeignKey("dinner_options.id"), nullable=True)

    appetizer_option = relationship("DinnerOption", foreign_keys=[appetizer_option_id], lazy="joined")
    main_option = relationship("DinnerOption", foreign_keys=[main_option_id], lazy="joined")   
